# Roadmap

## Phase 1 — Home Page

- Create `app.py` with the FastAPI application instance
- Create `templates/` directory
- Create `templates/base.html` — shared Jinja2 layout with:
  - HTML5 doctype and `<html lang="en">`
  - `<head>` with charset, viewport meta, Bootstrap 5 CSS CDN link
  - `<link>` favicon pointing to `https://www.python.org/static/favicon.ico`
  - A title block (default: "InvoiceDesk")
  - A simple navbar with the "InvoiceDesk" brand and links to Home (`/`), Invoices (`/invoices`), and Stats (`/stats`)
  - A `{% block content %}` for page-specific content
  - Bootstrap 5 JS bundle CDN at bottom of `<body>`
- Create `templates/home.html` that extends `base.html` with:
  - A hero/jumbotron section with the tagline: *"Bill it. Send it. Get paid."*
  - A brief welcoming paragraph about the tracker
- Add the `/` route in `app.py` returning the home template
- Add a `if __name__ == "__main__"` block to run with `uvicorn.run("app:app", reload=True)`
- Write a smoke test in `tests/test_app.py`:
  - Import `TestClient` from `starlette.testclient`
  - `GET /` returns status 200
  - Response body contains the tagline text

## Phase 2 — Invoice Board + Detail Pages

- Create `models.py` with:
  - An `Invoice` dataclass — fields: `id: int`, `client: str`, `description: str`, `amount: float`, `status: str` (default `"draft"`), `created_at: datetime` (default `datetime.now(timezone.utc)`; import from `datetime`)
  - A `Payment` dataclass — fields: `invoice_id: int`, `amount: float`, `note: str`, `paid_at: datetime` (same default)
  - A module-level constant `STATUSES = ["draft", "sent", "paid"]`
  - A module-level constant `ALLOWED_TRANSITIONS = {"draft": ["sent"], "sent": ["paid"], "paid": []}`
  - Module-level lists `invoices: list[Invoice]` and `payments: list[Payment]`
  - Helper functions:
    - `get_invoice(invoice_id: int) -> Invoice | None`
    - `payments_for(invoice_id: int) -> list[Payment]`
    - `paid_total(invoice_id: int) -> float` — the sum of that invoice's payment amounts, rounded to 2 decimals
    - `new_invoice_id() -> int` — `max(existing ids) + 1`, or `1` if empty
- Populate seed data: 5 invoices with `id` 1..5 covering **all three statuses**, realistic cent amounts, and 4-6 payments spread across at least 2 invoices — seed data must be consistent with the rules below (every `paid` seed invoice's payments sum to at least its amount; payments exist only on `sent` or `paid` invoices)
- Add `GET /invoices` route in `app.py`:
  - Optional `status` query parameter; when present and in `STATUSES`, show only invoices with that status; when present but NOT in `STATUSES`, raise `HTTPException(status_code=400)`
  - Return `templates/invoices.html`, invoices sorted newest-first by `created_at`
- Create `templates/invoices.html` that extends `base.html` with:
  - A heading: "Invoices"
  - Filter links: "All" to `/invoices` plus one per status to `/invoices?status={status}`
  - Loop through invoices and render each as a Bootstrap card showing:
    - The client name as a link to `/invoices/{id}`
    - The description and formatted `created_at`
    - The amount formatted as `$X.XX`
    - A status badge, colored by status: `draft` → `text-bg-secondary`, `sent` → `text-bg-warning`, `paid` → `text-bg-success`
    - A line `$P.PP of $A.AA paid` using `paid_total` and the amount, both two decimals
- Add `GET /invoices/{invoice_id}` route in `app.py`:
  - Path parameter typed as `int`; unknown id → `HTTPException(status_code=404)`
  - Return `templates/invoice_detail.html` with the invoice and its payments
- Create `templates/invoice_detail.html` that extends `base.html` with:
  - Client as heading, status badge (same color mapping), description, formatted `created_at`, the amount as `$X.XX`
  - A line reading exactly `Balance due: $X.XX` — the amount minus `paid_total`, two decimals
  - A payments section listing each payment's note, formatted `paid_at`, and amount as `$X.XX`
  - A "Back to invoices" link to `/invoices`
- Write tests in `tests/test_app.py`:
  - `GET /invoices` returns 200 and contains a seed client name
  - `GET /invoices?status=draft` contains a draft seed invoice and does NOT contain a paid one
  - `GET /invoices?status=bogus` returns 400
  - A seed invoice detail page returns 200, contains a seed payment's note, and shows the correct `Balance due: $X.XX`
  - `GET /invoices/999` returns 404

## Phase 3 — Create Invoices, Record Payments, Work the Lifecycle

- Create `templates/invoice_new.html` that extends `base.html` with a form:
  - `POST` method to `/invoices`
  - Text input for `client`, textarea for `description`, text input for `amount`, submit button
  - For each field with a validation error: the `is-invalid` Bootstrap class and an `invalid-feedback` div with the message; all inputs re-render with submitted values preserved (including the raw amount text)
- Add `GET /invoices/new` route returning the empty form, and a "New invoice" button linking to it from the invoice board
- Add `POST /invoices` route in `app.py`:
  - Read `client`, `description`, `amount` from form data (`Form` from `fastapi`), all as strings
  - Validate: `client` and `description` non-empty after `.strip()`; `amount` must parse as a **finite** number and be strictly greater than 0 (reject `nan`/`inf`/`-inf` — check with `math.isfinite`)
  - On failure: re-render `invoice_new.html` with status code **422**, errors, preserved input (no redirect)
  - On success: round the amount to 2 decimals, create an `Invoice` with `new_invoice_id()` and status `"draft"`, append, redirect to `/invoices/{id}` (`RedirectResponse`, status 303)
- Add a payment form on `templates/invoice_detail.html`:
  - `POST` method to `/invoices/{id}/payments`; text input for `note`, text input for `amount`, submit button
- Add `POST /invoices/{invoice_id}/payments` route:
  - Unknown invoice → 404
  - If the invoice's status is not `"sent"`, raise `HTTPException(status_code=400, detail=f"Cannot record a payment on a {status} invoice")`
  - Validate `amount` parses as a **finite** number (reject `nan`/`inf`/`-inf` via `math.isfinite`) and is strictly greater than 0; on failure re-render the detail template with status **422**, the error, and preserved input (`note` is optional and may be empty)
  - On success: round to 2 decimals, append a `Payment`, redirect to `/invoices/{id}` (status 303)
- Add the lifecycle to the detail page:
  - For each status in `ALLOWED_TRANSITIONS[invoice.status]`, render a form button that `POST`s to `/invoices/{id}/status` with hidden input `new_status` (label: "Send invoice" for `sent`, "Mark paid" for `paid`)
  - A paid invoice shows no transition button
- Add `POST /invoices/{invoice_id}/status` route:
  - Read `new_status` from form data; unknown invoice → 404
  - If `new_status` is not in `ALLOWED_TRANSITIONS[invoice.status]`, raise `HTTPException(status_code=400, detail=f"Cannot move invoice from {invoice.status} to {new_status}")`
  - Additionally, moving `sent → paid` requires `paid_total(id) >= amount`; otherwise raise `HTTPException(status_code=400, detail=f"Cannot mark invoice paid: ${paid:.2f} of ${amount:.2f} paid")`
  - On success: update `invoice.status`, redirect to `/invoices/{id}` (status 303)
- Write tests in `tests/test_app.py`:
  - Valid `POST /invoices` returns 303 to the new detail page; following it shows the submitted client with a `draft` status badge
  - `POST /invoices` with empty `client` returns 422 and still contains the submitted description
  - `POST /invoices` with non-numeric `amount` returns 422 and preserves the raw amount text
  - `POST /invoices/{draft id}/payments` returns 400 (payments only on sent invoices)
  - `POST /invoices/999/payments` returns 404
  - Valid transition: `POST /invoices/{draft id}/status` with `new_status=sent` returns 303; detail then shows the `sent` badge
  - Invalid transitions return 400: `draft → paid` (skipping a step) and any transition on a `paid` invoice
  - Recording a valid payment on a sent invoice returns 303; the detail page then shows the payment note and the reduced `Balance due: $X.XX`
  - `POST /invoices/{sent id}/payments` with `amount` of `0` returns 422
  - `POST /invoices` with `amount` of `nan` returns 422, and `POST /invoices/{sent id}/payments` with `amount` of `inf` returns 422 (both parse via `float()`; only an `isfinite` check catches them)
  - `POST /invoices/{sent id}/status` with `new_status=paid` while payments total less than the amount returns 400; after payments cover the amount, the same request returns 303 and the detail shows the `paid` badge

## Phase 4 — Stats Page + JSON API

- Add `GET /stats` route in `app.py` and `templates/stats.html` extending `base.html`:
  - A heading: "Billing Stats"
  - A Bootstrap card per status showing the count of invoices in that status (all three statuses shown, including zero counts)
  - A line `Total invoiced: $X.XX` — the sum of all invoice amounts, two decimals
  - A line `Total collected: $X.XX` — the sum of all payment amounts, two decimals
  - A line `Outstanding: $X.XX` — total invoiced minus total collected, two decimals
- Add `GET /api/invoices` route in `app.py`:
  - Returns JSON: a list with one object per invoice, fields `id`, `client`, `description`, `amount`, `status`, `created_at` (ISO 8601 string via `.isoformat()`), and `paid_total`
  - Sorted by `id` ascending
- Write tests in `tests/test_app.py`:
  - `GET /stats` returns 200 and contains the correctly computed `Total invoiced`, `Total collected`, and `Outstanding` dollar lines
  - `GET /api/invoices` returns 200 with a JSON content type; the list length matches `len(invoices)`; the object for invoice 1 has all seven fields and the correct `paid_total`; `created_at` parses with `datetime.fromisoformat`
