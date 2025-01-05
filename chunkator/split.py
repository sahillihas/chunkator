import re

# Regular expression patterns for different text components
alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\\s|She\\s|It\\s|They\\s|Their\\s|Our\\s|We\\s|But\\s|However\\s|That\\s|This\\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\\.{2,}'

def sentence_split(text: str) -> list[str]:
    """
    Splits the input text into a list of sentences based on punctuation and special rules.

    Args:
    text (str): The input text to be split.

    Returns:
    list[str]: A list of sentences.
    """
    # Add spaces to ensure correct processing of the text
    text = " " + text + "  "
    text = text.replace("\n", " ")  # Replace newlines with spaces
    
    # Handle common abbreviations and patterns
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    
    # Handle specific cases like "Ph.D."
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")

    # Handle alphabetic abbreviations and acronyms
    text = re.sub("\\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.][.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.][.]", "\\1<prd>\\2<prd>", text)
    
    # Handle suffixes and special starters
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)

    # Handle punctuation with quotes
    if "”" in text:
        text = text.replace(".”", "”.")
    if "\"" in text:
        text = text.replace(".\"", "\".")
    if "!" in text:
        text = text.replace("!\"", "\"!")
    if "?" in text:
        text = text.replace("?\"", "\"?")
    
    # Add sentence stops
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    
    # Replace placeholders with actual periods
    text = text.replace("<prd>", ".")
    
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences

# Example usage
if __name__ == "__main__":
    sample_text = "Dr. Smith is here. She has a Ph.D. in Chemistry. Hello... Is it working? Yes!"
    print(sentence_split(sample_text))
