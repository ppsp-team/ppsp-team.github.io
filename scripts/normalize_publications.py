#!/usr/bin/env python3
"""
Normalize publication data - unify author names, journal titles formatting.
"""

import yaml
import re
from pathlib import Path

PUBLICATIONS_FILE = Path(__file__).parent.parent / '_data' / 'publications.yml'

# Common compound last name prefixes
COMPOUND_PREFIXES = {'van', 'von', 'de', 'la', 'del', 'der', 'di', 'da', 'dos', 'das', 'le', 'du', 'den'}


def normalize_authors(authors: str) -> str:
    """Normalize author names to consistent format: First Initial. Last Name"""
    if not authors:
        return authors
    
    # Clean up extra spaces
    authors = re.sub(r'\s+', ' ', authors.strip())
    
    # Split by comma to get individual authors
    author_list = [a.strip() for a in authors.split(',')]
    normalized = []
    
    for author in author_list:
        if not author:
            continue
        
        # Skip if already in "X. Lastname" format (handles multiple initials like "J.P. Smith" or "A. B. Jones")
        # Also handles hyphenated last names like "J. Smith-Jones"
        if re.match(r'^([A-Z]\.\s*)+[A-Za-z-]+$', author):
            normalized.append(author)
            continue
        
        # Split name into parts
        parts = author.split()
        if len(parts) >= 2:
            # Check for compound last names (van, von, de, etc.)
            # Find where the last name starts by looking for compound prefixes
            lastname_start = len(parts) - 1
            for i in range(len(parts) - 1, 0, -1):
                if parts[i - 1].lower() in COMPOUND_PREFIXES:
                    lastname_start = i - 1
                else:
                    break
            
            # Everything before lastname_start is first names, everything from there is last name
            firstnames = parts[:lastname_start]
            lastname = ' '.join(parts[lastname_start:])
            
            if firstnames:
                # Convert first names to initials
                initials = ' '.join([f"{n[0]}." for n in firstnames if n])
                normalized.append(f"{initials} {lastname}")
            else:
                normalized.append(author)
        else:
            normalized.append(author)
    
    return ', '.join(normalized)


def normalize_journal(journal: str) -> str:
    """Normalize journal names - proper capitalization."""
    if not journal:
        return journal
    
    journal = journal.strip()
    
    # Common journal name corrections
    corrections = {
        'Biological psychiatry': 'Biological Psychiatry',
        'Nature reviews disease primers': 'Nature Reviews Disease Primers',
        'Frontiers in psychology': 'Frontiers in Psychology',
        'Frontiers in psychiatry': 'Frontiers in Psychiatry',
        'Frontiers in neuroscience': 'Frontiers in Neuroscience',
        'Frontiers in neuroergonomics': 'Frontiers in Neuroergonomics',
        'Molecular autism': 'Molecular Autism',
        'Plos computational biology': 'PLoS Computational Biology',
        'Science advances': 'Science Advances',
        'Science translational medicine': 'Science Translational Medicine',
        'Neural computation': 'Neural Computation',
        'Social cognitive and affective neuroscience': 'Social Cognitive and Affective Neuroscience',
        'Journal of sleep research': 'Journal of Sleep Research',
        'Sleep medicine reviews': 'Sleep Medicine Reviews',
        'Arxiv': 'ArXiv',
        'Biorxiv': 'bioRxiv',
        'Medrxiv': 'medRxiv',
        'Psyarxiv': 'PsyArXiv',
    }
    
    for wrong, correct in corrections.items():
        if journal.lower() == wrong.lower():
            return correct
    
    return journal


def normalize_type(pub_type: str) -> str:
    """Normalize publication type."""
    if not pub_type:
        return 'Journal Paper'
    
    # Fix typos/variations
    corrections = {
        'Journal paper': 'Journal Paper',
        'journal paper': 'Journal Paper', 
        'Poster_conference': 'Poster_Conference',
        'poster_conference': 'Poster_Conference',
        'book_chapter': 'Book_Chapter',
        'preprint': 'Preprint',
    }
    
    return corrections.get(pub_type, pub_type)


def normalize_publications():
    """Main normalization function."""
    if not PUBLICATIONS_FILE.exists():
        print(f"❌ File not found: {PUBLICATIONS_FILE}")
        return
    
    with open(PUBLICATIONS_FILE, 'r', encoding='utf-8') as f:
        pubs = yaml.safe_load(f)
    
    if not pubs:
        print("❌ No publications found")
        return
    
    print(f"📚 Normalizing {len(pubs)} publications...")
    
    changes = 0
    for pub in pubs:
        # Normalize authors
        old_authors = pub.get('authors', '')
        new_authors = normalize_authors(old_authors)
        if old_authors != new_authors:
            pub['authors'] = new_authors
            changes += 1
        
        # Normalize journal
        old_journal = pub.get('publication', '')
        new_journal = normalize_journal(old_journal)
        if old_journal != new_journal:
            pub['publication'] = new_journal
            print(f"   📖 {old_journal} → {new_journal}")
            changes += 1
        
        # Normalize type
        old_type = pub.get('type', '')
        new_type = normalize_type(old_type)
        if old_type != new_type:
            pub['type'] = new_type
            print(f"   📄 Type: {old_type} → {new_type}")
            changes += 1
    
    # Sort by year (newest first)
    pubs.sort(key=lambda x: x.get('year', 0) or 0, reverse=True)
    
    # Save
    with open(PUBLICATIONS_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(pubs, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"\n✅ Done! Made {changes} corrections.")


if __name__ == "__main__":
    normalize_publications()
