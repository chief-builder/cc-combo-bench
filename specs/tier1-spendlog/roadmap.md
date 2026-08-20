# Roadmap

## Phase 1 — Home Page

- Create `app.py` with the FastAPI application instance
- Create `templates/` directory
- Create `templates/base.html` — shared Jinja2 layout with:
  - HTML5 doctype and `<html lang="en">`
  - `<head>` with charset, viewport meta, Bootstrap 5 CSS CDN link
  - `<link>` favicon pointing to `https://www.python.org/static/favicon.ico`
  - A title block (default: "SpendLog")
  - A simple navbar with the "SpendLog" brand and links to Home (`/`) and Journal (`/entries`)
  - A `{% block content %}` for page-specific content
  - Bootstrap 5 JS bundle CDN at bottom of `<body>`
- Create `templates/home.html` that extends `base.html` with:
  - A hero/jumbotron section with the tagline: *"Every penny, written down."*
  - A brief welcoming paragraph about the journal
- Add the `/` route in `app.py` returning the home template
- Add a `if __name__ == "__main__"` block to run with `uvicorn.run("app:app", reload=True)`
- Write a smoke test in `tests/test_app.py`:
  - Import `TestClient` from `starlette.testclient`
  - `GET /` returns status 200
  - Response body contains the tagline text

## Phase 2 — Spending Journal

- Create `models.py` with an `Entry` dataclass:
  - Fields: `description: str`, `amount: float`, `timestamp: datetime`
  - Add `from datetime import datetime, timezone` and set `timestamp` default to `datetime.now(timezone.utc)`
- Create a module-level list `entries: list[Entry]` in `models.py`
- Populate `entries` with 3-5 seed entries (everyday purchases like coffee, groceries, a bus ticket) with realistic cent amounts (e.g. 4.50, 23.87)
- Add `GET /entries` route in `app.py`:
  - Import `entries` from `models`
  - Compute `total` as the sum of all entry amounts, rounded to 2 decimals
  - Return `templates/entries.html` passing the entries list and the total as context
- Create `templates/entries.html` that extends `base.html` with:
  - A heading: "Spending Journal"
  - A line reading exactly `Total spent: $X.XX` where X.XX is the total formatted with two decimal places (e.g. `Total spent: $52.31`)
  - Loop through entries and render each as a Bootstrap card showing the description, the amount formatted as `$X.XX` (two decimal places), and the timestamp (formatted)
  - A form at the bottom with:
    - `POST` method to `/entries`
    - Text input for the description
    - Input for the amount
    - Submit button
- Add `POST /entries` route in `app.py`:
  - Read `description` (str) and `amount` (float) from form data (`Form` from `fastapi`)
  - Create a new `Entry` and append to the `entries` list
  - Redirect to `GET /entries` (use `RedirectResponse` with status 303)
- Write tests in `tests/test_app.py`:
  - `GET /entries` returns 200, contains a seed entry's description, and contains the correctly computed `Total spent: $X.XX` line
  - `POST /entries` with a description and amount redirects to `/entries` with status 303 (assert the 303 directly)
  - After `POST /entries`, `GET /entries` includes the newly added description and the updated total
