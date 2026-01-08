#!/usr/bin/env python3
"""
Clean publications data - fix doubled years, remove duplicates, fix wrong years.
"""

import yaml
import re
from pathlib import Path
from datetime import datetime

PUBLICATIONS_FILE = Path(__file__).parent.parent / '_data' / 'publications.yml'


def clean_publication_field(pub: dict) -> dict:
    """Clean up the publication field - remove doubled years."""
    publication = pub.get('publication', '')
    year = pub.get('year')
    
    if publication and year:
        # Remove year from end of publication if it appears there
        # Pattern: ", 2024" or ", 2024, 2024" etc.
        publication = re.sub(r',?\s*\d{4}(,?\s*\d{4})*\s*$', '', publication)
        pub['publication'] = publication.strip().rstrip(',')
    
    return pub


def extract_year_from_publication(pub: dict) -> dict:
    """Try to extract correct year from publication field if current year seems wrong."""
    publication = pub.get('publication', '')
    current_year = pub.get('year')
    
    # If year is current year or future (likely a fallback value), try to find real year in publication field
    this_year = datetime.now().year
    if current_year and current_year >= this_year and publication:
        # Look for year pattern in publication - use consistent pattern (1900-2029)
        year_match = re.search(r'\b(19\d{2}|20[0-2]\d)\b', publication)
        if year_match:
            real_year = int(year_match.group())
            # Only update if the found year is older (more likely to be correct)
            if real_year < current_year:
                print(f"   📅 Fixed year: {current_year} → {real_year} for: {pub.get('title', '')[:50]}...")
                pub['year'] = real_year
    
    return pub


def remove_duplicates(pubs: list) -> tuple[list, int]:
    """Remove duplicate publications based on title similarity.
    
    Returns:
        tuple[list, int]: Tuple of (unique_publications, duplicates_removed_count)
    """
    seen_titles = set()  # Use set instead of dict for efficiency
    unique_pubs = []
    duplicates_removed = 0
    
    for pub in pubs:
        title = pub.get('title', '').lower().strip()
        # Normalize title for comparison
        normalized = re.sub(r'[^a-z0-9]', '', title)
        
        if normalized and normalized not in seen_titles:
            seen_titles.add(normalized)
            unique_pubs.append(pub)
        else:
            duplicates_removed += 1
            print(f"   🔄 Removed duplicate: {pub.get('title', '')[:60]}...")
    
    return unique_pubs, duplicates_removed


def clean_publications():
    """Main cleaning function."""
    if not PUBLICATIONS_FILE.exists():
        print(f"❌ File not found: {PUBLICATIONS_FILE}")
        return
    
    with open(PUBLICATIONS_FILE, 'r', encoding='utf-8') as f:
        pubs = yaml.safe_load(f)
    
    if not pubs:
        print("❌ No publications found")
        return
    
    print(f"🧹 Cleaning {len(pubs)} publications...")
    
    # Step 1: Clean publication fields (remove doubled years)
    print("\n📝 Cleaning publication fields...")
    for pub in pubs:
        clean_publication_field(pub)
    
    # Step 2: Fix wrong 2025 fallback years
    print("\n📅 Fixing fallback years...")
    for pub in pubs:
        extract_year_from_publication(pub)
    
    # Step 3: Remove duplicates
    print("\n🔄 Removing duplicates...")
    pubs, dup_count = remove_duplicates(pubs)
    
    # Step 4: Sort by year (newest first)
    pubs.sort(key=lambda x: x.get('year', 0) or 0, reverse=True)
    
    # Save
    with open(PUBLICATIONS_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(pubs, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"\n✅ Done! Cleaned {len(pubs)} publications, removed {dup_count} duplicates.")


if __name__ == "__main__":
    clean_publications()
