# Tech Stack

| Layer | Choice | Version | Notes |
|-------|--------|---------|-------|
| Language | Python 3 | — | Managed with requirements.txt |
| Web framework | fastapi[standard] | 0.115.10 | ASGI, type-driven |
| Server | Uvicorn | | ASGI server, run via `main.py` |
| Templates | Jinja2 | | Bundled with FastAPI/Starlette |
| CSS | Bootstrap 5 | | CDN link, no npm/build step |
| Data model | `dataclasses.dataclass` | | Expense: `id`, `title`, `payee`, `amount`, `category`, `notes`, `spent_at` |
| Storage | In-memory `list` | | Module-level, no database |
| Testing | pytest + `TestClient` | 8.3.4 | `starlette.testclient.TestClient`, no running server needed |

No dependencies beyond tier 1 — same `requirements.txt`.

When running Python: you **must** use the virtual environment.
