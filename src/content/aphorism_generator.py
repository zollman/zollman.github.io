#!/usr/bin/env python3
"""
Script to parse APHORISMS_ALL.md and generate individual markdown files
for each aphorism with proper frontmatter for Astro content collections.
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import html

def slugify(text: str) -> str:
    """Convert title to URL-friendly slug."""
    # Remove parentheses and other special characters, convert to lowercase
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces and multiple hyphens with single hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    # Remove leading/trailing hyphens
    return slug.strip('-')

def extract_icon_from_title(title: str) -> Optional[str]:
    """Extract emoji icon from title if present."""
    # Look for common management/business related emojis that might fit the themes
    icon_map = {
        'who should do what': '🎯',
        'why then what': '💡', 
        'high safety': '🛡️',
        'call your shot': '🎯',
        'desk clerk': '🏢',
        'nemawashi': '🌱',
        'no cavalry': '🏇',
        'try and ask': '🤔',
        'option a b c': '⚖️',
        'pain power vision': '💼',
        'red conversation': '🚦',
        'good at want need': '🎯',
        'writing is thinking': '✍️',
        'agree on problem': '🤝',
        'hidden work': '🔍',
        'blue jays yankees': '⚾',
        'flight controls': '✈️',
        'debate principles': '⚖️',
        'five bullets': '📋',
        'janitor ivory tower': '🏗️',
        'bits features truth': '🔧',
        'demos hero': '🎭',
        'skill will': '🎯',
        'motivation communication': '📢',
        'platforms products': '🏗️',
        'to be of use': '💪'
    }
    
    title_lower = title.lower()
    for key, icon in icon_map.items():
        if key in title_lower:
            return icon
    
    return '📝'  # Default icon

def parse_references(ref_text: str) -> List[Dict[str, str]]:
    """Parse references section into structured format."""
    references = []
    
    # Split by numbered list items
    ref_items = re.split(r'\n\d+\.\s+', ref_text)
    
    for item in ref_items[1:]:  # Skip first empty split
        item = item.strip()
        if not item:
            continue
            
        # Try to extract URL and title from markdown links
        url_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', item)
        if url_match:
            title = url_match.group(1)
            url = url_match.group(2)
            
            # Remove the markdown link from item to get potential author
            remaining_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', '', item).strip()
            
            # Look for author patterns (text after comma, or "Author Name" pattern)
            author = None
            if remaining_text:
                # Remove leading/trailing punctuation and whitespace
                remaining_text = remaining_text.strip(' ,:')
                if remaining_text:
                    author = remaining_text
            
            ref_obj = {
                'title': title,
                'url': url
            }
            if author:
                ref_obj['author'] = author
                
            references.append(ref_obj)
        else:
            # Handle plain URLs or other formats
            url_match = re.search(r'https?://[^\s)]+', item)
            if url_match:
                url = url_match.group(0)
                # Use the rest as title, or URL as title if nothing else
                title = re.sub(r'https?://[^\s)]+', '', item).strip()
                if not title or title in ['.', ',', ':']:
                    title = url
                    
                references.append({
                    'title': title,
                    'url': url
                })
    
    return references

def clean_description(text: str) -> str:
    """Clean description text for frontmatter."""
    # Remove excessive whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove escaped dashes (markdown artifacts)
    text = text.replace('\\-', '-')
    # Escape quotes for YAML
    text = text.replace('"', '\\"')
    return text

def clean_markdown_content(text: str) -> str:
    """Clean markdown content by removing escaped characters."""
    # Remove escaped dashes (markdown artifacts)
    text = text.replace('\\-', '-')
    return text

def parse_aphorisms(content: str) -> List[Dict]:
    """Parse the APHORISMS_ALL.md content into structured aphorisms."""
    aphorisms = []
    
    # Split by ### headings, but keep the ### in each section
    sections = re.split(r'\n(?=### )', content)
    
    order = 1
    for section in sections:
        if not section.strip() or not section.startswith('###'):
            continue
            
        lines = section.split('\n')
        if not lines:
            continue
            
        # Extract title (first line, remove the ### and {#...} anchor)
        title_line = lines[0]
        title_match = re.match(r'###\s*(.+?)\s*\{#[^}]*\}', title_line)
        if title_match:
            title = title_match.group(1).strip()
        else:
            # Fallback for titles without anchors
            title = re.sub(r'^###\s*', '', title_line).strip()
            
        # Find the content and references
        content_lines = []
        references_text = ""
        in_references = False
        
        for line in lines[1:]:
            if line.strip() in ['References:', 'References \\[temporary\\]:']:
                in_references = True
                continue
            elif line.strip().startswith('###'):
                # Hit next section
                break
            elif in_references:
                references_text += line + '\n'
            else:
                content_lines.append(line)
                
        # Clean content (description)
        description = '\n'.join(content_lines).strip()
        # Clean the content to remove escaped characters
        description = clean_markdown_content(description)
        # Take first paragraph as description for frontmatter
        first_para = description.split('\n\n')[0] if description else title
        clean_desc = clean_description(first_para)
        
        # Parse references
        references = parse_references(references_text) if references_text.strip() else []
        
        # Generate icon
        icon = extract_icon_from_title(title)
        
        aphorism = {
            'title': title,
            'order': order,
            'icon': icon,
            'description': clean_desc,
            'references': references,
            'content': description,
            'slug': slugify(title)
        }
        
        aphorisms.append(aphorism)
        order += 1
    
    return aphorisms

def create_frontmatter(aphorism: Dict) -> str:
    """Create YAML frontmatter for an aphorism."""
    frontmatter = "---\n"
    frontmatter += f'title: "{aphorism["title"]}"\n'
    frontmatter += f'order: {aphorism["order"]}\n'
    frontmatter += f'icon: "{aphorism["icon"]}"\n'
    frontmatter += f'description: "{aphorism["description"]}"\n'
    
    if aphorism['references']:
        frontmatter += "references:\n"
        for ref in aphorism['references']:
            frontmatter += "  - title: \"" + ref['title'].replace('"', '\\"') + "\"\n"
            frontmatter += "    url: \"" + ref['url'] + "\"\n"
            if 'author' in ref:
                frontmatter += "    author: \"" + ref['author'].replace('"', '\\"') + "\"\n"
    
    frontmatter += "---\n"
    return frontmatter

def create_markdown_file(aphorism: Dict, output_dir: str) -> Tuple[str, str]:
    """Create a complete markdown file for an aphorism."""
    filename = f"{aphorism['order']:02d}-{aphorism['slug']}.md"
    
    content = create_frontmatter(aphorism)
    content += f"\n# {aphorism['title']}\n\n"
    content += aphorism['content']
    
    return filename, content

def main():
    # Paths
    input_file = Path("/Users/zollman/src/personal-astro/astro_academia/src/content/APHORISMS_ALL.md")
    output_dir = Path("/Users/zollman/src/personal-astro/astro_academia/src/content/aphorisms-generated")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse aphorisms
    aphorisms = parse_aphorisms(content)
    
    print(f"Found {len(aphorisms)} aphorisms")
    
    # Create files
    for aphorism in aphorisms:
        filename, file_content = create_markdown_file(aphorism, str(output_dir))
        file_path = output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
            
        print(f"Created: {filename}")
    
    print(f"\nAll files created in: {output_dir}")
    print(f"You may need to update content.config.ts to point to the new directory:")
    print(f'base: "./src/content/aphorisms-generated"')

if __name__ == "__main__":
    main()
