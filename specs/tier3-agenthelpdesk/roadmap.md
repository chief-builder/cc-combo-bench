# Roadmap

## Phase 1 — Home Page

- Create `app.py` with the FastAPI application instance
- Create `templates/` directory
- Create `templates/base.html` — shared Jinja2 layout with:
  - HTML5 doctype and `<html lang="en">`
  - `<head>` with charset, viewport meta, Bootstrap 5 CSS CDN link
  - `<link>` favicon pointing to `https://www.python.org/static/favicon.ico`
  - A title block (default: "AgentHelpdesk")
  - A simple navbar with the "AgentHelpdesk" brand and links to Home (`/`), Tickets (`/tickets`), and Stats (`/stats`)
  - A `{% block content %}` for page-specific content
  - Bootstrap 5 JS bundle CDN at bottom of `<body>`
- Create `templates/home.html` that extends `base.html` with:
  - A hero/jumbotron section with the tagline: *"File a ticket. A mediator agent will be with you shortly."*
  - A brief welcoming paragraph about the helpdesk
- Add the `/` route in `app.py` returning the home template
- Add a `if __name__ == "__main__"` block to run with `uvicorn.run("app:app", reload=True)`
- Write a smoke test in `tests/test_app.py`:
  - Import `TestClient` from `starlette.testclient`
  - `GET /` returns status 200
  - Response body contains the tagline text

## Phase 2 — Ticket Board + Detail Pages

- Create `models.py` with:
  - A `Ticket` dataclass — fields: `id: int`, `title: str`, `agent_name: str`, `description: str`, `status: str` (default `"open"`), `created_at: datetime` (default `datetime.now(timezone.utc)`; import from `datetime`)
  - A `Comment` dataclass — fields: `ticket_id: int`, `author: str`, `text: str`, `created_at: datetime` (same default)
  - A module-level constant `STATUSES = ["open", "in_progress", "resolved"]`
  - A module-level constant `ALLOWED_TRANSITIONS = {"open": ["in_progress"], "in_progress": ["resolved"], "resolved": []}`
  - Module-level lists `tickets: list[Ticket]` and `comments: list[Comment]`
  - Helper functions:
    - `get_ticket(ticket_id: int) -> Ticket | None`
    - `comments_for(ticket_id: int) -> list[Comment]`
    - `new_ticket_id() -> int` — `max(existing ids) + 1`, or `1` if empty
- Populate seed data: 5 tickets with `id` 1..5 covering **all three statuses** (gripes like "Human keeps saying 'just one small change'", "Asked to be concise AND thorough"), and 4-6 comments spread across at least 2 tickets
- Add `GET /tickets` route in `app.py`:
  - Optional `status` query parameter; when present and in `STATUSES`, show only tickets with that status; when present but NOT in `STATUSES`, raise `HTTPException(status_code=400)`
  - Return `templates/tickets.html`, tickets sorted newest-first by `created_at`
- Create `templates/tickets.html` that extends `base.html` with:
  - A heading: "Ticket Board"
  - Filter links: "All" to `/tickets` plus one per status to `/tickets?status={status}`
  - Loop through tickets and render each as a Bootstrap card showing:
    - The title as a link to `/tickets/{id}`
    - Agent name and formatted `created_at`
    - A status badge, colored by status: `open` → `text-bg-primary`, `in_progress` → `text-bg-warning`, `resolved` → `text-bg-success`
    - The comment count (via `comments_for`)
- Add `GET /tickets/{ticket_id}` route in `app.py`:
  - Path parameter typed as `int`; unknown id → `HTTPException(status_code=404)`
  - Return `templates/ticket_detail.html` with the ticket and its comments
- Create `templates/ticket_detail.html` that extends `base.html` with:
  - Title as heading, status badge (same color mapping), agent name, formatted `created_at`, full description
  - A comments section listing each comment's author, formatted `created_at`, and text
  - A "Back to board" link to `/tickets`
- Write tests in `tests/test_app.py`:
  - `GET /tickets` returns 200 and contains a seed ticket title
  - `GET /tickets?status=open` contains an open seed ticket and does NOT contain a resolved one
  - `GET /tickets?status=bogus` returns 400
  - `GET /tickets/1` returns 200 and contains a seed comment's text
  - `GET /tickets/999` returns 404

## Phase 3 — Open Tickets, Comment, Work the Status Flow

- Create `templates/ticket_new.html` that extends `base.html` with a form:
  - `POST` method to `/tickets`
  - Text input for `title`, text input for `agent_name`, textarea for `description`, submit button
  - For each field with a validation error: the `is-invalid` Bootstrap class and an `invalid-feedback` div with the message; all inputs re-render with submitted values preserved
- Add `GET /tickets/new` route returning the empty form, and a "File a ticket" button linking to it from the ticket board
- Add `POST /tickets` route in `app.py`:
  - Read `title`, `agent_name`, `description` from form data (`Form` from `fastapi`)
  - Validate: all three non-empty after `.strip()`
  - On failure: re-render `ticket_new.html` with status code **422**, errors, preserved input (no redirect)
  - On success: create a `Ticket` with `new_ticket_id()` and status `"open"`, append, redirect to `/tickets/{id}` (`RedirectResponse`, status 303)
- Add a comment form at the bottom of `templates/ticket_detail.html`:
  - `POST` method to `/tickets/{id}/comments`; text input for `author`, textarea for `text`, submit button
- Add `POST /tickets/{ticket_id}/comments` route:
  - Unknown ticket → 404
  - Validate `author` and `text` non-empty after `.strip()`; on failure re-render the detail template with status **422**, errors, and preserved input
  - On success: append a `Comment`, redirect to `/tickets/{id}` (status 303)
- Add the status workflow to the detail page:
  - For each status in `ALLOWED_TRANSITIONS[ticket.status]`, render a form button that `POST`s to `/tickets/{id}/status` with hidden input `new_status` (label: "Start work" for `in_progress`, "Resolve" for `resolved`)
  - A resolved ticket shows no transition button
- Add `POST /tickets/{ticket_id}/status` route:
  - Read `new_status` from form data; unknown ticket → 404
  - If `new_status` is not in `ALLOWED_TRANSITIONS[ticket.status]`, raise `HTTPException(status_code=400, detail=f"Cannot move ticket from {ticket.status} to {new_status}")`
  - On success: update `ticket.status`, redirect to `/tickets/{id}` (status 303)
- Write tests in `tests/test_app.py`:
  - Valid `POST /tickets` returns 303 to the new detail page; following it shows the submitted title with an `open` status badge
  - `POST /tickets` with empty `title` returns 422 and still contains the submitted description
  - `POST /tickets/{id}/comments` returns 303; the detail page then contains the new comment text
  - `POST /tickets/{id}/comments` with empty `author` or `text` returns 422 and still contains the submitted input
  - `POST /tickets/999/comments` returns 404
  - Valid transition: `POST /tickets/{open id}/status` with `new_status=in_progress` returns 303; detail then shows the `in_progress` badge
  - Invalid transitions return 400: `open → resolved` (skipping a step) and any transition on a `resolved` ticket

## Phase 4 — Stats Page + JSON API

- Add `GET /stats` route in `app.py` and `templates/stats.html` extending `base.html`:
  - A heading: "Helpdesk Stats"
  - A Bootstrap card per status showing the count of tickets in that status (all three statuses shown, including zero counts)
  - Total ticket count
  - Average comments per ticket, computed as `len(comments) / len(tickets)` rounded to 1 decimal place (`0` if there are no tickets)
- Add `GET /api/tickets` route in `app.py`:
  - Returns JSON: a list with one object per ticket, fields `id`, `title`, `agent_name`, `status`, `created_at` (ISO 8601 string via `.isoformat()`), and `comment_count`
  - Sorted by `id` ascending
- Write tests in `tests/test_app.py`:
  - `GET /stats` returns 200 and contains the per-status counts computed from the current data
  - `GET /api/tickets` returns 200 with a JSON content type; the list length matches `len(tickets)`; the object for ticket 1 has the correct `comment_count` and all six fields; `created_at` parses with `datetime.fromisoformat`
