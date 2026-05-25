# Run this to see capybara mention density per file
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

for filepath in sorted(DATA_DIR.glob("*.txt")):
    text = filepath.read_text(encoding='utf-8')
    words = len(text.split())
    
    # Count mentions (case insensitive)
    capybara_mentions = text.lower().count('capybara')
    
    # Mentions per 1000 words — density metric
    density = (capybara_mentions / words) * 1000
    
    print(f"{filepath.name:<45} {words:>6} words | {capybara_mentions:>3} mentions | {density:>5.1f} per 1000 words")