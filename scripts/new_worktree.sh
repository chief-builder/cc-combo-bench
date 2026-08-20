#!/usr/bin/env bash
# Create a clean combo worktree with benchmark scaffolding stripped.
# Stripping matters: the acceptance suite is only "held out" if it isn't
# in the worktree (the pilot's sub-agent read it from there), and stray
# scaffolding pollutes pytest collection.
#
# Usage: scripts/new_worktree.sh <worktree_path>
set -eu

WORKTREE="${1:?usage: new_worktree.sh <worktree_path>}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

git -C "$REPO_ROOT" worktree add --detach "$WORKTREE" HEAD
rm -rf "$WORKTREE/PLAN.md" "$WORKTREE/acceptance" "$WORKTREE/prompts" \
  "$WORKTREE/scripts" "$WORKTREE/results"
echo "worktree ready: $WORKTREE"
