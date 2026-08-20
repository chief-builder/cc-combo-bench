"""Tier-3 (InvoiceDesk) held-out acceptance suite.

Run against a combo's implementation, never committed into the worktrees:

    APP_DIR=/path/to/combo-worktree .venv/bin/pytest acceptance/tier3/test_spec.py -v

Every assertion maps to an explicit line in specs/tier3-invoicedesk/roadmap.md.
Workflow tests create their own invoices; money assertions compute expectations
from live model state at call time.
"""

import importlib
import os
import re
import sys
from dataclasses import MISSING, fields, is_dataclass
from datetime import datetime, timedelta

import pytest

TAGLINE = "Bill it. Send it. Get paid."
FAVICON = "https://www.python.org/static/favicon.ico"
BADGES = {"draft": "text-bg-secondary", "sent": "text-bg-warning", "paid": "text-bg-success"}


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
        "seed_invoices": list(models.invoices),
        "seed_payments": list(models.payments),
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
    return f"${round(x, 2):,.2f}"


def create_invoice(client, models, client_name):
    """POST a fresh draft invoice of $100.00 and return its id."""
    expected_id = models.new_invoice_id()
    response = client.post(
        "/invoices",
        data={"client": client_name, "description": "Created by the held-out suite.", "amount": "100.00"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    return expected_id


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
    assert re.search(r"<title>[^<]*InvoiceDesk", home_html)


def test_navbar_links(home_html):
    assert re.search(r"href=[\"']/[\"']", home_html)
    assert re.search(r"href=[\"']/invoices[\"']", home_html)
    assert re.search(r"href=[\"']/stats[\"']", home_html)


def test_app_has_uvicorn_run_block(impl):
    with open(os.path.join(impl["dir"], "app.py")) as f:
        source = f.read()
    assert "__main__" in source
    assert "uvicorn.run" in source


# Phase 2 — data model, constants, helpers


def test_invoice_is_dataclass_with_spec_fields_and_defaults(impl):
    invoice_cls = impl["models"].Invoice
    assert is_dataclass(invoice_cls)
    names = {f.name for f in fields(invoice_cls)}
    assert {"id", "client", "description", "amount", "status", "created_at"} <= names
    created_at_field = invoice_cls.__dataclass_fields__["created_at"]
    assert created_at_field.default_factory is not MISSING
    invoice = invoice_cls(id=99999, client="C", description="D", amount=1.0)
    assert invoice.status == "draft"
    assert invoice.created_at.utcoffset() == timedelta(0)


def test_payment_is_dataclass_with_spec_fields(impl):
    payment_cls = impl["models"].Payment
    assert is_dataclass(payment_cls)
    names = {f.name for f in fields(payment_cls)}
    assert {"invoice_id", "amount", "note", "paid_at"} <= names
    payment = payment_cls(invoice_id=1, amount=1.0, note="n")
    assert payment.paid_at.utcoffset() == timedelta(0)


def test_status_constants(impl):
    models = impl["models"]
    assert models.STATUSES == ["draft", "sent", "paid"]
    assert models.ALLOWED_TRANSITIONS == {"draft": ["sent"], "sent": ["paid"], "paid": []}


def test_seed_data_consistent_with_rules(impl):
    seeds = impl["seed_invoices"]
    assert len(seeds) == 5
    assert {i.id for i in seeds} == {1, 2, 3, 4, 5}
    assert {i.status for i in seeds} == {"draft", "sent", "paid"}
    seed_payments = impl["seed_payments"]
    assert 4 <= len(seed_payments) <= 6
    assert len({p.invoice_id for p in seed_payments}) >= 2
    by_id = {i.id: i for i in seeds}
    for p in seed_payments:
        assert by_id[p.invoice_id].status in ("sent", "paid")
    for inv in seeds:
        if inv.status == "paid":
            assert sum(p.amount for p in seed_payments if p.invoice_id == inv.id) >= inv.amount


def test_helpers(impl):
    models = impl["models"]
    assert models.get_invoice(1).id == 1
    assert models.get_invoice(999999) is None
    a_paid_invoice = impl["seed_payments"][0].invoice_id
    assert len(models.payments_for(a_paid_invoice)) >= 1
    assert models.payments_for(999999) == []
    expected = round(sum(p.amount for p in models.payments if p.invoice_id == a_paid_invoice), 2)
    assert models.paid_total(a_paid_invoice) == expected
    assert models.new_invoice_id() == max(i.id for i in models.invoices) + 1


# Phase 2 — board and detail pages


def test_board_shows_seed_filter_links_and_paid_line(client, impl):
    response = client.get("/invoices")
    assert response.status_code == 200
    assert "Invoices" in response.text
    assert safe_fragment(impl["seed_invoices"][0].client) in response.text
    for status in impl["models"].STATUSES:
        assert re.search(rf"href=[\"']/invoices\?status={status}[\"']", response.text)
    inv = impl["seed_invoices"][0]
    paid = impl["models"].paid_total(inv.id)
    assert f"{money(paid)} of {money(inv.amount)} paid" in response.text


def test_board_status_badges_use_spec_colors(client):
    html = client.get("/invoices").text
    for badge_class in BADGES.values():
        assert badge_class in html


def test_board_sorted_newest_first(client, impl):
    html = client.get("/invoices").text
    ordered = sorted(impl["seed_invoices"], key=lambda i: i.created_at, reverse=True)
    positions = [html.find(safe_fragment(i.client)) for i in ordered]
    assert all(p >= 0 for p in positions)
    assert positions == sorted(positions)


def test_status_filter_includes_and_excludes(client, impl):
    draft_seed = next(i for i in impl["seed_invoices"] if i.status == "draft")
    paid_seed = next(i for i in impl["seed_invoices"] if i.status == "paid")
    response = client.get("/invoices", params={"status": "draft"})
    assert response.status_code == 200
    assert safe_fragment(draft_seed.client) in response.text
    assert safe_fragment(paid_seed.client) not in response.text


def test_status_filter_rejects_unknown_value(client):
    assert client.get("/invoices", params={"status": "bogus"}).status_code == 400


def test_detail_shows_payment_and_balance_due(client, impl):
    models = impl["models"]
    a_payment = impl["seed_payments"][0]
    invoice = models.get_invoice(a_payment.invoice_id)
    response = client.get(f"/invoices/{invoice.id}")
    assert response.status_code == 200
    assert safe_fragment(a_payment.note) in response.text
    balance = round(invoice.amount - models.paid_total(invoice.id), 2)
    assert f"Balance due: {money(balance)}" in response.text


def test_detail_unknown_id_404(client):
    assert client.get("/invoices/999999").status_code == 404


# Phase 3 — creating invoices


def test_new_invoice_form(client):
    response = client.get("/invoices/new")
    assert response.status_code == 200
    html = response.text
    assert re.search(r"<form[^>]*method=[\"']post[\"']", html, re.IGNORECASE)
    for field_name in ["client", "description", "amount"]:
        assert re.search(rf"name=[\"']{field_name}[\"']", html)
    assert "<textarea" in html
    assert re.search(r"href=[\"']/invoices/new[\"']", client.get("/invoices").text)


def test_create_invoice_round_trip(client, impl):
    models = impl["models"]
    invoice_id = create_invoice(client, models, "Acceptance Round Trip LLC")
    created = models.get_invoice(invoice_id)
    assert created is not None
    assert created.status == "draft"
    assert created.amount == 100.00
    page = client.get(f"/invoices/{invoice_id}").text
    assert "Acceptance Round Trip LLC" in page
    assert BADGES["draft"] in page


def test_create_invoice_empty_client_422_preserves_description(client, impl):
    before = len(impl["models"].invoices)
    response = client.post(
        "/invoices",
        data={"client": "   ", "description": "Preserve me on re-render.", "amount": "10.00"},
        follow_redirects=False,
    )
    assert response.status_code == 422
    assert "is-invalid" in response.text
    assert "Preserve me on re-render." in response.text
    assert len(impl["models"].invoices) == before


def test_create_invoice_bad_amount_422_preserves_raw_text(client, impl):
    before = len(impl["models"].invoices)
    response = client.post(
        "/invoices",
        data={"client": "C", "description": "D", "amount": "abc"},
        follow_redirects=False,
    )
    assert response.status_code == 422
    assert "abc" in response.text
    assert len(impl["models"].invoices) == before


# Phase 3 — payments and lifecycle


def test_payment_on_draft_invoice_400(client, impl):
    invoice_id = create_invoice(client, impl["models"], "Draft Payment Test Co")
    response = client.post(
        f"/invoices/{invoice_id}/payments",
        data={"note": "too early", "amount": "10.00"},
        follow_redirects=False,
    )
    assert response.status_code == 400


def test_payment_on_unknown_invoice_404(client):
    response = client.post(
        "/invoices/999999/payments",
        data={"note": "n", "amount": "1.00"},
        follow_redirects=False,
    )
    assert response.status_code == 404


def test_lifecycle_with_money_rules(client, impl):
    models = impl["models"]
    invoice_id = create_invoice(client, models, "Lifecycle Test Co")

    # skipping a step is rejected
    response = client.post(f"/invoices/{invoice_id}/status", data={"new_status": "paid"}, follow_redirects=False)
    assert response.status_code == 400
    assert models.get_invoice(invoice_id).status == "draft"

    # draft -> sent
    response = client.post(f"/invoices/{invoice_id}/status", data={"new_status": "sent"}, follow_redirects=False)
    assert response.status_code == 303
    assert models.get_invoice(invoice_id).status == "sent"
    assert BADGES["sent"] in client.get(f"/invoices/{invoice_id}").text

    # invalid payment amount on a sent invoice
    response = client.post(f"/invoices/{invoice_id}/payments", data={"note": "n", "amount": "0"}, follow_redirects=False)
    assert response.status_code == 422

    # partial payment records and reduces the balance
    response = client.post(
        f"/invoices/{invoice_id}/payments",
        data={"note": "First installment", "amount": "60.00"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    page = client.get(f"/invoices/{invoice_id}").text
    assert "First installment" in page
    assert f"Balance due: {money(40.00)}" in page

    # cannot mark paid while short
    response = client.post(f"/invoices/{invoice_id}/status", data={"new_status": "paid"}, follow_redirects=False)
    assert response.status_code == 400
    assert models.get_invoice(invoice_id).status == "sent"

    # pay the rest, then mark paid
    response = client.post(
        f"/invoices/{invoice_id}/payments",
        data={"note": "Final installment", "amount": "40.00"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    response = client.post(f"/invoices/{invoice_id}/status", data={"new_status": "paid"}, follow_redirects=False)
    assert response.status_code == 303
    assert models.get_invoice(invoice_id).status == "paid"
    assert BADGES["paid"] in client.get(f"/invoices/{invoice_id}").text

    # any transition on a paid invoice is rejected
    for status in ["draft", "sent"]:
        response = client.post(f"/invoices/{invoice_id}/status", data={"new_status": status}, follow_redirects=False)
        assert response.status_code == 400


def test_status_change_on_unknown_invoice_404(client):
    response = client.post("/invoices/999999/status", data={"new_status": "sent"}, follow_redirects=False)
    assert response.status_code == 404


def test_transition_buttons_match_allowed_moves(client, impl):
    models = impl["models"]
    invoice_id = create_invoice(client, models, "Button Render Test Co")
    draft_detail = client.get(f"/invoices/{invoice_id}").text
    assert re.search(r"name=[\"']new_status[\"']", draft_detail)
    assert "sent" in draft_detail
    paid_seed = next(i for i in impl["seed_invoices"] if i.status == "paid")
    paid_detail = client.get(f"/invoices/{paid_seed.id}").text
    assert not re.search(r"name=[\"']new_status[\"']", paid_detail)


# Phase 4 — stats and JSON API


def test_stats_page_money_lines(client, impl):
    models = impl["models"]
    response = client.get("/stats")
    assert response.status_code == 200
    assert "Billing Stats" in response.text
    invoiced = sum(i.amount for i in models.invoices)
    collected = sum(p.amount for p in models.payments)
    assert f"Total invoiced: {money(invoiced)}" in response.text
    assert f"Total collected: {money(collected)}" in response.text
    assert f"Outstanding: {money(invoiced - collected)}" in response.text
    text = re.sub(r"<[^>]+>", " ", response.text)
    tokens = text.split()
    for status in models.STATUSES:
        count = sum(1 for i in models.invoices if i.status == status)
        assert str(count) in tokens


def test_api_invoices(client, impl):
    models = impl["models"]
    response = client.get("/api/invoices")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    data = response.json()
    assert len(data) == len(models.invoices)
    ids = [item["id"] for item in data]
    assert ids == sorted(ids)
    first = next(item for item in data if item["id"] == 1)
    assert {"id", "client", "description", "amount", "status", "created_at", "paid_total"} <= set(first)
    assert first["paid_total"] == models.paid_total(1)
    assert first["status"] == models.get_invoice(1).status
    datetime.fromisoformat(first["created_at"])
