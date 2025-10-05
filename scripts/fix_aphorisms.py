#!/usr/bin/env python3
"""
Script to remove duplication from aphorism markdown files.
Removes the 'description' field from frontmatter and the duplicate heading from the body.
"""

import re
import sys
from pathlib import Path

def process_aphorism_file(filepath):
    """
    Process a single aphorism markdown file:
    1. Remove the 'description' field from frontmatter
    2. Remove the duplicate h1 heading from the body (if it matches the title)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into frontmatter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"Warning: {filepath} doesn't have valid frontmatter")
        return False
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Extract title from frontmatter
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
    title = title_match.group(1).strip('"\'') if title_match else None
    
    # Remove description field from frontmatter (handles multi-line descriptions)
    # Match 'description:' followed by quoted string that may span multiple lines
    frontmatter_cleaned = re.sub(
        r'^description:\s*["\'].*?["\']$',
        '',
        frontmatter,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # Also handle case where description is on multiple lines without the closing quote on same line
    frontmatter_cleaned = re.sub(
        r'^description:.*?\n',
        '',
        frontmatter_cleaned,
        flags=re.MULTILINE
    )
    
    # Remove empty lines from frontmatter
    frontmatter_lines = [line for line in frontmatter_cleaned.split('\n') if line.strip()]
    frontmatter_cleaned = '\n'.join(frontmatter_lines)
    
    # Clean up body: remove the duplicate h1 heading if it matches the title
    body_cleaned = body.lstrip('\n')
    
    if title:
        # Remove h1 heading that matches the title (e.g., "# Why, then what, then how")
        heading_pattern = rf'^#\s+{re.escape(title)}\s*$'
        body_cleaned = re.sub(heading_pattern, '', body_cleaned, flags=re.MULTILINE)
    
    # Remove leading blank lines from body
    body_cleaned = body_cleaned.lstrip('\n')
    
    # Reconstruct the file
    new_content = f"---\n{frontmatter_cleaned}\n---\n\n{body_cleaned}"
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    # Find all aphorism markdown files
    aphorisms_dir = Path(__file__).parent / 'src' / 'content' / 'aphorisms'
    
    if not aphorisms_dir.exists():
        print(f"Error: Directory {aphorisms_dir} not found")
        sys.exit(1)
    
    aphorism_files = sorted(aphorisms_dir.glob('*.md'))
    
    if not aphorism_files:
        print(f"Warning: No markdown files found in {aphorisms_dir}")
        sys.exit(1)
    
    print(f"Processing {len(aphorism_files)} aphorism files...")
    
    success_count = 0
    for filepath in aphorism_files:
        print(f"  Processing {filepath.name}...", end=' ')
        if process_aphorism_file(filepath):
            print("✓")
            success_count += 1
        else:
            print("✗")
    
    print(f"\nSuccessfully processed {success_count}/{len(aphorism_files)} files")

if __name__ == '__main__':
    main()
