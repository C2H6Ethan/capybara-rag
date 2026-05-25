import wikipediaapi
import os
import time
from pathlib import Path

# Define project root and data directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Wikipedia API
# First argument is your app name - Wikipedia asks you to identify yourself
# Second argument is the language
wiki = wikipediaapi.Wikipedia(
    user_agent='CapybaraRAG/1.0 (github.com/yourusername/capybara-rag)',
    language='en'
)

# Curated list of articles - each tuple is (wikipedia_title, filename, reason)
ARTICLES = [
    # Core capybara articles
    ("Capybara",                    "capybara_main.txt",          "main article"),
    ("Hydrochoerus",                "capybara_genus.txt",         "genus, more scientific depth"),
    ("Hydrochoerus isthmius",       "capybara_lesser.txt",        "close relative, good comparison"),
    
    # Habitats
    ("Pantanal",                    "habitat_pantanal.txt",       "primary habitat"),
    ("Llanos",                      "habitat_llanos.txt",         "secondary habitat"),
    ("Orinoco",                     "habitat_orinoco.txt",        "major capybara habitat river"),
    
    # Predators
    ("Jaguar",                      "predator_jaguar.txt",        "primary predator"),
    ("Green anaconda",              "predator_anaconda.txt",      "primary predator"),
    ("Spectacled caiman",           "predator_caiman.txt",        "primary predator"),
    
    # Ecosystem neighbors
    ("Giant otter",                 "neighbor_giant_otter.txt",   "shares exact habitat, interacts with capybaras"),
    ("Marsh deer",                  "neighbor_marsh_deer.txt",    "shares habitat, coexists with capybaras"),

    # Biological context
    ("Exotic pet",                  "context_exotic_pet.txt",     "legal and ownership context"),
]


def fetch_article(title):
    """
    Fetch a Wikipedia article and return its full text.
    Returns None if article doesn't exist.
    """
    print(f"Fetching: {title}...")
    
    page = wiki.page(title)
    
    if not page.exists():
        print(f"  WARNING: '{title}' not found on Wikipedia")
        return None
    
    # page.text gives us clean plain text - no HTML, no markup
    # This is why we use the API instead of scraping - it does the cleaning for us
    return page.text


def check_quality(text, filename):
    """
    Basic quality check on fetched text.
    Prints stats so you can verify the data looks right.
    """
    word_count = len(text.split())
    char_count = len(text)
    
    print(f"  Characters: {char_count:,}")
    print(f"  Words: {word_count:,}")
    print(f"  Preview: {text[:150].strip()}...")
    
    # Flag suspiciously short articles
    if word_count < 500:
        print(f"  WARNING: Very short article, might be a stub")
    else:
        print(f"  Quality: OK")


def save_article(text, filename):
    """
    Save article text to data/raw/ directory.
    """
    filepath = DATA_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"  Saved to: data/raw/{filename}")


def collect_all_articles():
    """
    Main function - fetches all articles in our curated list,
    checks quality, and saves them.
    """
    print(f"Starting data collection")
    print(f"Saving to: {DATA_DIR}")
    print(f"Articles to fetch: {len(ARTICLES)}\n")
    
    successful = []
    failed = []
    
    for title, filename, reason in ARTICLES:
        print(f"--- {title} ({reason}) ---")
        
        # Fetch the article
        text = fetch_article(title)
        
        if text is None:
            failed.append(title)
            print()
            continue
        
        # Check quality
        check_quality(text, filename)
        
        # Save it
        save_article(text, filename)
        successful.append(title)
        
        print()
        
        # Be polite - wait 1 second between requests
        # Wikipedia asks scrapers not to hammer their servers
        time.sleep(1)
    
    # Summary
    print("=" * 50)
    print(f"DONE")
    print(f"Successfully fetched: {len(successful)}/{len(ARTICLES)}")
    
    if failed:
        print(f"Failed: {failed}")
    
    print(f"\nFiles saved to: {DATA_DIR}")


if __name__ == "__main__":
    collect_all_articles()