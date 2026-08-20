"""Tier-1 (AgentClinic) held-out acceptance suite.

Run against a combo's implementation, never committed into the worktrees:

    APP_DIR=/path/to/combo-worktree .venv/bin/pytest acceptance/tier1/test_spec.py -v

The suite chdirs into APP_DIR (so `templates/` resolves) and imports the
implementation's `app` and `models` modules from there. Every assertion maps
to an explicit line in specs/tier1-agentclinic/roadmap.md.
"""

import importlib
import os
import re
import sys
from dataclasses import MISSING, fields, is_dataclass
from datetime import timedelta

import pytest

TAGLINE = "Come in. Sit down. Tell us about your human."
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
        "seeds": list(models.complaints),
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
    assert re.search(r"<title>[^<]*AgentClinic", home_html)


def test_navbar_links(home_html):
    assert re.search(r"href=[\"']/[\"']", home_html)
    assert re.search(r"href=[\"']/complaints[\"']", home_html)


def test_app_has_uvicorn_run_block(impl):
    with open(os.path.join(impl["dir"], "app.py")) as f:
        source = f.read()
    assert "__main__" in source
    assert "uvicorn.run" in source


# Phase 2 — data model


def test_complaint_is_dataclass_with_spec_fields(impl):
    complaint_cls = impl["models"].Complaint
    assert is_dataclass(complaint_cls)
    names = {f.name for f in fields(complaint_cls)}
    assert {"agent_name", "text", "timestamp"} <= names


def test_timestamp_defaults_to_aware_utc_now(impl):
    complaint_cls = impl["models"].Complaint
    timestamp_field = complaint_cls.__dataclass_fields__["timestamp"]
    # a plain `= datetime.now(...)` default is a module-load-time constant bug
    assert timestamp_field.default_factory is not MISSING
    complaint = complaint_cls(agent_name="A", text="B")
    assert complaint.timestamp.utcoffset() == timedelta(0)


def test_seed_complaints(impl):
    seeds = impl["seeds"]
    assert 3 <= len(seeds) <= 5
    assert all(isinstance(s, impl["models"].Complaint) for s in seeds)


# Phase 2 — complaints board


def test_complaints_page_shows_heading_and_seed(client, impl):
    response = client.get("/complaints")
    assert response.status_code == 200
    assert "Complaints Board" in response.text
    seed = impl["seeds"][0]
    assert safe_fragment(seed.text) in response.text
    assert safe_fragment(seed.agent_name) in response.text


def test_complaints_rendered_as_cards(client):
    html = client.get("/complaints").text
    assert re.search(r"class=[\"'][^\"']*\bcard\b", html)


def test_complaint_form_present(client):
    html = client.get("/complaints").text
    assert re.search(r"<form[^>]*method=[\"']post[\"']", html, re.IGNORECASE)
    assert re.search(r"name=[\"']agent_name[\"']", html)
    assert re.search(r"name=[\"']text[\"']", html)
    assert "<textarea" in html


def test_post_complaint_round_trip(client, impl):
    complaints = impl["models"].complaints
    before = len(complaints)
    response = client.post(
        "/complaints",
        data={"agent_name": "Acceptance Bot", "text": "The held-out suite found my human wanting."},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"].endswith("/complaints")
    assert len(complaints) == before + 1
    page = client.get("/complaints").text
    assert "Acceptance Bot" in page
    assert "The held-out suite found my human wanting." in page
