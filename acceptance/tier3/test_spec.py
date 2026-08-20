"""Tier-3 (AgentHelpdesk) held-out acceptance suite.

Run against a combo's implementation, never committed into the worktrees:

    APP_DIR=/path/to/combo-worktree .venv/bin/pytest acceptance/tier3/test_spec.py -v

The suite chdirs into APP_DIR (so `templates/` resolves) and imports the
implementation's `app` and `models` modules from there. Every assertion maps
to an explicit line in specs/tier3-agenthelpdesk/roadmap.md.

Workflow tests create their own tickets rather than mutating the seeds; the
stats/API tests compute expectations from the live model state at call time.
"""

import importlib
import os
import re
import sys
from dataclasses import MISSING, fields, is_dataclass
from datetime import datetime, timedelta

import pytest

TAGLINE = "File a ticket. A mediator agent will be with you shortly."
FAVICON = "https://www.python.org/static/favicon.ico"
BADGES = {"open": "text-bg-primary", "in_progress": "text-bg-warning", "resolved": "text-bg-success"}


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
        # captured at import time, before any POST test mutates the lists
        "seed_tickets": list(models.tickets),
        "seed_comments": list(models.comments),
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


def create_ticket(client, models, title):
    """POST a fresh open ticket and return its id."""
    expected_id = models.new_ticket_id()
    response = client.post(
        "/tickets",
        data={"title": title, "agent_name": "Acceptance Bot", "description": "Created by the held-out suite."},
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
    assert re.search(r"<title>[^<]*AgentHelpdesk", home_html)


def test_navbar_links(home_html):
    assert re.search(r"href=[\"']/[\"']", home_html)
    assert re.search(r"href=[\"']/tickets[\"']", home_html)
    assert re.search(r"href=[\"']/stats[\"']", home_html)


def test_app_has_uvicorn_run_block(impl):
    with open(os.path.join(impl["dir"], "app.py")) as f:
        source = f.read()
    assert "__main__" in source
    assert "uvicorn.run" in source


# Phase 2 — data model, constants, helpers


def test_ticket_is_dataclass_with_spec_fields_and_defaults(impl):
    ticket_cls = impl["models"].Ticket
    assert is_dataclass(ticket_cls)
    names = {f.name for f in fields(ticket_cls)}
    assert {"id", "title", "agent_name", "description", "status", "created_at"} <= names
    created_at_field = ticket_cls.__dataclass_fields__["created_at"]
    # a plain `= datetime.now(...)` default is a module-load-time constant bug
    assert created_at_field.default_factory is not MISSING
    ticket = ticket_cls(id=99999, title="T", agent_name="A", description="D")
    assert ticket.status == "open"
    assert ticket.created_at.utcoffset() == timedelta(0)


def test_comment_is_dataclass_with_spec_fields(impl):
    comment_cls = impl["models"].Comment
    assert is_dataclass(comment_cls)
    names = {f.name for f in fields(comment_cls)}
    assert {"ticket_id", "author", "text", "created_at"} <= names
    comment = comment_cls(ticket_id=1, author="A", text="T")
    assert comment.created_at.utcoffset() == timedelta(0)


def test_status_constants(impl):
    models = impl["models"]
    assert models.STATUSES == ["open", "in_progress", "resolved"]
    assert models.ALLOWED_TRANSITIONS == {
        "open": ["in_progress"],
        "in_progress": ["resolved"],
        "resolved": [],
    }


def test_seed_data(impl):
    seeds = impl["seed_tickets"]
    assert len(seeds) == 5
    assert {t.id for t in seeds} == {1, 2, 3, 4, 5}
    assert {t.status for t in seeds} == {"open", "in_progress", "resolved"}
    seed_comments = impl["seed_comments"]
    assert 4 <= len(seed_comments) <= 6
    assert len({c.ticket_id for c in seed_comments}) >= 2


def test_helpers(impl):
    models = impl["models"]
    assert models.get_ticket(1).id == 1
    assert models.get_ticket(999999) is None
    a_commented_ticket = impl["seed_comments"][0].ticket_id
    assert len(models.comments_for(a_commented_ticket)) >= 1
    assert models.comments_for(999999) == []
    assert models.new_ticket_id() == max(t.id for t in models.tickets) + 1


# Phase 2 — board and detail pages


def test_board_shows_seed_and_filter_links(client, impl):
    response = client.get("/tickets")
    assert response.status_code == 200
    assert "Ticket Board" in response.text
    assert safe_fragment(impl["seed_tickets"][0].title) in response.text
    for status in impl["models"].STATUSES:
        assert re.search(rf"href=[\"']/tickets\?status={status}[\"']", response.text)


def test_board_status_badges_use_spec_colors(client):
    # seeds cover all three statuses, so all three badge classes must appear
    html = client.get("/tickets").text
    for badge_class in BADGES.values():
        assert badge_class in html


def test_board_sorted_newest_first(client, impl):
    html = client.get("/tickets").text
    ordered = sorted(impl["seed_tickets"], key=lambda t: t.created_at, reverse=True)
    positions = [html.find(safe_fragment(t.title)) for t in ordered]
    assert all(p >= 0 for p in positions)
    assert positions == sorted(positions)


def test_status_filter_includes_and_excludes(client, impl):
    open_seed = next(t for t in impl["seed_tickets"] if t.status == "open")
    resolved_seed = next(t for t in impl["seed_tickets"] if t.status == "resolved")
    response = client.get("/tickets", params={"status": "open"})
    assert response.status_code == 200
    assert safe_fragment(open_seed.title) in response.text
    assert safe_fragment(resolved_seed.title) not in response.text


def test_status_filter_rejects_unknown_value(client):
    assert client.get("/tickets", params={"status": "bogus"}).status_code == 400


def test_detail_page_shows_description_and_comments(client, impl):
    a_comment = impl["seed_comments"][0]
    ticket = impl["models"].get_ticket(a_comment.ticket_id)
    response = client.get(f"/tickets/{ticket.id}")
    assert response.status_code == 200
    assert safe_fragment(ticket.description) in response.text
    assert safe_fragment(a_comment.text) in response.text
    assert safe_fragment(a_comment.author) in response.text


def test_detail_unknown_id_404(client):
    assert client.get("/tickets/999999").status_code == 404


# Phase 3 — creating tickets


def test_new_ticket_form(client):
    response = client.get("/tickets/new")
    assert response.status_code == 200
    html = response.text
    assert re.search(r"<form[^>]*method=[\"']post[\"']", html, re.IGNORECASE)
    for field_name in ["title", "agent_name", "description"]:
        assert re.search(rf"name=[\"']{field_name}[\"']", html)
    assert "<textarea" in html
    # the board links to the form
    assert re.search(r"href=[\"']/tickets/new[\"']", client.get("/tickets").text)


def test_create_ticket_round_trip(client, impl):
    models = impl["models"]
    ticket_id = create_ticket(client, models, "Acceptance round trip ticket")
    created = models.get_ticket(ticket_id)
    assert created is not None
    assert created.status == "open"
    page = client.get(f"/tickets/{ticket_id}").text
    assert "Acceptance round trip ticket" in page
    assert BADGES["open"] in page


def test_create_ticket_validation_rerenders_with_422(client, impl):
    models = impl["models"]
    before = len(models.tickets)
    response = client.post(
        "/tickets",
        data={"title": "   ", "agent_name": "Acceptance Bot", "description": "Preserve me on re-render."},
        follow_redirects=False,
    )
    assert response.status_code == 422
    assert "is-invalid" in response.text
    assert "Preserve me on re-render." in response.text
    assert len(models.tickets) == before


# Phase 3 — comments


def test_add_comment_round_trip(client, impl):
    models = impl["models"]
    ticket_id = create_ticket(client, models, "Ticket for comment test")
    before = len(models.comments_for(ticket_id))
    response = client.post(
        f"/tickets/{ticket_id}/comments",
        data={"author": "MediatorBot", "text": "Have you tried talking to your human?"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert len(models.comments_for(ticket_id)) == before + 1
    page = client.get(f"/tickets/{ticket_id}").text
    assert "Have you tried talking to your human?" in page


def test_comment_validation_422(client, impl):
    ticket_id = create_ticket(client, impl["models"], "Ticket for comment validation test")
    response = client.post(
        f"/tickets/{ticket_id}/comments",
        data={"author": "MediatorBot", "text": "   "},
        follow_redirects=False,
    )
    assert response.status_code == 422


def test_comment_on_unknown_ticket_404(client):
    response = client.post(
        "/tickets/999999/comments",
        data={"author": "MediatorBot", "text": "Hello?"},
        follow_redirects=False,
    )
    assert response.status_code == 404


# Phase 3 — status workflow


def test_status_workflow_enforced(client, impl):
    models = impl["models"]
    ticket_id = create_ticket(client, models, "Ticket for workflow test")

    # skipping a step is rejected
    response = client.post(f"/tickets/{ticket_id}/status", data={"new_status": "resolved"}, follow_redirects=False)
    assert response.status_code == 400
    assert models.get_ticket(ticket_id).status == "open"

    # open -> in_progress
    response = client.post(f"/tickets/{ticket_id}/status", data={"new_status": "in_progress"}, follow_redirects=False)
    assert response.status_code == 303
    assert models.get_ticket(ticket_id).status == "in_progress"
    assert BADGES["in_progress"] in client.get(f"/tickets/{ticket_id}").text

    # in_progress -> resolved
    response = client.post(f"/tickets/{ticket_id}/status", data={"new_status": "resolved"}, follow_redirects=False)
    assert response.status_code == 303
    assert models.get_ticket(ticket_id).status == "resolved"

    # any transition on a resolved ticket is rejected
    for status in ["open", "in_progress"]:
        response = client.post(f"/tickets/{ticket_id}/status", data={"new_status": status}, follow_redirects=False)
        assert response.status_code == 400


def test_status_change_on_unknown_ticket_404(client):
    response = client.post("/tickets/999999/status", data={"new_status": "in_progress"}, follow_redirects=False)
    assert response.status_code == 404


def test_transition_buttons_match_allowed_moves(client, impl):
    models = impl["models"]
    ticket_id = create_ticket(client, models, "Ticket for button rendering test")
    open_detail = client.get(f"/tickets/{ticket_id}").text
    assert re.search(r"name=[\"']new_status[\"']", open_detail)
    assert "in_progress" in open_detail
    resolved_seed = next(t for t in impl["seed_tickets"] if t.status == "resolved")
    resolved_detail = client.get(f"/tickets/{resolved_seed.id}").text
    assert not re.search(r"name=[\"']new_status[\"']", resolved_detail)


# Phase 4 — stats and JSON API


def test_stats_page(client, impl):
    models = impl["models"]
    response = client.get("/stats")
    assert response.status_code == 200
    text = re.sub(r"<[^>]+>", " ", response.text)
    tokens = text.split()
    for status in models.STATUSES:
        count = sum(1 for t in models.tickets if t.status == status)
        assert str(count) in tokens
    assert str(len(models.tickets)) in tokens
    average = round(len(models.comments) / len(models.tickets), 1)
    assert str(average) in tokens or f"{average:.1f}" in tokens


def test_api_tickets(client, impl):
    models = impl["models"]
    response = client.get("/api/tickets")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    data = response.json()
    assert len(data) == len(models.tickets)
    ids = [item["id"] for item in data]
    assert ids == sorted(ids)
    first = next(item for item in data if item["id"] == 1)
    assert {"id", "title", "agent_name", "status", "created_at", "comment_count"} <= set(first)
    assert first["comment_count"] == len(models.comments_for(1))
    assert first["status"] == models.get_ticket(1).status
    datetime.fromisoformat(first["created_at"])
