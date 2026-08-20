# Sub-agent — implement one later phase (specs with 3+ phases)

Used by kickoff-per-phase-multi.md for every phase after Phase 1.
{{PHASE}} = the phase number to implement; {{PREV_PHASE}} = the highest
phase already implemented ({{PHASE}} - 1). Tier-1 runs keep using
subagent-phase2.md unchanged for round-to-round comparability. Contains
no model reference, so it is byte-identical across sub-agent models.

---

The roadmap through Phase {{PREV_PHASE}} of the app specified in
{{WORKTREE}}/{{SPEC_DIR}}/ is already implemented in {{WORKTREE}}. Work
only inside {{WORKTREE}} — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase {{PHASE}} of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase {{PHASE}} requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at {{MAIN_REPO}}/.venv for everything you
  run.
- Write the tests Phase {{PHASE}} calls for and run the full suite with
  `cd {{WORKTREE}} && {{MAIN_REPO}}/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
