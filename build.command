#!/bin/bash
set -euo pipefail

# Run from this script's directory (project root)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

APP_NAME="TowelCodeCombiner"
MAIN_PY="list_all_files.py"

# Explicit macOS icon (you have this file)
ICON_ICNS="icon/AppIcon.icns"

# Safety check
if [ ! -f "$ICON_ICNS" ]; then
  echo "❌ Icon not found: $ICON_ICNS"
  exit 1
fi

# Clean old builds
rm -rf build dist

# Build
pyinstaller \
  --noconfirm \
  --clean \
  --name "$APP_NAME" \
  --onefile \
  --windowed \
  --icon "$ICON_ICNS" \
  --hidden-import tkinterdnd2 \
  --collect-all tkinterdnd2 \
  "$MAIN_PY"

echo ""
echo "✅ Build complete."
echo "📦 Output: $SCRIPT_DIR/dist/$APP_NAME.app (or dist/$APP_NAME depending on PyInstaller)"
echo "🎨 Icon used: $ICON_ICNS"
