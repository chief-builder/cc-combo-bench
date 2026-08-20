# Sub-agent — implement all phases

Used by combos 1, 4, 5 (spawned from kickoff-single.md). Contains no model
reference, so it is byte-identical across sub-agent models.

---

Implement the app specified in {{WORKTREE}}/{{SPEC_DIR}}/. Work only
inside {{WORKTREE}} — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then implement
ALL phases of the roadmap exactly as written — file names, routes, status
codes, defaults, CDN links, and template contents are requirements, not
suggestions.

- Use the virtual environment at {{MAIN_REPO}}/.venv for everything you
  run.
- Write the tests the roadmap calls for and run them with
  `cd {{WORKTREE}} && {{MAIN_REPO}}/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
