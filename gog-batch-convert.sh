#!/bin/bash
# A script to find all !info.txt files in a directory and convert them to info.html

# Check if a directory was provided
if [ -z "$1" ]; then
  echo "Usage: ./gog-batch-convert.sh /path/to/your/gog/library"
  exit 1
fi

GOG_DIR="$1"
SCRIPT_PATH="$HOME/.local/bin/gog-convert.py"

echo "🔍 Searching for !info.txt files in: $GOG_DIR"

# Find all !info.txt files and process them
find "$GOG_DIR" -type f -name '!info.txt' | while read -r file; do
  DIR=$(dirname "$file")
  OUTPUT_HTML="$DIR/info.html"
  echo "  > Converting: $file"
  "$SCRIPT_PATH" "$file" > "$OUTPUT_HTML"
done

echo "✅ Batch conversion complete!"
