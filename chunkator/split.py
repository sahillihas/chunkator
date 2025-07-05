import re
import warnings
from typing import List

# Precompile regex patterns
PREFIXES = re.compile(r"\b(?:Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt)[.]")
SUFFIXES = re.compile(r"\b(?:Inc|Ltd|Jr|Sr|Co)\b")
STARTERS = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He|She|It|They|Their|Our|We|But|However|That|This|Wherever)\b")
ACRONYMS = re.compile(r"\b(?:[A-Z](?:[.][A-Z])+[.])")
WEBSITES = re.compile(r"\.(com|net|org|io|gov|edu|me)")
DIGITS = re.compile(r"(\d)[.](\d)")
MULTIPLE_DOTS = re.compile(r"\.{3,}")
INITIALS = re.compile(r"\b([A-Z])[.](?=[A-Z][.])")
SINGLE_INITIAL = re.compile(r"\b([A-Z])[.]")

def sentence_split(text: str) -> List[str]:
    """
    Splits input text into sentences using rule-based heuristics.
    Returns a list of sentence strings.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    try:
        # Step 1: Clean and normalize
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)  # recom- mendation → recommendation
        text = text.replace("\n", " ")
        text = f" {text}  "

        # Step 2: Protect known non-boundary patterns
        text = PREFIXES.sub(lambda m: m.group(0).replace(".", "<prd>"), text)
        text = WEBSITES.sub(r"<prd>\1", text)
        text = DIGITS.sub(r"\1<prd>\2", text)
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")

        # Step 3: Handle ellipses
        text = MULTIPLE_DOTS.sub("<ellip><stop>", text)

        # Step 4: Acronyms, initials
        text = ACRONYMS.sub(lambda m: m.group(0).replace(".", "<prd>"), text)
        text = INITIALS.sub(r"\1<prd>", text)
        text = SINGLE_INITIAL.sub(r"\1<prd>", text)

        # Step 5: Suffix handling
        text = re.sub(r" " + SUFFIXES.pattern + r"[.] (?=" + STARTERS.pattern + ")", r"<prd><stop>", text)
        text = SUFFIXES.sub(lambda m: m.group(0).replace(".", "<prd>"), text)

        # Step 6: Fix quotes around punctuation
        text = re.sub(r'([.!?])”', r'”\1', text)
        text = re.sub(r'([.!?])"', r'"\1', text)

        # Step 7: Sentence boundary markers
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")

        # Step 8: Restore placeholders
        text = text.replace("<prd>", ".")
        text = text.replace("<ellip>", "...")

        # Step 9: Final sentence split
        sentences = [s.strip() for s in text.split("<stop>") if s.strip()]
        return sentences

    except re.error as regex_err:
        warnings.warn(f"[Regex Error] Failed during sentence splitting: {regex_err}")
        return [text.strip()]

    except Exception as e:
        warnings.warn(f"[Unexpected Error] Sentence splitting failed: {e}")
        return []


# Example usage
if __name__ == "__main__":
    sample_text = """
    Dr. Smith has a Ph.D. in Chemistry... She said, "It’s working!" Visit www.example.com for more info.
    The recom-
    mendation was ignored. U.S.A. is big. E. coli is common. Mr. J.R.R. Tolkien wrote many books.
    """
    result = sentence_split(sample_text)
    for i, sentence in enumerate(result, 1):
        print(f"{i}. {sentence}")
