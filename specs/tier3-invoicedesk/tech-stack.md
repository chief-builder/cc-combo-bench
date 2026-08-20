# Tech Stack

| Layer | Choice | Version | Notes |
|-------|--------|---------|-------|
| Language | Python 3 | — | Managed with requirements.txt |
| Web framework | fastapi[standard] | 0.115.10 | ASGI, type-driven |
| Server | Uvicorn | | ASGI server, run via `main.py` |
| Templates | Jinja2 | | Bundled with FastAPI/Starlette |
| CSS | Bootstrap 5 | | CDN link, no npm/build step |
| Data model | `dataclasses.dataclass` | | Invoice: `id`, `client`, `description`, `amount`, `status`, `created_at`; Payment: `invoice_id`, `amount`, `note`, `paid_at` |
| Storage | In-memory `list`s | | Module-level, no database |
| API | Plain FastAPI JSON routes | | `/api/...` returning lists of dicts, datetimes as ISO 8601 |
| Testing | pytest + `TestClient` | 8.3.4 | `starlette.testclient.TestClient`, no running server needed |

No dependencies beyond tier 1 — same `requirements.txt`.

When running Python: you **must** use the virtual environment.
