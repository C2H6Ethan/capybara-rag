from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
FILTERED_DIR = PROJECT_ROOT / "data" / "filtered"
FILTERED_DIR.mkdir(parents=True, exist_ok=True)

# Terms that indicate capybara relevance
RELEVANCE_TERMS = [
    'capybara', 'capybaras', 'hydrochoerus',
    'giant rodent', 'largest rodent'
]

# Files to filter (low density but potentially useful)
FILES_TO_FILTER = [
    'predator_jaguar.txt',
    'predator_anaconda.txt',
    'habitat_pantanal.txt',
    'context_exotic_pet.txt',
    'habitat_llanos.txt',
    'iucn_capybara_redlist.txt',
]

# Files to copy as-is (already high density, no filtering needed)
FILES_TO_KEEP = [
    'capybara_main.txt',
    'capybara_lesser.txt',
    'capybara_genus.txt',
    'animaldiversity_capybara.txt',
    'animaldiversity_hydrochoerinae.txt',
    'britannica_capybara.txt',
    'nationalgeographic_capybara.txt',
    'thesprucepets_capybara.txt',
    'a-z-animals.txt',
    'rainforest-alliance.txt',
    'worldwildlife.txt',
]


def is_relevant_paragraph(paragraph):
    """
    Returns True if paragraph contains any capybara-related terms.
    We check lowercase to catch all capitalizations.
    """
    paragraph_lower = paragraph.lower()
    return any(term in paragraph_lower for term in RELEVANCE_TERMS)


def filter_file(filename):
    """
    Reads a file, splits into paragraphs, keeps only relevant ones.
    Saves filtered version to data/filtered/
    """
    filepath = DATA_DIR / filename

    if not filepath.exists():
        print(f"  SKIP: {filename} not found")
        return

    text = filepath.read_text(encoding='utf-8')

    # Split into paragraphs on double newlines
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    # Filter to only relevant paragraphs
    relevant = [p for p in paragraphs if is_relevant_paragraph(p)]

    total = len(paragraphs)
    kept = len(relevant)

    if kept == 0:
        print(f"  {filename}: {total} paragraphs, 0 relevant — SKIPPING FILE")
        return

    # Join back with double newlines
    filtered_text = '\n\n'.join(relevant)

    # Save to filtered directory
    output_path = FILTERED_DIR / filename
    output_path.write_text(filtered_text, encoding='utf-8')

    print(f"  {filename}: kept {kept}/{total} paragraphs ({len(filtered_text.split())} words)")


def copy_file(filename):
    """
    Copies high-density files as-is to filtered directory.
    """
    filepath = DATA_DIR / filename

    if not filepath.exists():
        print(f"  SKIP: {filename} not found")
        return

    text = filepath.read_text(encoding='utf-8')
    output_path = FILTERED_DIR / filename
    output_path.write_text(text, encoding='utf-8')

    words = len(text.split())
    print(f"  {filename}: copied as-is ({words} words)")


if __name__ == "__main__":
    print("=== Filtering low-density files ===")
    for filename in FILES_TO_FILTER:
        filter_file(filename)

    print("\n=== Copying high-density files ===")
    for filename in FILES_TO_KEEP:
        copy_file(filename)

    print(f"\nFiltered data saved to: {FILTERED_DIR}")

    # Run density check on filtered files
    print("\n=== Density check on filtered corpus ===")
    for filepath in sorted(FILTERED_DIR.glob("*.txt")):
        text = filepath.read_text(encoding='utf-8')
        words = len(text.split())
        mentions = text.lower().count('capybara')
        density = (mentions / words) * 1000 if words > 0 else 0
        print(f"  {filepath.name:<45} {words:>5} words | {mentions:>3} mentions | {density:>5.1f} per 1000 words")