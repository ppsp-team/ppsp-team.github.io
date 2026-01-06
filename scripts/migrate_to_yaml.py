#!/usr/bin/env python3
"""
Migration script to convert existing .md publication files to single YAML file.
Run once to migrate, then delete this script.
"""

import os
import re
import yaml
from pathlib import Path

# Paths
PAPERS_DIR = Path(__file__).parent.parent / '_papers' / 'papers'
OUTPUT_FILE = Path(__file__).parent.parent / '_data' / 'publications.yml'


def parse_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding='utf-8')
    
    # Extract frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    
    try:
        data = yaml.safe_load(match.group(1))
        return data
    except yaml.YAMLError as e:
        print(f"  ⚠️ YAML error in {file_path.name}: {e}")
        return None


def migrate_publications():
    """Migrate all .md publication files to single YAML."""
    if not PAPERS_DIR.exists():
        print(f"❌ Papers directory not found: {PAPERS_DIR}")
        return
    
    publications = []
    errors = []
    
    # Process all .md files
    md_files = sorted(PAPERS_DIR.glob('*.md'))
    print(f"📂 Found {len(md_files)} publication files")
    
    for md_file in md_files:
        data = parse_frontmatter(md_file)
        if data:
            # Extract relevant fields
            pub = {
                'title': data.get('title', ''),
                'authors': data.get('authors', ''),
                'publication': data.get('publication', ''),
                'year': data.get('year'),
                'link': data.get('link', ''),
                'type': data.get('type', 'Journal Paper'),
                'category': data.get('category', [])
            }
            
            # Ensure category is a list
            if isinstance(pub['category'], str):
                pub['category'] = [pub['category']]
            elif pub['category'] is None:
                pub['category'] = []
            
            # Only add if we have a title
            if pub['title']:
                publications.append(pub)
            else:
                errors.append(md_file.name)
        else:
            errors.append(md_file.name)
    
    # Sort by year (newest first)
    publications.sort(key=lambda x: x.get('year', 0) or 0, reverse=True)
    
    # Save to YAML
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(publications, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✅ Migrated {len(publications)} publications to {OUTPUT_FILE}")
    
    if errors:
        print(f"⚠️ Skipped {len(errors)} files with errors:")
        for e in errors[:5]:
            print(f"   - {e}")
        if len(errors) > 5:
            print(f"   ... and {len(errors) - 5} more")


if __name__ == "__main__":
    migrate_publications()
