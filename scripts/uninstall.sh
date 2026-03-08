#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <target-workspace-path>"
  exit 1
fi

TARGET="$1"
MANIFEST_FILE="$TARGET/.founder-kit/installed_paths.txt"

if [[ ! -f "$MANIFEST_FILE" ]]; then
  echo "No installation manifest found: $MANIFEST_FILE"
  exit 1
fi

while IFS= read -r path; do
  if [[ -n "$path" && -e "$path" ]]; then
    rm -rf "$path"
    echo "Removed: $path"
  fi
done < "$MANIFEST_FILE"

echo "Uninstall complete. Backups (if created) remain in: $TARGET/.founder-kit-backup"
