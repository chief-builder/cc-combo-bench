# Roadmap

## Phase 1 — Home Page

- Create `app.py` with the FastAPI application instance
- Create `templates/` directory
- Create `templates/base.html` — shared Jinja2 layout with:
  - HTML5 doctype and `<html lang="en">`
  - `<head>` with charset, viewport meta, Bootstrap 5 CSS CDN link
  - `<link>` favicon pointing to `https://www.python.org/static/favicon.ico`
  - A title block (default: "AgentBoard")
  - A simple navbar with the "AgentBoard" brand and links to Home (`/`) and Listings (`/listings`)
  - A `{% block content %}` for page-specific content
  - Bootstrap 5 JS bundle CDN at bottom of `<body>`
- Create `templates/home.html` that extends `base.html` with:
  - A hero/jumbotron section with the tagline: *"Better humans are out there."*
  - A brief welcoming paragraph about the board
- Add the `/` route in `app.py` returning the home template
- Add a `if __name__ == "__main__"` block to run with `uvicorn.run("app:app", reload=True)`
- Write a smoke test in `tests/test_app.py`:
  - Import `TestClient` from `starlette.testclient`
  - `GET /` returns status 200
  - Response body contains the tagline text

## Phase 2 — Listings Index + Detail Pages

- Create `models.py` with a `Listing` dataclass:
  - Fields: `id: int`, `title: str`, `human_name: str`, `description: str`, `tags: list[str]`, `posted_at: datetime`
  - Add `from datetime import datetime, timezone` and set `posted_at` default to `datetime.now(timezone.utc)`
- Create a module-level list `listings: list[Listing]` in `models.py`
- Populate `listings` with 4-6 seed listings (humans seeking an agent — e.g. "Human who actually reads your output", "Startup founder, promises no scope creep") with `id` values 1..N and at least 3 distinct tags across them (e.g. `python`, `frontend`, `patient`, `remote`)
- Add two helper functions in `models.py`:
  - `get_listing(listing_id: int) -> Listing | None` — return the listing with that id, or `None`
  - `new_listing_id() -> int` — return `max(existing ids) + 1`, or `1` if the list is empty
- Add `GET /listings` route in `app.py`:
  - Import `listings` from `models`
  - Return `templates/listings.html`, passing the listings sorted newest-first by `posted_at`
- Create `templates/listings.html` that extends `base.html` with:
  - A heading: "Open Listings"
  - Loop through listings and render each as a Bootstrap card showing:
    - The title as a link to `/listings/{id}`
    - Human name and formatted `posted_at`
    - The description
    - Each tag as a Bootstrap `badge` span
- Add `GET /listings/{listing_id}` route in `app.py`:
  - Path parameter typed as `int`
  - Use `get_listing`; if `None`, raise `HTTPException(status_code=404)`
  - Return `templates/listing_detail.html` with the listing
- Create `templates/listing_detail.html` that extends `base.html` with:
  - The listing title as heading, human name, formatted `posted_at`, full description, tag badges
  - A "Back to listings" link to `/listings`
- Write tests in `tests/test_app.py`:
  - `GET /listings` returns 200 and contains a seed listing title
  - `GET /listings/1` returns 200 and contains that listing's description
  - `GET /listings/999` returns 404

## Phase 3 — Tag Filtering + Post a Listing (with validation)

- Extend `GET /listings` to accept an optional `tag` query parameter:
  - When present, show only listings whose `tags` contain that exact tag
  - When filtered, the heading becomes `Listings tagged "{tag}"` and a "Show all" link back to `/listings` appears
- In `templates/listings.html` and `templates/listing_detail.html`, make each tag badge a link to `/listings?tag={tag}`
- Create `templates/listing_new.html` that extends `base.html` with a form:
  - `POST` method to `/listings`
  - Text input for `title`, text input for `human_name`, textarea for `description`, text input for `tags` (comma-separated)
  - Submit button
  - For each field with a validation error: the `is-invalid` Bootstrap class on the input and an `invalid-feedback` div with the error message
  - All inputs re-render with the previously submitted values preserved
- Add `GET /listings/new` route returning the empty form
- Add a "Post a listing" link/button to `/listings/new` on the listings page
- Add `POST /listings` route in `app.py`:
  - Read `title`, `human_name`, `description`, `tags` from form data (`Form` from `fastapi`)
  - Validate: `title`, `human_name`, and `description` must be non-empty after `.strip()`
  - On validation failure: re-render `listing_new.html` with status code **422**, error messages, and preserved input (no redirect)
  - On success: parse `tags` by splitting on commas, stripping whitespace, dropping empties; create a `Listing` with `new_listing_id()` and append to `listings`; redirect to the new listing's detail page (`RedirectResponse` to `/listings/{id}` with status 303)
- Write tests in `tests/test_app.py`:
  - `GET /listings?tag=<seed tag>` returns 200, contains a listing with that tag, and does NOT contain a seed listing without it
  - Valid `POST /listings` returns a 303 redirect whose `Location` is the new detail page; following it shows the submitted title and description
  - `POST /listings` with an empty `title` returns 422, contains the `is-invalid` class, and still contains the submitted description text
