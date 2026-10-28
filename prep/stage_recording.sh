#!/usr/bin/env bash
# Copy a fresh, clean recording workspace next to the project folder before a take (or after a rehearsal).
# Every run creates a NEW version; nothing is moved or deleted.
#
#   bash prep/stage_recording.sh UC1     # -> <parent of project>/Mercor_UC1/UC1_Cross_Sell_v1, _v2, ...
#   bash prep/stage_recording.sh UC2     # -> <parent of project>/Mercor_UC2/UC2_Propensity_To_Pay_v1, _v2, ...
#
# e.g. project ~/LLM_Training_recording -> ~/Mercor_UC1/UC1_Cross_Sell_v1
# Set STAGE_DESTINATION to use a different parent folder.
set -euo pipefail

cd "$(dirname "$0")/.."
REPO_DIR="$(pwd)"

case "${1:-}" in
  UC1|uc1) UC="UC1"; NAME="UC1_Cross_Sell" ;;
  UC2|uc2) UC="UC2"; NAME="UC2_Propensity_To_Pay" ;;
  *) echo "Usage: bash prep/stage_recording.sh UC1|UC2" >&2; exit 1 ;;
esac

SRC="$REPO_DIR/recording_workspace/$NAME"
[ -x "$REPO_DIR/.venv/bin/python" ] || { echo "Run 'bash setup_mac.sh' first." >&2; exit 1; }

GROUP="${STAGE_DESTINATION:-$(dirname "$REPO_DIR")}/Mercor_$UC"
mkdir -p "$GROUP"
# next free version number: v1, v2, ...
LAST=$(find "$GROUP" -mindepth 1 -maxdepth 1 -type d -name "${NAME}_v*" | sed -n 's/.*_v\([0-9][0-9]*\)$/\1/p' | sort -n | tail -1)
FOLDER="${NAME}_v$(( ${LAST:-0} + 1 ))"
DEST="$GROUP/$FOLDER"

cp -R "$SRC" "$DEST"
# empty working folders for the pipeline outputs (git does not keep empty folders)
if [ -d "$DEST/Deliverables/1_Input" ]; then mkdir -p "$DEST/Deliverables/3_Intermediate" "$DEST/Deliverables/4_Output"; fi
# downloaded files carry a quarantine flag that triggers "file downloaded from the internet" pop-ups on camera
xattr -dr com.apple.quarantine "$DEST" 2>/dev/null || true

# VS Code workspace settings: AI features off, venv interpreter, readable font sizes.
# The .vscode folder is hidden from the VS Code explorer and from Finder.
mkdir -p "$DEST/.vscode"
cat > "$DEST/.vscode/settings.json" <<EOF
{
  "chat.disableAIFeatures": true,
  "github.copilot.enable": { "*": false },
  "github.copilot.nextEditSuggestions.enabled": false,
  "editor.inlineSuggest.enabled": false,
  "python.defaultInterpreterPath": "$REPO_DIR/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "editor.fontSize": 15,
  "notebook.markup.fontSize": 15,
  "terminal.integrated.fontSize": 14,
  "workbench.startupEditor": "none",
  "files.exclude": { "**/.vscode": true, "**/.DS_Store": true, "**/.ipynb_checkpoints": true, "**/__pycache__": true, "Metadata.rtf": true },
  "workbench.editorAssociations": { "*.md": "vscode.markdown.preview.editor" },
  "jupyter.notebookFileRoot": "\${fileDirname}"
}
EOF

echo "Staged clean workspace: $DEST"
(cd "$DEST/Deliverables" && find . -mindepth 1 -maxdepth 2 -not -name ".*" | sort | sed "s|^./||")
echo
echo "Open it in VS Code:  File > Open Folder... > $GROUP > $FOLDER"
echo "Then follow PART 2 of the recording script (UC1_RECORDING_SCRIPT.md / UC2_RECORDING_SCRIPT.md)"
