#!/usr/bin/env python
import sys
import re
import os

try:
    import markdown
except ImportError:
    print("Error: The 'markdown' library is required. Please install it using your system's package manager (e.g., 'sudo pacman -S python-markdown') or with pip/uv.", file=sys.stderr)
    sys.exit(1)

def format_changelog(changelog_text):
    """
    Converts changelog text to HTML using the markdown library.
    If it already contains HTML, it's returned as is.
    """
    text = changelog_text.strip()
    if re.search(r'<(h[1-6]|ul|li|hr|p|div|table)>', text, re.IGNORECASE):
        return text
    html = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    return html

def format_game_items(content):
    """
    Parses the indented structure of the 'game items' section and formats it into
    HTML with subheadings and lists.
    """
    if not content:
        return ""
    
    # Split the content by subsection headers (e.g., "standalone...:") but keep them as delimiters
    subsections = re.split(r'(^\s*[a-zA-Z ]+\s*\.{3,}:)', content, flags=re.MULTILINE)
    
    html = ""
    # Start from index 1 because the first split element is usually empty space before the first header
    for i in range(1, len(subsections), 2):
        # Header is the delimiter, body is the content that follows
        header = subsections[i].strip().replace('...:', '').replace('....:', '').title()
        body = subsections[i+1]
        
        html += f"<h4>{header}</h4>\n<ul>\n"
        
        # This regex handles multi-line items with optional versions
        item_pattern = re.compile(r'^\s*\[(.*?)\] -- (.*?)(?:\n\s*version: (.*?))?$', re.MULTILINE)
        
        for match in item_pattern.finditer(body):
            filename, description, version = match.groups()
            html += f"<li><strong>{filename}:</strong> {description}"
            if version:
                html += f"<br><small class='version-info'>Version: {version.strip()}</small>"
            html += "</li>\n"
            
        html += "</ul>\n"
        
    return html

def create_html_from_info(file_path):
    """
    Reads a GOG !info.txt file and converts it into a complete HTML file with a dark theme,
    then prints it to standard output.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}", file=sys.stderr)
        sys.exit(1)

    # --- Line-by-line parsing logic for robustness ---
    lines = content.splitlines()
    
    section_buffers = {
        'metadata': [],
        'game items': [],
        'extras': [],
        'changelog': [],
        'gog messages': []
    }
    
    current_section_key = 'metadata'
    header_pattern = re.compile(r'^([a-zA-Z ]+)\s*\.{3,}:', re.IGNORECASE)

    for line in lines:
        match = header_pattern.match(line)
        # Check if the line is a section header
        if match:
            section_name = match.group(1).strip().lower()
            if section_name in section_buffers:
                current_section_key = section_name
                continue  # Skip adding the header line itself to the content

        # Append the line to the buffer for the current section
        section_buffers[current_section_key].append(line)

    # Join the collected lines for each section
    metadata_part = '\n'.join(section_buffers['metadata'])
    game_items_content = '\n'.join(section_buffers['game items'])
    extras_content = '\n'.join(section_buffers['extras'])
    changelog_content = '\n'.join(section_buffers['changelog'])
    gog_messages_content = '\n'.join(section_buffers['gog messages'])

    # --- Title and Metadata Parsing ---
    title_match = re.search(r"title\s*\.{5,}\s*(.*)", metadata_part, re.IGNORECASE)
    title = title_match.group(1).strip().replace('_', ' ').title() if title_match else "Game Information"

    meta_html = "<h2>Game Details</h2>\n<dl>\n"
    meta_regex = re.compile(r"^(.+?)\s*\.{5,}\s*(.+)$", re.MULTILINE)
    for match in meta_regex.finditer(metadata_part):
        key = match.group(1).strip().replace('_', ' ').title()
        value = match.group(2).strip()
        if key.lower() == 'title': continue
        if key.lower() == 'url':
            meta_html += f"  <dt>{key}</dt>\n  <dd><a href=\"{value}\" target=\"_blank\">{value}</a></dd>\n"
        else:
            meta_html += f"  <dt>{key}</dt>\n  <dd>{value}</dd>\n"
    meta_html += "</dl>\n"

    # --- GOG Messages Section ---
    gog_messages_html = ""
    if gog_messages_content.strip():
        gog_messages_html = f"<h2>GOG Messages</h2>\n<div class=\"message-box\">{markdown.markdown(gog_messages_content)}</div>\n"

    # --- Game Items Section (uses the new detailed formatter) ---
    game_items_html = ""
    if game_items_content.strip():
        game_items_html = "<h2>Game Items</h2>\n" + format_game_items(game_items_content)

    # --- Extras Section ---
    extras_html = ""
    if extras_content.strip():
        extras_html = "<h2>Extras</h2>\n<ul>\n"
        for extra in extras_content.strip().splitlines():
            if extra.strip():
                clean_extra = re.sub(r"\[(.*?)\] -- ", r"<strong>\1:</strong> ", extra.strip())
                extras_html += f"  <li>{clean_extra}</li>\n"
        extras_html += "</ul>\n"

    # --- Changelog Section ---
    changelog_html = ""
    if changelog_content.strip():
        formatted_changelog = format_changelog(changelog_content)
        changelog_html = f"<h2>Changelog</h2>{formatted_changelog}"

    # --- Final HTML Assembly ---
    html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.4; margin: 0; background-color: #1e1e1e; color: #d4d4d4; }}
        .container {{ max-width: 800px; margin: 2em auto; background: #2d2d2d; padding: 2em; border-radius: 8px; border: 1px solid #444; box-shadow: 0 4px 12px rgba(0,0,0,0.4); }}
        h1 {{ font-size: 1.8em; margin-top: 0; color: #ffffff; border-bottom: 1px solid #555; padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.4em; color: #ffffff; border-bottom: 1px solid #555; padding-bottom: 0.3em; }}
        h3 {{ font-size: 1.1em; color: #ffffff; border-bottom: 1px solid #555; padding-bottom: 0.3em; }}
        h4, h5 {{ color: #fafafa; margin-top: 1.2em; font-size: 1.0em; }}
        p {{ margin-top: 0; margin-bottom: 0.7em; }}
        dt {{ font-weight: bold; color: #cccccc; float: left; width: 120px; clear: left; }}
        dd {{ margin-left: 140px; margin-bottom: 8px; }}
        a {{ color: #68a0ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        strong {{ color: #c8c8c8; }}
        hr {{ border: 0; border-top: 1px solid #555; margin: 1.5em 0; }}
        ul, ol {{ padding-left: 20px; }}
        li {{ margin-bottom: 0.1em; }}
        li p {{ margin-bottom: 0.1em; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 1em; }}
        th, td {{ border: 1px solid #555; padding: 8px; text-align: left; }}
        th {{ background-color: #3a3a3a; font-weight: bold; }}
        code, pre {{ background-color: #252526; font-family: monospace; }}
        pre {{ padding: 1em; border-radius: 5px; white-space: pre-wrap; word-wrap: break-word; }}
        .message-box {{ background-color: #3a3a3a; border-left: 4px solid #68a0ff; padding: 0.5em 1.5em; margin-bottom: 1.5em; border-radius: 4px; }}
        .version-info {{ color: #9e9e9e; font-style: italic; font-size: 0.9em; }}
    </style>
</head>
<body><div class="container"><h1>{title}</h1><div class="content">{meta_html}{gog_messages_html}{game_items_html}{extras_html}{changelog_html}</div></div></body>
</html>"""
    print(html_output)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gog-convert.py <path_to_!info.txt>", file=sys.stderr)
        sys.exit(1)
    create_html_from_info(sys.argv[1])

