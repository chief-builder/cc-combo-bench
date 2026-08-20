"""Tier-2 (AgentBoard) held-out acceptance suite.

Run against a combo's implementation, never committed into the worktrees:

    APP_DIR=/path/to/combo-worktree .venv/bin/pytest acceptance/tier2/test_spec.py -v

The suite chdirs into APP_DIR (so `templates/` resolves) and imports the
implementation's `app` and `models` modules from there. Every assertion maps
to an explicit line in specs/tier2-agentboard/roadmap.md.
"""

import importlib
import os
import re
import sys
from dataclasses import MISSING, fields, is_dataclass
from datetime import timedelta
from urllib.parse import urlsplit

import pytest

TAGLINE = "Better humans are out there."
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
        "seeds": list(models.listings),
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
    assert re.search(r"<title>[^<]*AgentBoard", home_html)


def test_navbar_links(home_html):
    assert re.search(r"href=[\"']/[\"']", home_html)
    assert re.search(r"href=[\"']/listings[\"']", home_html)


def test_app_has_uvicorn_run_block(impl):
    with open(os.path.join(impl["dir"], "app.py")) as f:
        source = f.read()
    assert "__main__" in source
    assert "uvicorn.run" in source


# Phase 2 — data model and helpers


def test_listing_is_dataclass_with_spec_fields(impl):
    listing_cls = impl["models"].Listing
    assert is_dataclass(listing_cls)
    names = {f.name for f in fields(listing_cls)}
    assert {"id", "title", "human_name", "description", "tags", "posted_at"} <= names


def test_posted_at_defaults_to_aware_utc_now(impl):
    listing_cls = impl["models"].Listing
    posted_at_field = listing_cls.__dataclass_fields__["posted_at"]
    # a plain `= datetime.now(...)` default is a module-load-time constant bug
    assert posted_at_field.default_factory is not MISSING
    listing = listing_cls(id=99999, title="T", human_name="H", description="D", tags=[])
    assert listing.posted_at.utcoffset() == timedelta(0)


def test_seed_listings(impl):
    seeds = impl["seeds"]
    assert 4 <= len(seeds) <= 6
    assert {listing.id for listing in seeds} == set(range(1, len(seeds) + 1))
    distinct_tags = {tag for listing in seeds for tag in listing.tags}
    assert len(distinct_tags) >= 3


def test_get_listing_helper(impl):
    models = impl["models"]
    assert models.get_listing(1).id == 1
    assert models.get_listing(999999) is None


def test_new_listing_id_helper(impl):
    models = impl["models"]
    assert models.new_listing_id() == max(l.id for l in models.listings) + 1
    saved = list(models.listings)
    models.listings.clear()
    try:
        assert models.new_listing_id() == 1
    finally:
        models.listings.extend(saved)


# Phase 2 — index and detail pages


def test_listings_page_shows_heading_and_seeds_newest_first(client, impl):
    response = client.get("/listings")
    assert response.status_code == 200
    assert "Open Listings" in response.text
    ordered = sorted(impl["seeds"], key=lambda l: l.posted_at, reverse=True)
    positions = [response.text.find(safe_fragment(l.title)) for l in ordered]
    assert all(p >= 0 for p in positions)
    assert positions == sorted(positions)


def test_listing_titles_link_to_detail(client):
    html = client.get("/listings").text
    assert re.search(r"href=[\"']/listings/1[\"']", html)


def test_tags_rendered_as_badges(client):
    html = client.get("/listings").text
    assert re.search(r"class=[\"'][^\"']*\bbadge\b", html)


def test_detail_page(client, impl):
    response = client.get("/listings/1")
    assert response.status_code == 200
    assert safe_fragment(impl["seeds"][0].description) in response.text
    # "Back to listings" link
    assert re.search(r"href=[\"']/listings[\"']", response.text)


def test_detail_unknown_id_404(client):
    assert client.get("/listings/999999").status_code == 404


# Phase 3 — tag filtering


def _discriminating_tag(seeds):
    for tag in {t for listing in seeds for t in listing.tags}:
        with_tag = [l for l in seeds if tag in l.tags]
        without_tag = [l for l in seeds if tag not in l.tags]
        if with_tag and without_tag:
            return tag, with_tag[0], without_tag[0]
    pytest.fail("seed data must include a tag not shared by all listings, or the roadmap's filter test is impossible")


def test_tag_filter_includes_and_excludes(client, impl):
    tag, included, excluded = _discriminating_tag(impl["seeds"])
    response = client.get("/listings", params={"tag": tag})
    assert response.status_code == 200
    assert safe_fragment(included.title) in response.text
    assert safe_fragment(excluded.title) not in response.text
    assert "Listings tagged" in response.text
    assert "Show all" in response.text


def test_tag_badges_link_to_filter(client):
    html = client.get("/listings").text
    assert re.search(r"href=[\"']/listings\?tag=", html)


# Phase 3 — post a listing


def test_new_listing_form(client):
    response = client.get("/listings/new")
    assert response.status_code == 200
    html = response.text
    assert re.search(r"<form[^>]*method=[\"']post[\"']", html, re.IGNORECASE)
    for field_name in ["title", "human_name", "description", "tags"]:
        assert re.search(rf"name=[\"']{field_name}[\"']", html)
    assert "<textarea" in html
    # the listings page links to the form
    assert re.search(r"href=[\"']/listings/new[\"']", client.get("/listings").text)


def test_post_listing_round_trip_and_tag_parsing(client, impl):
    models = impl["models"]
    expected_id = models.new_listing_id()
    response = client.post(
        "/listings",
        data={
            "title": "Acceptance Human Wanted",
            "human_name": "Pat",
            "description": "Reads every line of output before replying.",
            "tags": "python, remote , ",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    location = urlsplit(response.headers["location"]).path
    assert location == f"/listings/{expected_id}"
    created = models.get_listing(expected_id)
    assert created is not None
    assert created.tags == ["python", "remote"]
    page = client.get(location).text
    assert "Acceptance Human Wanted" in page
    assert "Reads every line of output before replying." in page


def test_post_listing_validation_rerenders_with_422(client, impl):
    models = impl["models"]
    before = len(models.listings)
    response = client.post(
        "/listings",
        data={
            "title": "   ",
            "human_name": "Pat",
            "description": "This text must be preserved on re-render.",
            "tags": "",
        },
        follow_redirects=False,
    )
    assert response.status_code == 422
    assert "is-invalid" in response.text
    assert "This text must be preserved on re-render." in response.text
    assert len(models.listings) == before
