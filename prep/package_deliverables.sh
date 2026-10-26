#!/usr/bin/env bash
# Validate a finished take and build Deliverables.zip (run OFF camera, after recording).
#   bash prep/package_deliverables.sh UC1      (or UC2)
set -euo pipefail
cd "$(dirname "$0")/.."
exec .venv/bin/python prep/package_deliverables.py "$@"
