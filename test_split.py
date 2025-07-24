# test_sentence_split.py
import unittest
from chunkator import sentence_split


class TestSentenceSplit(unittest.TestCase):
    """Unit tests for the sentence_split function."""

    def test_basic_sentences(self):
        """Test splitting of regular sentences with proper punctuation."""
        text = "Dr. Smith is here. She has a Ph.D. in Chemistry."
        expected = ["Dr. Smith is here.", "She has a Ph.D. in Chemistry."]
        self.assertEqual(sentence_split(text), expected)

    def test_ellipses_handling(self):
        """Test handling of ellipses in sentence splitting."""
        text = "Hello... Is it working? Yes... it is!"
        expected = ["Hello...", "Is it working?", "Yes... it is!"]
        self.assertEqual(sentence_split(text), expected)

    def test_common_abbreviations(self):
        """Test abbreviations like Mr., Prof., U.S.A. that shouldn't split sentences."""
        text = "Mr. Brown met Prof. Green. They discussed the U.S.A. case."
        expected = ["Mr. Brown met Prof. Green.", "They discussed the U.S.A. case."]
        self.assertEqual(sentence_split(text), expected)

    def test_acronyms_followed_by_sentences(self):
        """Test acronyms followed by normal sentences."""
        text = "U.S.A. is big. It has many states."
        expected = ["U.S.A. is big.", "It has many states."]
        self.assertEqual(sentence_split(text), expected)

    def test_website_urls(self):
        """Ensure website URLs like www.example.com are not split incorrectly."""
        text = "Visit www.example.com. Then send feedback."
        expected = ["Visit www.example.com.", "Then send feedback."]
        self.assertEqual(sentence_split(text), expected)

    def test_hyphenated_line_breaks(self):
        """Test merging of hyphenated line breaks across lines."""
        text = "The recom-\nmendation was accepted."
        expected = ["The recommendation was accepted."]
        self.assertEqual(sentence_split(text), expected)

    def test_initials_and_titles(self):
        """Check titles and initials are handled gracefully without breaking sentence."""
        text = "Mr. J.R.R. Tolkien wrote many books. They were popular."
        expected = ["Mr. J.R.R. Tolkien wrote many books.", "They were popular."]
        self.assertEqual(sentence_split(text), expected)

    def test_single_letter_abbreviation(self):
        """Ensure single-letter abbreviations like 'E.' are not split."""
        text = "E. coli is a bacteria. Dr. E. Stone confirmed it."
        expected = ["E. coli is a bacteria.", "Dr. E. Stone confirmed it."]
        self.assertEqual(sentence_split(text), expected)

    def test_quotes_and_dialogue(self):
        """Test punctuation with quotation marks."""
        text = 'She said, "It works!" Then she smiled.'
        expected = ['She said, "It works!"', "Then she smiled."]
        self.assertEqual(sentence_split(text), expected)

    def test_suffix_abbreviations(self):
        """Test suffixes like Ltd., Co. don't break sentences prematurely."""
        text = "Smith & Co. Ltd. is closed. We’re switching vendors."
        expected = ["Smith & Co. Ltd. is closed.", "We’re switching vendors."]
        self.assertEqual(sentence_split(text), expected)

    def test_missing_terminal_punctuation(self):
        """Handle cases where no punctuation marks end the sentence."""
        text = "This is a sentence without trailing punctuation"
        expected = ["This is a sentence without trailing punctuation"]
        self.assertEqual(sentence_split(text), expected)


if __name__ == "__main__":
    unittest.main()
