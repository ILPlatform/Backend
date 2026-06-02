#!/usr/bin/env bash

set -e

if [ -n "${BASH_VERSION:-}" ]; then
  SCRIPT_PATH="${BASH_SOURCE[0]}"
elif [ -n "${ZSH_VERSION:-}" ]; then
  SCRIPT_PATH="${(%):-%x}"
else
  SCRIPT_PATH="$0"
fi

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$SCRIPT_PATH")" && pwd)"
FUNCTIONS_DIR="$ROOT_DIR/functions"
VENV_DIR="$FUNCTIONS_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
  python3.12 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install -r "$FUNCTIONS_DIR/requirements.txt"
source "$VENV_DIR/bin/activate"

if command -v lsof >/dev/null 2>&1 && lsof -nP -iTCP:5001 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port 5001 is already in use. The Functions emulator may already be running:"
  lsof -nP -iTCP:5001 -sTCP:LISTEN
  return 1 2>/dev/null || exit 1
fi

cd "$ROOT_DIR"
firebase emulators:start --only functions
