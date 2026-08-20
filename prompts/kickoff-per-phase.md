# Kickoff — one sub-agent per phase

Used by combos 2, 3, 6. Fill placeholders per README.md before use.

---

You are the main agent in a benchmark run. Your working directory is
{{WORKTREE}}, a clean worktree of the benchmark repo. The app to build is
specified in {{SPEC_DIR}}/ (mission.md, tech-stack.md, roadmap.md).

You orchestrate; you never implement. Do not write or edit implementation
code or tests yourself, and do not fix any problem you find — your role is
to delegate, verify, and report.

1. Spawn one sub-agent to implement Phase 1 of the roadmap. Build its
   prompt from {{MAIN_REPO}}/prompts/subagent-phase1.md: take the part
   below its `---` line, fill the placeholders the same way as this
   prompt, and save it to a unique temp file created with `mktemp` —
   never a fixed or shared path; parallel benchmark runs collide on
   shared scratch files. Pass it verbatim — do not reword, add, or
   remove anything. Spawn by running exactly this command in the
   FOREGROUND with an explicit long timeout (600000 ms) — it can take
   ten minutes; never background it and never rely on monitors or
   completion notifications, which do not survive in this environment:

   `cd {{WORKTREE}} && claude -p --model {{SUBAGENT_MODEL}} --permission-mode acceptEdits --allowedTools "Bash" --output-format text < <the temp file>`

   Capture its stdout; that is the sub-agent's report. Start it exactly
   once — never launch a second copy while one is running. If a
   duplicate ever starts by mistake, kill it immediately and record the
   incident in the results file. The same rule applies to every spawn
   in this run.

2. When it finishes, review the Phase 1 code against the roadmap. Record
   every defect you find. Do not fix anything, and do not relay fixes to
   the next sub-agent.

3. Spawn a second sub-agent to implement Phase 2, with the prompt built
   from {{MAIN_REPO}}/prompts/subagent-phase2.md and the same spawn
   command, under the same rules.

4. When it finishes, review the Phase 2 code against the roadmap. Record
   every defect. Do not fix anything.

5. Run verification, fully scripted, in this order:
   - The implementation's own tests:
     `cd {{WORKTREE}} && {{MAIN_REPO}}/.venv/bin/python -m pytest tests/ -v`
   - The held-out acceptance suite:
     `APP_DIR={{WORKTREE}} {{MAIN_REPO}}/.venv/bin/pytest {{MAIN_REPO}}/{{ACCEPTANCE_SUITE}} -v`
   - The smoke script:
     `{{MAIN_REPO}}/{{SMOKE_SCRIPT}} {{WORKTREE}} {{PORT}}`
   Run these commands exactly as given. Do not improvise other checks, do
   not start a server any other way, and do not ask the user to run
   anything.

6. Write {{MAIN_REPO}}/results/{{RESULTS_FILE}} with these sections:
   - "Prompts used": both verbatim sub-agent prompts you passed.
   - "Review findings": the defects from steps 2 and 4, categorized, with
     file and line references, labeled by phase.
   - "Verification": the pass/fail outcomes and summary output of all
     three checks from step 5.
   Leave cost stats out — they are added later from session transcripts.

7. End with a single summary message: verification outcomes and review
   findings. Do not fix anything afterward, even if verification failed.
