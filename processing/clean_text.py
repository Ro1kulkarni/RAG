import re
from bs4 import BeautifulSoup
from textwrap import dedent

RAW_FILE = "C:/Ro1/Test/loan-product-assistant/data/raw/scraped_data.html"
OUTPUT = "C:/Ro1/Test/loan-product-assistant/data/processed/knowledge_base.txt"


# ---------------------------------------------------------
# 1. LOAD HTML AS TEXT
# ---------------------------------------------------------

def load_html_to_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    return text


# ---------------------------------------------------------
# 2. REMOVE URLS + HEADERS
# ---------------------------------------------------------

def remove_headers_and_urls(text):
    text = re.sub(r"=+", "", text)                  # ====== separators
    text = re.sub(r"URL:.*", "", text)             # URL: ....
    text = re.sub(r"https?://\S+", "", text)       # Remove any http link
    return text


# ---------------------------------------------------------
# 3. REMOVE UI JUNK / NOISE
# ---------------------------------------------------------

def remove_ui_noise(text):
    noise_patterns = [
        r"Click here.*",
        r"SHOW EMI.*",
        r"Scan this Code.*",
        r"Please click.*",
        r"Follow the step.*",
        r"How to Apply for Digital Loans Online.*",
        r"EMI Calculator.*",
        r"Check Eligibility.*",
        r"www\..*",
    ]
    for pat in noise_patterns:
        text = re.sub(pat, "", text, flags=re.IGNORECASE)
    return text


# ---------------------------------------------------------
# 4. REMOVE SHORT FORMS
# ---------------------------------------------------------

def remove_short_forms(text):
    return re.sub(r"\s*\([^)]*\)", "", text)


# ---------------------------------------------------------
# 5. CLEAN BULLET POINTS
# ---------------------------------------------------------

def clean_bullet_points(text):
    text = re.sub(r"\n\s*\*", "\n- ", text)
    text = re.sub(r"\n\s*[•–]\s*", "\n- ", text)
    return text


# ---------------------------------------------------------
# 6. NORMALIZE & CLEAN SPACES
# ---------------------------------------------------------

def normalize_spaces(text):
    text = dedent(text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# ---------------------------------------------------------
# 7. REMOVE DUPLICATE LINES
# ---------------------------------------------------------

def remove_duplicate_lines(text):
    seen = set()
    result = []
    for line in text.split("\n"):
        cleaned = line.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(line)
    return "\n".join(result)


# ---------------------------------------------------------
# 8. REMOVE HEADINGS + SPECIAL SYMBOLS (ADDED HERE)
# ---------------------------------------------------------

def deep_clean_text(text):
    final_lines = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        # Remove markdown headings (#, ##, ###)
        if re.match(r"^#{1,6}\s*", line):
            continue

        # Remove FAQ related text
        if "faq" in line.lower() or "frequently asked" in line.lower():
            continue

        # Remove bullets like "-" ":" at start
        line = re.sub(r"^[-:]\s*", "", line)

        # Remove short forms
        line = remove_short_forms(line)

        # -----------------------------------------
        # REMOVE SPECIAL SYMBOLS (YOUR REQUIREMENT)
        # -----------------------------------------
        line = re.sub(r"[:,/.\-*\%()?\&|]", " ", line)
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            final_lines.append(line)

    return "\n".join(final_lines)


# ---------------------------------------------------------
# 9. FULL CLEANING PIPELINE
# ---------------------------------------------------------

def clean_pipeline():
    raw = load_html_to_text(RAW_FILE)

    text = raw
    text = remove_headers_and_urls(text)
    text = remove_ui_noise(text)
    text = clean_bullet_points(text)
    text = normalize_spaces(text)
    text = remove_duplicate_lines(text)
    text = deep_clean_text(text)
    text = normalize_spaces(text)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(text)

    print("✔ Cleaning complete!")
    print(f"✔ Clean knowledge base saved to: {OUTPUT}")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":
    clean_pipeline()