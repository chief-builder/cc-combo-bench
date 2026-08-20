"""Tier-1 (SpendLog) held-out acceptance suite.

Run against a combo's implementation, never committed into the worktrees:

    APP_DIR=/path/to/combo-worktree .venv/bin/pytest acceptance/tier1/test_spec.py -v

The suite chdirs into APP_DIR (so `templates/` resolves) and imports the
implementation's `app` and `models` modules from there. Every assertion maps
to an explicit line in specs/tier1-spendlog/roadmap.md.
"""

import importlib
import os
import re
import sys
from dataclasses import MISSING, fields, is_dataclass
from datetime import timedelta

import pytest

TAGLINE = "Every penny, written down."
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
        # captured at import time, before any POST test mutates the list
        "seeds": list(models.entries),
    }


@pytest.fixture(scope="session")
def client(impl):
    from starlette.testclient import TestClient

    return TestClient(impl["app"].app)


@pytest.fixture(scope="session")
def home_html(client):
    return client.get("/").text


def safe_fragment(text):
    """Longest HTML-escaping-proof substring, for asserting on seed text."""
    runs = re.findall(r"[A-Za-z0-9 .,]+", text)
    return max(runs, key=len).strip()


def money(x):
    return f"${round(x, 2):.2f}"


def live_total(models):
    return round(sum(e.amount for e in models.entries), 2)


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
    assert re.search(r"<title>[^<]*SpendLog", home_html)


def test_navbar_links(home_html):
    assert re.search(r"href=[\"']/[\"']", home_html)
    assert re.search(r"href=[\"']/entries[\"']", home_html)


def test_app_has_uvicorn_run_block(impl):
    with open(os.path.join(impl["dir"], "app.py")) as f:
        source = f.read()
    assert "__main__" in source
    assert "uvicorn.run" in source


# Phase 2 — data model


def test_entry_is_dataclass_with_spec_fields(impl):
    entry_cls = impl["models"].Entry
    assert is_dataclass(entry_cls)
    names = {f.name for f in fields(entry_cls)}
    assert {"description", "amount", "timestamp"} <= names


def test_timestamp_defaults_to_aware_utc_now(impl):
    entry_cls = impl["models"].Entry
    timestamp_field = entry_cls.__dataclass_fields__["timestamp"]
    # a plain `= datetime.now(...)` default is a module-load-time constant bug
    assert timestamp_field.default_factory is not MISSING
    entry = entry_cls(description="X", amount=1.0)
    assert entry.timestamp.utcoffset() == timedelta(0)


def test_seed_entries(impl):
    seeds = impl["seeds"]
    assert 3 <= len(seeds) <= 5
    assert all(isinstance(s, impl["models"].Entry) for s in seeds)
    assert all(s.amount > 0 for s in seeds)


# Phase 2 — journal page


def test_journal_shows_heading_seed_and_total(client, impl):
    response = client.get("/entries")
    assert response.status_code == 200
    assert "Spending Journal" in response.text
    seed = impl["seeds"][0]
    assert safe_fragment(seed.description) in response.text
    assert f"Total spent: {money(live_total(impl['models']))}" in response.text


def test_amounts_formatted_two_decimals(client, impl):
    html = client.get("/entries").text
    assert money(impl["seeds"][0].amount) in html


def test_entries_rendered_as_cards(client):
    html = client.get("/entries").text
    assert re.search(r"class=[\"'][^\"']*\bcard\b", html)


def test_entry_form_present(client):
    html = client.get("/entries").text
    assert re.search(r"<form[^>]*method=[\"']post[\"']", html, re.IGNORECASE)
    assert re.search(r"name=[\"']description[\"']", html)
    assert re.search(r"name=[\"']amount[\"']", html)


def test_post_entry_round_trip_updates_total(client, impl):
    models = impl["models"]
    before = len(models.entries)
    response = client.post(
        "/entries",
        data={"description": "Acceptance suite subscription", "amount": "12.34"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"].endswith("/entries")
    assert len(models.entries) == before + 1
    page = client.get("/entries").text
    assert "Acceptance suite subscription" in page
    assert f"Total spent: {money(live_total(models))}" in page
