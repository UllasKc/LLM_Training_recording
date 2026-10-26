#!/usr/bin/env bash
# One-time setup on the provided Apple Silicon Mac (run inside the dedicated recording user).
#
#   bash setup_mac.sh
#
# Creates .venv with Python 3.12, installs the locked packages (prebuilt arm64 wheels only),
# registers a Jupyter kernel for VS Code, and verifies everything. Safe to re-run.
set -euo pipefail

cd "$(dirname "$0")"
REPO_DIR="$(pwd)"
KERNEL_NAME="ds-venv"
KERNEL_LABEL="Python 3.12 (ds-venv)"

say()  { printf "\n\033[1m==> %s\033[0m\n" "$1"; }
fail() { printf "\n\033[31mERROR: %s\033[0m\n" "$1" >&2; exit 1; }

say "Checking machine"
[ "$(uname -s)" = "Darwin" ] || fail "This script is for macOS."
[ "$(uname -m)" = "arm64" ]  || fail "Apple Silicon (M-series) Mac required; found $(uname -m)."
echo "macOS $(sw_vers -productVersion) on $(sysctl -n machdep.cpu.brand_string)"

say "Finding Python 3.12"
PY=""
for c in python3.12 /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 /opt/homebrew/bin/python3.12; do
  if command -v "$c" >/dev/null 2>&1; then PY="$(command -v "$c")"; break; fi
done
if [ -z "$PY" ]; then
  fail "Python 3.12 not found.
  Install it from https://www.python.org/downloads/macos/ (latest 3.12.x 'macOS 64-bit universal2 installer'),
  then re-run: bash setup_mac.sh
  (The python3 that ships with Xcode is 3.9 and is not used.)"
fi
echo "Using $PY ($("$PY" --version))"

say "Creating virtual environment in .venv"
if [ ! -x .venv/bin/python ]; then
  "$PY" -m venv .venv
fi
.venv/bin/python -m pip install --quiet --upgrade pip

say "Installing locked packages (binary wheels only - nothing is compiled)"
.venv/bin/python -m pip install --quiet --only-binary=:all: -r requirements-lock.txt

say "Registering Jupyter kernel '$KERNEL_LABEL' for VS Code"
.venv/bin/python -m ipykernel install --user --name "$KERNEL_NAME" --display-name "$KERNEL_LABEL" >/dev/null

say "Verifying setup"
.venv/bin/python prep/verify_setup.py

cat <<EOF

Setup complete.
  Interpreter : $REPO_DIR/.venv/bin/python
  VS Code     : pick kernel "$KERNEL_LABEL" in the notebook kernel picker
Next, before each take:
  bash prep/stage_recording.sh UC1     # or UC2
EOF
