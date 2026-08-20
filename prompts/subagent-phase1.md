# Sub-agent — implement Phase 1 only

Used by combos 2, 3, 6 (spawned from kickoff-per-phase.md). Contains no
model reference, so it is byte-identical across sub-agent models.

---

Implement Phase 1 of the app specified in {{WORKTREE}}/{{SPEC_DIR}}/.
Work only inside {{WORKTREE}} — create every file there, never in any
other directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 1 of the roadmap exactly as written — file names, routes,
status codes, defaults, CDN links, and template contents are requirements,
not suggestions. Do not start any later phase.

- Use the virtual environment at {{MAIN_REPO}}/.venv for everything you
  run.
- Write the tests Phase 1 calls for and run them with
  `cd {{WORKTREE}} && {{MAIN_REPO}}/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
