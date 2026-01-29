#!/usr/bin/env python3
"""Extract COMPLETE job data from PDFs - NO TRUNCATION."""

import os
import sys
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    os.system("pip3 install PyPDF2")
    import PyPDF2

def extract_full_text(pdf_path):
    """Extract ALL text from PDF - complete extraction."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def main():
    temp_dir = Path("temp_jobs_data")
    
    # Process each PDF and output complete content
    pdfs = {
        "phenomenological_fr": "Offre_Stage_Analyses_Phenomenologiques_FR.pdf",
        "phenomenological_en": "Internship_Offer_Phenomenological_Analysis_EN.pdf",
        "ios_fr": "Offre_Stage_Developpeur_iOS_PPSP_FR.pdf",
        "ios_en": "Offre_Stage_Developpeur_iOS_PPSP_EN.pdf",
        "python_fr": "Offre_Stage_PPSP_Developpeur_Python_HyPyP_FR.pdf",
        "python_en": "Offre_Stage_PPSP_Python_Developer_HyPyP_EN.pdf",
        "psychology_fr": "Offre_Stage_PPSP_Psychologie_FR.pdf",
        "psychology_en": "Offre_Stage_PPSP_Psychology_EN.pdf",
    }
    
    for key, filename in pdfs.items():
        pdf_path = temp_dir / filename
        if pdf_path.exists():
            print(f"\n{'='*80}")
            print(f"### {key.upper()}: {filename}")
            print('='*80)
            text = extract_full_text(pdf_path)
            print(text)  # Print EVERYTHING
            print('\n')

if __name__ == "__main__":
    main()
