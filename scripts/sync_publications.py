#!/usr/bin/env python3
"""
Publications Sync Script - SerpAPI Google Scholar Integration
Fetches publications from Google Scholar and updates _data/publications.yml
"""

import os
import re
import yaml
import requests
from pathlib import Path

# Get current year dynamically for fallback
def get_current_year():
    """Return current year for fallback when year is unknown."""
    import datetime
    return datetime.datetime.now().year

# Load environment variables from .env file
def load_env():
    env_path = Path(__file__).parent / '.env'
    env_vars = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Strip quotes from values (handles "value" or 'value')
                    value = value.strip().strip('"').strip("'")
                    env_vars[key.strip()] = value
    return env_vars

env = load_env()
SERPAPI_KEY = env.get('SERPAPI_KEY', os.getenv('SERPAPI_KEY', ''))
AUTHOR_ID = env.get('AUTHOR_ID', 'TakXk9MAAAAJ')  # Guillaume Dumas's Google Scholar ID

# Paths
SCRIPT_DIR = Path(__file__).parent
PUBLICATIONS_FILE = SCRIPT_DIR.parent / '_data' / 'publications.yml'


def fetch_scholar_publications(author_id: str, api_key: str, start: int = 0) -> dict:
    """Fetch publications from Google Scholar via SerpAPI."""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_scholar_author",
        "author_id": author_id,
        "api_key": api_key,
        "start": start,
        "num": 100,  # Max per request
        "sort": "pubdate"  # Sort by publication date
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def extract_publication_info(article: dict) -> dict:
    """Extract publication info from SerpAPI article data."""
    # Parse year from the publication info
    year = article.get('year', '')
    if not year:
        # Try to extract from citation info
        citation = article.get('citation', '')
        # Use consistent year regex pattern (1900-2029)
        year_match = re.search(r'\b(19\d{2}|20[0-2]\d)\b', citation)
        if year_match:
            year = year_match.group()
    
    # Get publication venue
    publication = article.get('publication', '')
    if not publication:
        # Try citation field
        citation = article.get('citation', '')
        if citation:
            publication = citation.split(',')[0] if ',' in citation else citation
    
    # Determine type based on publication venue
    pub_type = "Journal Paper"
    pub_lower = publication.lower() if publication else ""
    if 'arxiv' in pub_lower or 'biorxiv' in pub_lower or 'medrxiv' in pub_lower:
        pub_type = "Preprint"
    elif 'conference' in pub_lower or 'proceedings' in pub_lower:
        pub_type = "Conference"
    elif 'book' in pub_lower or 'chapter' in pub_lower:
        pub_type = "Book_Chapter"
    
    # Use current year as fallback instead of hardcoded value
    fallback_year = get_current_year()
    parsed_year = int(year) if year and str(year).isdigit() else fallback_year
    
    return {
        'title': article.get('title', ''),
        'authors': article.get('authors', ''),
        'publication': publication,
        'year': parsed_year,
        'link': article.get('link', ''),
        'type': pub_type,
        'category': [],  # Can be manually categorized later
        'cited_by': article.get('cited_by', {}).get('value', 0)
    }


def load_existing_publications() -> list:
    """Load existing publications from YAML file."""
    if PUBLICATIONS_FILE.exists():
        with open(PUBLICATIONS_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or []
    return []


def save_publications(publications: list):
    """Save publications to YAML file."""
    # Sort by year (newest first)
    publications.sort(key=lambda x: x.get('year', 0) or 0, reverse=True)
    
    with open(PUBLICATIONS_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(publications, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def normalize_title(title: str) -> str:
    """Normalize title for comparison."""
    return re.sub(r'[^a-z0-9]', '', title.lower())


def find_new_publications(fetched: list, existing: list) -> list:
    """Find publications that don't exist yet."""
    existing_titles = {normalize_title(pub.get('title', '')) for pub in existing}
    
    new_pubs = []
    for pub in fetched:
        normalized = normalize_title(pub.get('title', ''))
        if normalized and normalized not in existing_titles:
            new_pubs.append(pub)
    
    return new_pubs


def sync_publications(dry_run: bool = False):
    """Main sync function."""
    if not SERPAPI_KEY:
        print("❌ Error: SERPAPI_KEY not found in .env file or environment")
        print("   Please add your API key to scripts/.env")
        return
    
    # Validate AUTHOR_ID
    if not AUTHOR_ID or len(AUTHOR_ID) < 5:
        print("❌ Error: AUTHOR_ID is missing or invalid")
        print("   Please set a valid Google Scholar author ID")
        return
    
    print(f"🔍 Fetching publications for author: {AUTHOR_ID}")
    
    # Fetch all publications (paginated)
    # Note: If there are exactly 100, 200, etc. publications, an extra empty API call may be made.
    # This is expected behavior and does not affect results.
    all_articles = []
    start = 0
    while True:
        try:
            data = fetch_scholar_publications(AUTHOR_ID, SERPAPI_KEY, start)
            articles = data.get('articles', [])
            if not articles:
                break
            all_articles.extend(articles)
            print(f"   Fetched {len(all_articles)} publications...")
            
            # Check if there are more pages
            if len(articles) < 100:
                break
            start += 100
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            if status_code == 401 or status_code == 403:
                print(f"❌ Authentication Error: Invalid API key (HTTP {status_code})")
            elif status_code == 429:
                print(f"❌ Rate Limit Error: Too many requests (HTTP 429). Please wait and try again.")
            else:
                print(f"❌ HTTP Error: {e}")
            return
        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {e}")
            return
    
    print(f"📚 Total publications found: {len(all_articles)}")
    
    # Extract publication info
    fetched_pubs = [extract_publication_info(art) for art in all_articles]
    # Filter out empty titles and publications with unreasonable years (0 or far future)
    current_year = get_current_year()
    fetched_pubs = [p for p in fetched_pubs if p['title'] and 0 < p.get('year', 0) <= current_year + 1]
    
    # Load existing
    existing_pubs = load_existing_publications()
    print(f"📂 Existing publications in YAML: {len(existing_pubs)}")
    
    # Find new ones
    new_pubs = find_new_publications(fetched_pubs, existing_pubs)
    print(f"✨ New publications to add: {len(new_pubs)}")
    
    if new_pubs:
        print("\n📝 New publications:")
        for pub in new_pubs:
            print(f"   - [{pub.get('year', '?')}] {pub['title'][:60]}...")
        
        if dry_run:
            print("\n🔸 DRY RUN - No changes made")
        else:
            # Add new publications
            existing_pubs.extend(new_pubs)
            save_publications(existing_pubs)
            print(f"\n✅ Added {len(new_pubs)} new publications to {PUBLICATIONS_FILE}")
    else:
        print("\n✅ All publications are already up to date!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sync publications from Google Scholar")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be added without making changes")
    args = parser.parse_args()
    
    sync_publications(dry_run=args.dry_run)
