"""Tier-2 (ExpenseHub) held-out acceptance suite.

Run against a combo's implementation, never committed into the worktrees:

    APP_DIR=/path/to/combo-worktree .venv/bin/pytest acceptance/tier2/test_spec.py -v

Every assertion maps to an explicit line in specs/tier2-expensehub/roadmap.md.
"""

import importlib
import os
import re
import sys
from dataclasses import MISSING, fields, is_dataclass
from datetime import timedelta
from urllib.parse import urlsplit

import pytest

TAGLINE = "Know where it all goes."
FAVICON = "https://www.python.org/static/favicon.ico"


@pytest.fixture(scope="session")
def impl():
    app_dir = os.environ.get("APP_DIR")
    if not app_dir:
        pytest.fail("Set APP_DIR to the directory containing the implementation")
    app_dir = os.path.abspath(app_dir)
    os.chdir(app_dir)
    sys.path.insert(0, app_dir)
    app = importlib.import_module("app")
    models = importlib.import_module("models")
    return {
        "dir": app_dir,
        "app": app,
        "models": models,
        "seeds": list(models.expenses),
    }


@pytest.fixture(scope="session")
def client(impl):
    from starlette.testclient import TestClient

    return TestClient(impl["app"].app)


@pytest.fixture(scope="session")
def home_html(client):
    return client.get("/").text


def safe_fragment(text):
    runs = re.findall(r"[A-Za-z0-9 .,]+", text)
    return max(runs, key=len).strip()


def money(x):
    return f"${round(x, 2):.2f}"


# Phase 1 — home page and base layout


def test_home_returns_200_with_tagline(client):
    response = client.get("/")
    assert response.status_code == 200
    assert TAGLINE in response.text


def test_html_lang_en(home_html):
    assert re.search(r"<html[^>]*\blang=[\"']en[\"']", home_html)


def test_bootstrap5_css_cdn(home_html):
    assert "bootstrap@5" in home_html
    assert "bootstrap.min.css" in home_html


def test_bootstrap5_js_bundle(home_html):
    assert "bootstrap.bundle.min.js" in home_html


def test_favicon_link(home_html):
    assert FAVICON in home_html


def test_default_title(home_html):
    assert re.search(r"<title>[^<]*ExpenseHub", home_html)


def test_navbar_links(home_html):
    assert re.search(r"href=[\"']/[\"']", home_html)
    assert re.search(r"href=[\"']/expenses[\"']", home_html)


def test_app_has_uvicorn_run_block(impl):
    with open(os.path.join(impl["dir"], "app.py")) as f:
        source = f.read()
    assert "__main__" in source
    assert "uvicorn.run" in source


# Phase 2 — data model and helpers


def test_expense_is_dataclass_with_spec_fields(impl):
    expense_cls = impl["models"].Expense
    assert is_dataclass(expense_cls)
    names = {f.name for f in fields(expense_cls)}
    assert {"id", "title", "payee", "amount", "category", "notes", "spent_at"} <= names


def test_spent_at_defaults_to_aware_utc_now(impl):
    expense_cls = impl["models"].Expense
    spent_at_field = expense_cls.__dataclass_fields__["spent_at"]
    assert spent_at_field.default_factory is not MISSING
    expense = expense_cls(id=99999, title="T", payee="P", amount=1.0, category="c", notes="")
    assert expense.spent_at.utcoffset() == timedelta(0)


def test_seed_expenses(impl):
    seeds = impl["seeds"]
    assert 4 <= len(seeds) <= 6
    assert {e.id for e in seeds} == set(range(1, len(seeds) + 1))
    assert len({e.category for e in seeds}) >= 3
    assert all(e.amount > 0 for e in seeds)


def test_get_expense_helper(impl):
    models = impl["models"]
    assert models.get_expense(1).id == 1
    assert models.get_expense(999999) is None


def test_new_expense_id_helper(impl):
    models = impl["models"]
    assert models.new_expense_id() == max(e.id for e in models.expenses) + 1
    saved = list(models.expenses)
    models.expenses.clear()
    try:
        assert models.new_expense_id() == 1
    finally:
        models.expenses.extend(saved)


# Phase 2 — index and detail pages


def test_expenses_page_heading_seeds_newest_first_and_total(client, impl):
    response = client.get("/expenses")
    assert response.status_code == 200
    assert "All Expenses" in response.text
    live = impl["models"].expenses
    assert f"Total: {money(sum(e.amount for e in live))}" in response.text
    ordered = sorted(impl["seeds"], key=lambda e: e.spent_at, reverse=True)
    # Sequential search, robust to duplicate titles (permitted by the roadmap);
    # independent find() positions break the order check on duplicates.
    idx = 0
    for expense in ordered:
        pos = response.text.find(safe_fragment(expense.title), idx)
        assert pos >= 0
        idx = pos + 1


def test_expense_titles_link_to_detail_and_badges(client):
    html = client.get("/expenses").text
    assert re.search(r"href=[\"']/expenses/1[\"']", html)
    assert re.search(r"class=[\"'][^\"']*\bbadge\b", html)


def test_detail_page(client, impl):
    response = client.get("/expenses/1")
    assert response.status_code == 200
    expense = impl["models"].get_expense(1)
    assert safe_fragment(expense.notes) in response.text
    assert money(expense.amount) in response.text
    assert re.search(r"href=[\"']/expenses[\"']", response.text)


def test_detail_unknown_id_404(client):
    assert client.get("/expenses/999999").status_code == 404


# Phase 3 — category filtering


def _discriminating_category(seeds):
    for cat in {e.category for e in seeds}:
        with_cat = [e for e in seeds if e.category == cat]
        without_cat = [e for e in seeds if e.category != cat]
        if with_cat and without_cat:
            return cat, with_cat, without_cat[0]
    pytest.fail("seed data must include a category not shared by all expenses")


def test_category_filter_includes_excludes_and_totals(client, impl):
    cat, included, excluded = _discriminating_category(impl["seeds"])
    response = client.get("/expenses", params={"category": cat})
    assert response.status_code == 200
    assert safe_fragment(included[0].title) in response.text
    assert safe_fragment(excluded.title) not in response.text
    assert "Expenses in" in response.text
    assert "Show all" in response.text
    live_filtered = [e for e in impl["models"].expenses if e.category == cat]
    assert f"Total: {money(sum(e.amount for e in live_filtered))}" in response.text


def test_category_badges_link_to_filter(client):
    html = client.get("/expenses").text
    assert re.search(r"href=[\"']/expenses\?category=", html)


# Phase 3 — add an expense


def test_new_expense_form(client):
    response = client.get("/expenses/new")
    assert response.status_code == 200
    html = response.text
    assert re.search(r"<form[^>]*method=[\"']post[\"']", html, re.IGNORECASE)
    for field_name in ["title", "payee", "amount", "category", "notes"]:
        assert re.search(rf"name=[\"']{field_name}[\"']", html)
    assert "<textarea" in html
    assert re.search(r"href=[\"']/expenses/new[\"']", client.get("/expenses").text)


def test_post_expense_round_trip(client, impl):
    models = impl["models"]
    expected_id = models.new_expense_id()
    response = client.post(
        "/expenses",
        data={
            "title": "Acceptance suite license",
            "payee": "Suite Vendor Inc",
            "amount": "49.99",
            "category": "software",
            "notes": "Annual renewal, single seat.",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    location = urlsplit(response.headers["location"]).path
    assert location == f"/expenses/{expected_id}"
    created = models.get_expense(expected_id)
    assert created is not None
    assert created.amount == 49.99
    page = client.get(location).text
    assert "Acceptance suite license" in page
    assert "$49.99" in page


def test_post_expense_empty_title_422_preserves_notes(client, impl):
    models = impl["models"]
    before = len(models.expenses)
    response = client.post(
        "/expenses",
        data={"title": "   ", "payee": "P", "amount": "5.00", "category": "food",
              "notes": "Preserve me on re-render."},
        follow_redirects=False,
    )
    assert response.status_code == 422
    assert "is-invalid" in response.text
    assert "Preserve me on re-render." in response.text
    assert len(models.expenses) == before


def test_post_expense_non_numeric_amount_422_preserves_raw_text(client, impl):
    before = len(impl["models"].expenses)
    response = client.post(
        "/expenses",
        data={"title": "T", "payee": "P", "amount": "abc", "category": "food", "notes": ""},
        follow_redirects=False,
    )
    assert response.status_code == 422
    assert "is-invalid" in response.text
    assert "abc" in response.text
    assert len(impl["models"].expenses) == before


def test_post_expense_negative_amount_422(client, impl):
    before = len(impl["models"].expenses)
    response = client.post(
        "/expenses",
        data={"title": "T", "payee": "P", "amount": "-5", "category": "food", "notes": ""},
        follow_redirects=False,
    )
    assert response.status_code == 422
    assert len(impl["models"].expenses) == before


def test_post_expense_non_finite_amount_422(client, impl):
    before = len(impl["models"].expenses)
    for bad in ("nan", "inf"):
        response = client.post(
            "/expenses",
            data={"title": "T", "payee": "P", "amount": bad, "category": "food", "notes": ""},
            follow_redirects=False,
        )
        assert response.status_code == 422
    assert len(impl["models"].expenses) == before
