import re
import warnings
from typing import List

# Precompiled regex patterns for performance and clarity
PREFIXES = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|St)[.]")
SUFFIXES = re.compile(r"\b(?:Inc|Ltd|Jr|Sr|Co)\b")
STARTERS = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He|She|It|They|Their|Our|We|But|However|That|This|Wherever)\b")
ACRONYMS = re.compile(r"\b(?:[A-Z](?:[.][A-Z])+[.])")
WEBSITES = re.compile(r"\.(com|net|org|io|gov|edu|me)\b")
DIGITS = re.compile(r"(\d)[.](\d)")
MULTIPLE_DOTS = re.compile(r"\.{3,}")
INITIALS = re.compile(r"\b([A-Z])[.](?=[A-Z][.])")
SINGLE_INITIAL = re.compile(r"\b([A-Z])[.]")

def sentence_split(text: str) -> List[str]:
    """
    Splits a text into sentences using rule-based heuristics.
    
    Args:
        text (str): The input text.
    
    Returns:
        List[str]: List of sentences.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    try:
        # Normalize line breaks and hyphenated line wraps
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
        text = text.replace('\n', ' ')
        text = f" {text}  "  # pad for regex context

        # Protect known non-boundary dots
        text = PREFIXES.sub(lambda m: m.group().replace('.', '<prd>'), text)
        text = WEBSITES.sub(r"<prd>\1", text)
        text = DIGITS.sub(r"\1<prd>\2", text)
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")

        # Handle ellipses
        text = MULTIPLE_DOTS.sub("<ellip><stop>", text)

        # Handle acronyms and initials
        text = ACRONYMS.sub(lambda m: m.group().replace('.', '<prd>'), text)
        text = INITIALS.sub(r"\1<prd>", text)
        text = SINGLE_INITIAL.sub(r"\1<prd>", text)

        # Handle suffixes followed by sentence starters
        text = re.sub(
            rf" {SUFFIXES.pattern}[.] (?={STARTERS.pattern})",
            "<prd><stop>", text
        )
        text = SUFFIXES.sub(lambda m: m.group().replace('.', '<prd>'), text)

        # Fix punctuation inside quotes
        text = re.sub(r'([.!?])”', r'”\1', text)
        text = re.sub(r'([.!?])"', r'"\1', text)

        # Mark sentence boundaries
        text = text.replace('.', '.<stop>')
        text = text.replace('?', '?<stop>')
        text = text.replace('!', '!<stop>')

        # Restore placeholders
        text = text.replace('<prd>', '.')
        text = text.replace('<ellip>', '...')

        # Final split and cleanup
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
        "E. coli is common. Mr. J.R.R. Tolkien wrote many books."
    )
    for i, sentence in enumerate(sentence_split(sample_text), 1):
        print(f"{i}. {sentence}")
