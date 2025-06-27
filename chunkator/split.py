import re
import warnings
from typing import List

# Regex components (with improved boundary handling)
alphabets = r"([A-Za-z])"
prefixes = r"\b(?:Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt)[.]"
suffixes = r"\b(?:Inc|Ltd|Jr|Sr|Co)\b"
starters = r"\b(?:Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He|She|It|They|Their|Our|We|But|However|That|This|Wherever)\b"
acronyms = r"\b(?:[A-Z](?:[.][A-Z])+[.])"
websites = r"[.](?:com|net|org|io|gov|edu|me)"
digits = r"([0-9])"
multiple_dots = r"\.{3,}"


def sentence_split(text: str) -> List[str]:
    """
    Splits input text into sentences using rule-based heuristics.
    Includes error handling for robustness.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    try:
        # Join hyphenated words split across lines
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)

        # Normalize line breaks
        text = text.replace("\n", " ")

        # Pad text to simplify boundary handling
        text = " " + text + "  "

        # Protect common patterns
        text = re.sub(prefixes, lambda m: m.group(0).replace(".", "<prd>"), text)
        text = re.sub(websites, r"<prd>\1", text)
        text = re.sub(digits + r"[.]" + digits, r"\1<prd>\2", text)
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")

        # Ellipses: replace with marker and <stop>
        text = re.sub(multiple_dots, "<ellip><stop>", text)

        # Acronyms and initials
        text = re.sub(acronyms + r" " + starters, lambda m: m.group(0).replace(".", "<prd>").replace(" ", "<stop> "), text)
        text = re.sub(r"\b([A-Z])[.]([A-Z])[.]", r"\1<prd>\2<prd>", text)
        text = re.sub(r"\b([A-Z])[.]", r"\1<prd>", text)

        # Suffix handling
        text = re.sub(r" " + suffixes + r"[.] " + starters, r" \1<stop> \2", text)
        text = re.sub(r" " + suffixes + r"[.]", r" \1<prd>", text)

        # Handle single-letter abbreviations like E. coli
        text = re.sub(r"\s" + alphabets + r"[.] ", r" \1<prd> ", text)
        text = re.sub(r" " + alphabets + r"[.]", r" \1<prd>", text)

        # Quote-safe punctuation
        text = re.sub(r'([.!?])”', r'”\1', text)
        text = re.sub(r'([.!?])"', r'"\1', text)

        # Mark sentence boundaries
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")

        # Restore special placeholders
        text = text.replace("<prd>", ".")
        text = text.replace("<ellip>", "...")

        # Final split
        sentences = text.split("<stop>")
        return [s.strip() for s in sentences if s.strip()]

    except re.error as regex_err:
        warnings.warn(f"Regex processing failed: {regex_err}")
        return [text.strip()]  # Return the original text as one sentence fallback

    except Exception as e:
        warnings.warn(f"Unexpected error in sentence splitting: {e}")
        return []  # Return empty if unrecoverable


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
