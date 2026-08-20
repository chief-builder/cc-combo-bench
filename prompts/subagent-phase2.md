# Sub-agent — implement Phase 2 only

Used by combos 2, 3, 6 (spawned from kickoff-per-phase.md). Contains no
model reference, so it is byte-identical across sub-agent models.

---

Phase 1 of the app specified in {{WORKTREE}}/{{SPEC_DIR}}/ is already
implemented in {{WORKTREE}}. Work only inside {{WORKTREE}} — create
every file there, never in any other directory. Read mission.md,
tech-stack.md, and
roadmap.md, then implement Phase 2 of the roadmap exactly as written —
file names, routes, status codes, defaults, CDN links, and template
contents are requirements, not suggestions. Modify existing files only
where Phase 2 requires it (e.g. new routes in app.py, new tests in
tests/test_app.py); leave the rest of the Phase 1 code as you found it,
even if you disagree with it.

- Use the virtual environment at {{MAIN_REPO}}/.venv for everything you
  run.
- Write the tests Phase 2 calls for and run the full suite with
  `cd {{WORKTREE}} && {{MAIN_REPO}}/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
