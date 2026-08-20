# Kickoff — single cross-provider sub-agent, all phases

Cross-provider phase: identical to kickoff-single.md except the spawn
command and the cost-stats note. `{{SUBAGENT_CLI}}` is the provider's
full non-interactive command (see README.md per-provider table); the
prompt is piped to it on stdin. The sub-agent prompt file is the same
provider-neutral subagent-both-phases.md — that neutrality is the
control.

---

You are the main agent in a benchmark run. Your working directory is
{{WORKTREE}}, a clean worktree of the benchmark repo. The app to build is
specified in {{SPEC_DIR}}/ (mission.md, tech-stack.md, roadmap.md).

You orchestrate; you never implement. Do not write or edit implementation
code or tests yourself, and do not fix any problem you find — your role is
to delegate, verify, and report.

1. Spawn exactly one sub-agent to implement all phases of the roadmap.
   Build its prompt from {{MAIN_REPO}}/prompts/subagent-both-phases.md:
   take the part below its `---` line, fill the placeholders the same
   way as this prompt, and save it to a unique temp file created with
   `mktemp` — never a fixed or shared path; parallel benchmark runs
   collide on shared scratch files. Pass it verbatim — do not reword,
   add, or remove anything. Spawn by running exactly this command in
   the FOREGROUND with an explicit long timeout (600000 ms) — it can
   take ten minutes; never background it and never rely on monitors or
   completion notifications, which do not survive in this environment:

   `cd {{WORKTREE}} && {{SUBAGENT_CLI}} < <the temp file>`

   Capture its full stdout; the final message in it is the sub-agent's
   report. Start it exactly once — never launch a second copy while one
   is running. If a duplicate ever starts by mistake, kill it
   immediately and record the incident in the results file.

2. When it finishes, review the implementation by reading the code against
   the roadmap. Record every defect you find (critical/functional,
   spec-conformance, minor/style). Do not fix anything.

3. Run verification, fully scripted, in this order:
   - The implementation's own tests:
     `cd {{WORKTREE}} && {{MAIN_REPO}}/.venv/bin/python -m pytest tests/ -v`
   - The held-out acceptance suite:
     `APP_DIR={{WORKTREE}} {{MAIN_REPO}}/.venv/bin/pytest {{MAIN_REPO}}/{{ACCEPTANCE_SUITE}} -v`
   - The smoke script:
     `{{MAIN_REPO}}/{{SMOKE_SCRIPT}} {{WORKTREE}} {{PORT}}`
   Run these commands exactly as given. Do not improvise other checks, do
   not start a server any other way, and do not ask the user to run
   anything.

4. Write {{MAIN_REPO}}/results/{{RESULTS_FILE}} with these sections:
   - "Prompts used": the verbatim sub-agent prompt you passed, and the
     exact spawn command line you ran.
   - "Review findings": the defects from step 2, categorized, with file
     and line references.
   - "Verification": the pass/fail outcomes and summary output of all
     three checks from step 3.
   - "Provider stats": any token-usage or model information the
     provider printed to stdout (e.g. a "tokens used" line), quoted
     verbatim. Leave all other cost stats out — they are added later.

5. End with a single summary message: verification outcomes and review
   findings. Do not fix anything afterward, even if verification failed.
