import re
from typing import List

# Regex components
alphabets = r"([A-Za-z])"
prefixes = r"(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt)[.]"
suffixes = r"(Inc|Ltd|Jr|Sr|Co)"
starters = r"(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = r"([A-Z][.](?:[A-Z][.])+)"  # e.g., U.S.A.
websites = r"[.](com|net|org|io|gov|edu|me)"
digits = r"([0-9])"
multiple_dots = r"\.{2,}"


def sentence_split(text: str) -> List[str]:
    """
    Splits input text into sentences using rule-based heuristics.
    Handles abbreviations, initials, websites, ellipses, and hyphenated line breaks.
    """

    # Rejoin hyphenated words split across lines
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)

    # Replace newlines with spaces
    text = text.replace("\n", " ")

    # Pad text
    text = " " + text + "  "

    # Abbreviation and website protection
    text = re.sub(prefixes, r"\1<prd>", text)
    text = re.sub(websites, r"<prd>\1", text)
    text = re.sub(digits + r"[.]" + digits, r"\1<prd>\2", text)

    # Ellipsis and multi-dot
    text = re.sub(multiple_dots, lambda m: "<prd>" * len(m.group(0)) + "<stop>", text)

    # Handle Ph.D.
    text = text.replace("Ph.D.", "Ph<prd>D<prd>")

    # Initials like A.B.C.
    text = re.sub(r"\b([A-Z])[.]([A-Z])[.]", r"\1<prd>\2<prd>", text)
    text = re.sub(r"\b([A-Z])[.]", r"\1<prd>", text)

    # Acronyms followed by sentence starters
    text = re.sub(acronyms + r" " + starters, r"\1<stop> \2", text)

    # Two dots in a row with alphabet, e.g., A..B.
    text = re.sub(r"([A-Za-z])[.][.]([A-Za-z])[.]", r"\1<prd><prd>\2<prd>", text)
    text = re.sub(r"([A-Za-z])[.][.]", r"\1<prd><prd>", text)

    # Suffixes and starters
    text = re.sub(r" " + suffixes + r"[.] " + starters, r" \1<stop> \2", text)
    text = re.sub(r" " + suffixes + r"[.]", r" \1<prd>", text)

    # Single letter abbreviations (e.g., E. coli)
    text = re.sub(r"\s" + alphabets + r"[.] ", r" \1<prd> ", text)
    text = re.sub(r" " + alphabets + r"[.]", r" \1<prd>", text)

    # Quote-safe punctuation replacements
    text = text.replace(".”", "”.")
    text = text.replace(".\"", "\".")
    text = text.replace("!\"", "\"!")
    text = text.replace("?\"", "\"?")

    # Mark sentence boundaries
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")

    # Restore protected periods
    text = text.replace("<prd>", ".")

    # Final sentence list
    sentences = text.split("<stop>")
    return [s.strip() for s in sentences if s.strip()]


# Example usage
if __name__ == "__main__":
    sample_text = """
    Dr. Smith has a Ph.D. in Chemistry... She said, "It’s working!" Visit www.example.com for more info.
    The recom-
    mendation was ignored. U.S.A. is big. E. coli is common. Mr. J.R.R. Tolkien wrote many books.
    """
    result = sentence_split(sample_text)
    for i, s in enumerate(result, 1):
        print(f"{i}. {s}")
