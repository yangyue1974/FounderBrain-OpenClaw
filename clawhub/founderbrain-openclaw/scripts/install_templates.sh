#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <target-workspace-path>"
  exit 1
fi

TARGET="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$(cd "$SCRIPT_DIR/../assets/templates" && pwd)"
STAMP="$(date +%Y%m%d%H%M%S)"
BACKUP_DIR="$TARGET/.founderbrain-backup/$STAMP"

mkdir -p "$TARGET" "$BACKUP_DIR"

backup_and_copy() {
  local rel="$1"
  local src="$ASSETS_DIR/$rel"
  local dst="$TARGET/$rel"
  if [[ -e "$dst" ]]; then
    mkdir -p "$BACKUP_DIR/$(dirname "$rel")"
    cp -R "$dst" "$BACKUP_DIR/$rel"
  fi
  mkdir -p "$(dirname "$dst")"
  rm -rf "$dst"
  cp -R "$src" "$dst"
}

backup_and_copy skills
backup_and_copy router
backup_and_copy prompts
backup_and_copy memory
backup_and_copy agent

echo "FounderBrain installed to: $TARGET"
echo "Backup saved at: $BACKUP_DIR"
