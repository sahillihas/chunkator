import re
import warnings
from typing import List

# Precompiled regex patterns
PREFIXES = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|St)\.")
SUFFIXES = re.compile(r"\b(?:Inc|Ltd|Jr|Sr|Co)\.")
STARTERS = re.compile(
    r"\b(?:Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He|She|It|They|Their|Our|We|But|However|That|This|Wherever)\b"
)
ACRONYMS = re.compile(r"\b(?:[A-Z]\.){2,}(?:[A-Z]\.?)?")
WEBSITES = re.compile(r"\b(?:[\w\-]+\.)+(?:com|net|org|io|gov|edu|me)(?=\b|/)")
DIGITS = re.compile(r"(\d)\.(\d)")
MULTIPLE_DOTS = re.compile(r"\.{3,}")
INITIALS = re.compile(r"\b([A-Z])\.(?=[A-Z]\.)")
SINGLE_INITIAL = re.compile(r"\b([A-Z])\.")
ABBREVIATIONS = re.compile(r'\b(?:e\.g|i\.e|etc)\.')
COMMON_ABBR = re.compile(r'\b(?:No\.|vs\.|Rs\.)')

def sentence_split(text: str) -> List[str]:
    """
    Splits a text into sentences using rule-based heuristics.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    try:
        # Normalize and pad
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)  # Fix hyphenated line breaks
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = f" {text.strip()}  "

        # Protect non-boundary dots with <prd>
        text = PREFIXES.sub(lambda m: m.group().replace('.', '<prd>'), text)
        text = SUFFIXES.sub(lambda m: m.group().replace('.', '<prd>'), text)
        text = WEBSITES.sub(lambda m: m.group().replace('.', '<prd>'), text)
        text = DIGITS.sub(r"\1<prd>\2", text)
        text = re.sub(r'\bPh\.D\.?', 'Ph<prd>D<prd>', text)
        text = ABBREVIATIONS.sub(lambda m: m.group().replace('.', '<prd>'), text)
        text = COMMON_ABBR.sub(lambda m: m.group().replace('.', '<prd>'), text)

        # Ellipses (e.g. "...")
        text = MULTIPLE_DOTS.sub('<ellip><stop>', text)

        # Acronyms and initials (e.g., U.S.A. or J.R.R.)
        text = ACRONYMS.sub(lambda m: m.group().replace('.', '<prd>'), text)
        text = INITIALS.sub(r"\1<prd>", text)
        text = SINGLE_INITIAL.sub(r"\1<prd>", text)
        text = re.sub(r'\b([A-Z])<prd> ([A-Z])<prd>', r'\1<prd>\2<prd>', text)

        # Suffixes followed by sentence starters
        text = re.sub(
            r'\b(?:Inc|Ltd|Jr|Sr|Co)<prd> (?=' + STARTERS.pattern + ')',
            '<prd><stop>', text
        )

        # Punctuation followed by quotes (e.g., ." or !')
        text = re.sub(r'([.!?])("|\')', r'\1\2<stop>', text)

        # Sentence boundaries
        text = text.replace('.', '.<stop>')
        text = text.replace('?', '?<stop>')
        text = text.replace('!', '!<stop>')

        # Restore protected tokens
        text = text.replace('<prd>', '.')
        text = text.replace('<ellip>', '...')

        # Final split
        return [s.strip() for s in text.split('<stop>') if s.strip()]

    except re.error as regex_err:
        warnings.warn(f"[Regex Error] Sentence splitting failed: {regex_err}")
        return [text.strip()]

    except Exception as e:
        warnings.warn(f"[Unexpected Error] Sentence splitting failed: {e}")
        return []

# Example usage
if __name__ == "__main__":
    sample_text = (
        "Dr. Smith has a Ph.D. in Chemistry... She said, \"It’s working!\" "
        "Visit www.example.com for more info. "
        "The recom-\nmendation was ignored. U.S.A. is big. "
        "E. coli is common. Mr. J.R.R. Tolkien wrote many books. "
        "Examples include e.g. Multani Mitti, i.e. Fuller’s Earth. "
        "No. 1 on the list was Bhringraj."
    )
    for i, sentence in enumerate(sentence_split(sample_text), 1):
        print(f"{i}. {sentence}")
