#!/bin/bash

# Always resolve paths relative to the script itself
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure data dir and files
mkdir -p "$PROJECT_ROOT/data"
touch "$PROJECT_ROOT/data/journal.txt" \
      "$PROJECT_ROOT/data/processed.txt" \
      "$PROJECT_ROOT/data/failed.txt"

# Create symlink to the journal file
mkdir -p ~/AudioHijackLogs
ln -sf "$PROJECT_ROOT/data/journal.txt" ~/AudioHijackLogs/journal.txt

echo "📂 Created symlink: ~/AudioHijackLogs/journal.txt → $PROJECT_ROOT/data/journal.txt"