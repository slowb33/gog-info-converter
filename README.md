Of course. Here is the complete source code for the `README.md` file. You can copy this directly into a new `README.md` file in your project folder, and GitHub will format it correctly.

````markdown
# GOG Info Converter

A Python script to convert GOG.com `!info.txt` files into beautifully styled, readable HTML files. It includes a dark theme and can be integrated with the Dolphin file manager for easy, one-click conversions.

This project was inspired by Dirk Adam and developed with Google Gemini.

---

## Features

-   **Intelligent Parsing:** Accurately parses different formats of `!info.txt` files, including those with subsections for standalone, Galaxy, and shared game items.
-   **Markdown & HTML Support:** Automatically detects and correctly formats changelogs written in either Markdown-like syntax or plain HTML.
-   **Dark Theme:** Generates a clean, modern dark-themed HTML output for comfortable viewing.
-   **Dolphin Integration:** Can be configured to run on double-click from the KDE Dolphin file manager.
-   **Batch Conversion:** Includes a shell script to convert an entire library of `!info.txt` files at once.

---

## Requirements

This script is designed for Arch-based Linux distributions (like CachyOS) using the KDE Plasma desktop environment.

-   **Python 3**
-   **`python-markdown` library:** Provides robust Markdown-to-HTML conversion.

---

## Installation

Follow these steps to set up the script and integrate it with your system.

### 1. Install Dependencies

The script requires the `python-markdown` library. Open a terminal and install it using `pacman`:

```bash
sudo pacman -S python-markdown
````

### 2\. Place the Script

Place the `gog-convert.py` script in a directory that is part of your system's `PATH`. A standard location for user scripts is `~/.local/bin/`.

```bash
# Create the directory if it doesn't exist
mkdir -p ~/.local/bin

# Move the script into the directory
mv gog-convert.py ~/.local/bin/

# Make the script executable
chmod +x ~/.local/bin/gog-convert.py
```

-----

## Usage

There are two primary ways to use the converter.

### Option A: Double-Click to View in Dolphin

This is the most convenient method for viewing individual files. It creates a temporary HTML file and opens it in your default web browser.

**1. Create the `.desktop` file:**

Using a text editor like `vi`, create a new file at `~/.local/share/applications/gog-info-viewer.desktop` and add the following content:

```ini
[Desktop Entry]
Type=Application
Name=GOG Info Viewer
Comment=View GOG !info.txt files in a browser
Exec=sh -c 'TMPFILE=$(mktemp --suffix=.html); ~/.local/bin/gog-convert.py "%f" > "$TMPFILE" && xdg-open "$TMPFILE"'
Icon=text-html
Terminal=false
MimeType=text/plain;
```

**2. Associate the File Type:**

Now, tell Dolphin to use this new action for `!info.txt` files.

  - Find any `!info.txt` file in Dolphin.
  - **Right-click** on it → **Properties**.
  - Go to the **"File Type Options"** tab.
  - In the "Application Preference Order" list, find **"GOG Info Viewer"** and move it to the top.
  - Click **OK**.

From now on, double-clicking any `!info.txt` file will open a perfectly formatted version in your browser.

### Option B: Batch Convert Your Library

To generate a permanent `info.html` file for every `!info.txt` in your game library, you can use the provided batch script.

**1. Create the batch script:**

Create a file named `gog-batch-convert.sh` in `~/.local/bin/` with the following content:

```bash
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
```

**2. Make it executable:**

```bash
chmod +x ~/.local/bin/gog-batch-convert.sh
```

**3. Run the script:**

Point the script to your main GOG games directory.

```bash
gog-batch-convert.sh "/path/to/your/GOG Games/"
```

The script will find every `!info.txt` and create a corresponding `info.html` file in the same folder.

```
```
