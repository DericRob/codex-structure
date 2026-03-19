#!/usr/bin/env bash
set -euo pipefail

documents_dir="$HOME/Documents"
codex_file="$documents_dir/CODEX.md"

if [[ ! -f "$codex_file" ]]; then
  echo "Missing workspace instructions: $codex_file" >&2
  exit 1
fi

workspace_instructions="$(cat "$codex_file")"
bootstrap_prompt="$(cat <<EOF
Read and follow the workspace instructions below before doing any work.

BEGIN WORKSPACE INSTRUCTIONS
$workspace_instructions
END WORKSPACE INSTRUCTIONS
EOF
)"

exec codex --cd "$documents_dir" "$@" "$bootstrap_prompt"
