import re

# ReGeX patterns for different text components
alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\\s|She\\s|It\\s|They\\s|Their\\s|Our\\s|We\\s|But\\s|However\\s|That\\s|This\\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'  # fixed escaping

def sentence_split(text: str) -> list[str]:
    """
    Splits the input text into a list of sentences based on punctuation and special rules,
    including rejoining hyphenated words split across lines.
    """
    # Preprocessing
    text = text.replace("\n", " ")  # Replace newlines with spaces
    
    # Handle hyphenated line breaks: remove hyphen and join words
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
    
    text = " " + text + "  "
    
    # Handle common abbreviations and patterns
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    
    text = re.sub("\\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.][.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.][.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)

    # Punctuation with quotes
    text = text.replace(".”", "”.")
    text = text.replace(".\"", "\".")
    text = text.replace("!\"", "\"!")
    text = text.replace("?\"", "\"?")
    
    # Sentence stops
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    
    # Replace placeholders
    text = text.replace("<prd>", ".")
    
    # Final sentence list
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences

# Example usage
if __name__ == "__main__":
    sample_text = """Dr. Smith is here. She has a Ph.D. in Chemistry.
The recom-
mendation was ignored. Hello... Is it working? Yes!"""
    print(sentence_split(sample_text))
