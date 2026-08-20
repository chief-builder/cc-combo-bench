# Roadmap

## Phase 1 — Home Page

- Create `app.py` with the FastAPI application instance
- Create `templates/` directory
- Create `templates/base.html` — shared Jinja2 layout with:
  - HTML5 doctype and `<html lang="en">`
  - `<head>` with charset, viewport meta, Bootstrap 5 CSS CDN link
  - `<link>` favicon pointing to `https://www.python.org/static/favicon.ico`
  - A title block (default: "ExpenseHub")
  - A simple navbar with the "ExpenseHub" brand and links to Home (`/`) and Expenses (`/expenses`)
  - A `{% block content %}` for page-specific content
  - Bootstrap 5 JS bundle CDN at bottom of `<body>`
- Create `templates/home.html` that extends `base.html` with:
  - A hero/jumbotron section with the tagline: *"Know where it all goes."*
  - A brief welcoming paragraph about the app
- Add the `/` route in `app.py` returning the home template
- Add a `if __name__ == "__main__"` block to run with `uvicorn.run("app:app", reload=True)`
- Write a smoke test in `tests/test_app.py`:
  - Import `TestClient` from `starlette.testclient`
  - `GET /` returns status 200
  - Response body contains the tagline text

## Phase 2 — Expense List + Detail Pages

- Create `models.py` with an `Expense` dataclass:
  - Fields: `id: int`, `title: str`, `payee: str`, `amount: float`, `category: str`, `notes: str`, `spent_at: datetime`
  - Add `from datetime import datetime, timezone` and set `spent_at` default to `datetime.now(timezone.utc)`
- Create a module-level list `expenses: list[Expense]` in `models.py`
- Populate `expenses` with 4-6 seed expenses (groceries, transport, coffee, software, etc.) with `id` values 1..N, realistic cent amounts, and at least 3 distinct categories across them (e.g. `food`, `transport`, `software`)
- Add two helper functions in `models.py`:
  - `get_expense(expense_id: int) -> Expense | None` — return the expense with that id, or `None`
  - `new_expense_id() -> int` — return `max(existing ids) + 1`, or `1` if the list is empty
- Add `GET /expenses` route in `app.py`:
  - Import `expenses` from `models`
  - Return `templates/expenses.html`, passing the expenses sorted newest-first by `spent_at`, plus the total of the amounts of the expenses being shown, rounded to 2 decimals
- Create `templates/expenses.html` that extends `base.html` with:
  - A heading: "All Expenses"
  - A line reading exactly `Total: $X.XX` — the total of the expenses currently shown, formatted with two decimal places
  - Loop through expenses and render each as a Bootstrap card showing:
    - The title as a link to `/expenses/{id}`
    - Payee and formatted `spent_at`
    - The amount formatted as `$X.XX` (two decimal places)
    - The category as a Bootstrap `badge`
- Add `GET /expenses/{expense_id}` route in `app.py`:
  - Path parameter typed as `int`
  - Use `get_expense`; if `None`, raise `HTTPException(status_code=404)`
  - Return `templates/expense_detail.html` with the expense
- Create `templates/expense_detail.html` that extends `base.html` with:
  - The expense title as heading, payee, formatted `spent_at`, the amount as `$X.XX`, the category badge, and the notes
  - A "Back to expenses" link to `/expenses`
- Write tests in `tests/test_app.py`:
  - `GET /expenses` returns 200, contains a seed expense title, and contains the correctly computed `Total: $X.XX` line
  - `GET /expenses/1` returns 200 and contains that expense's notes
  - `GET /expenses/999` returns 404

## Phase 3 — Category Filtering + Add an Expense (with money validation)

- Extend `GET /expenses` to accept an optional `category` query parameter:
  - When present, show only expenses whose `category` equals it exactly, and compute the `Total: $X.XX` line from only the expenses shown
  - When filtered, the heading becomes `Expenses in "{category}"` and a "Show all" link back to `/expenses` appears
- In `templates/expenses.html` and `templates/expense_detail.html`, make each category badge a link to `/expenses?category={category}`
- Create `templates/expense_new.html` that extends `base.html` with a form:
  - `POST` method to `/expenses`
  - Text input for `title`, text input for `payee`, text input for `amount`, text input for `category`, textarea for `notes`
  - Submit button
  - For each field with a validation error: the `is-invalid` Bootstrap class on the input and an `invalid-feedback` div with the error message
  - All inputs re-render with the previously submitted values preserved (including the raw amount text exactly as typed)
- Add `GET /expenses/new` route returning the empty form
- Add an "Add expense" link/button to `/expenses/new` on the expenses page
- Add `POST /expenses` route in `app.py`:
  - Read `title`, `payee`, `amount`, `category`, `notes` from form data (`Form` from `fastapi`), all as strings
  - Validate: `title`, `payee`, and `category` must be non-empty after `.strip()`; `amount` must parse as a number and be strictly greater than 0 (reject non-numeric text, zero, and negatives)
  - On validation failure: re-render `expense_new.html` with status code **422**, error messages, and preserved input (no redirect)
  - On success: round the amount to 2 decimals, create an `Expense` with `new_expense_id()`, append to `expenses`, and redirect to the new expense's detail page (`RedirectResponse` to `/expenses/{id}` with status 303)
  - `notes` is optional and may be empty
- Write tests in `tests/test_app.py`:
  - `GET /expenses?category=<seed category>` returns 200, contains a seed expense with that category, does NOT contain a seed expense of a different category, and shows the `Total: $X.XX` of only the filtered expenses
  - Valid `POST /expenses` returns a 303 redirect whose `Location` is the new detail page; following it shows the submitted title and the amount formatted as `$X.XX`
  - `POST /expenses` with an empty `title` returns 422, contains the `is-invalid` class, and still contains the submitted notes text
  - `POST /expenses` with `amount` set to non-numeric text (e.g. `abc`) returns 422 and preserves the raw amount text
  - `POST /expenses` with a negative `amount` returns 422
