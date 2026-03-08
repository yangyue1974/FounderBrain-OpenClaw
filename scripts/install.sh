#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <target-workspace-path> [--force]"
  exit 1
fi

TARGET="$1"
FORCE="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES_DIR="$ROOT_DIR/templates"
STAMP="$(date +%Y%m%d%H%M%S)"
BACKUP_DIR="$TARGET/.founder-kit-backup/$STAMP"
MANIFEST_DIR="$TARGET/.founder-kit"
MANIFEST_FILE="$MANIFEST_DIR/installed_paths.txt"

mkdir -p "$TARGET" "$BACKUP_DIR" "$MANIFEST_DIR"
: > "$MANIFEST_FILE"

copy_with_backup() {
  local src="$1"
  local dst="$2"

  if [[ -e "$dst" ]]; then
    if [[ "$FORCE" != "--force" ]]; then
      local rel
      rel="${dst#$TARGET/}"
      mkdir -p "$BACKUP_DIR/$(dirname "$rel")"
      cp -R "$dst" "$BACKUP_DIR/$rel"
    fi
  fi

  mkdir -p "$(dirname "$dst")"
  rm -rf "$dst"
  cp -R "$src" "$dst"
  echo "$dst" >> "$MANIFEST_FILE"
}

copy_with_backup "$TEMPLATES_DIR/skills" "$TARGET/skills"
copy_with_backup "$TEMPLATES_DIR/router" "$TARGET/router"
copy_with_backup "$TEMPLATES_DIR/prompts" "$TARGET/prompts"
copy_with_backup "$TEMPLATES_DIR/memory" "$TARGET/memory"
mkdir -p "$TARGET/agent"
copy_with_backup "$TEMPLATES_DIR/agent/IDENTITY.md" "$TARGET/agent/IDENTITY.md"
copy_with_backup "$TEMPLATES_DIR/agent/TOOLS.md" "$TARGET/agent/TOOLS.md"
copy_with_backup "$TEMPLATES_DIR/agent/MEMORY.md" "$TARGET/agent/MEMORY.md"

echo "Installed founder agent kit into: $TARGET"
echo "Backup (if any): $BACKUP_DIR"
echo "Installed paths manifest: $MANIFEST_FILE"
