# Unit Tests
import unittest
from chunkator import sentence_split

class TestSentenceSplit(unittest.TestCase):

    def test_basic_split(self):
        text = "Dr. Smith is here. She has a Ph.D. in Chemistry."
        expected = ["Dr. Smith is here.", "She has a Ph.D. in Chemistry."]
        self.assertEqual(sentence_split(text), expected)

    def test_multiple_ellipses(self):
        text = "Hello... Is it working? Yes... it is!"
        expected = ["Hello...", "Is it working?", "Yes... it is!"]
        self.assertEqual(sentence_split(text), expected)

    def test_abbreviations(self):
        text = "Mr. Brown met Prof. Green. They discussed the U.S.A. case."
        expected = ["Mr. Brown met Prof. Green.", "They discussed the U.S.A. case."]
        self.assertEqual(sentence_split(text), expected)

    def test_acronyms_with_starters(self):
        text = "U.S.A. is big. It has many states."
        expected = ["U.S.A. is big.", "It has many states."]
        self.assertEqual(sentence_split(text), expected)

    def test_website_handling(self):
        text = "Visit www.example.com. Then send feedback."
        expected = ["Visit www.example.com.", "Then send feedback."]
        self.assertEqual(sentence_split(text), expected)

    def test_hyphenated_line_breaks(self):
        text = "The recom-\nmendation was accepted."
        expected = ["The recommendation was accepted."]
        self.assertEqual(sentence_split(text), expected)

    def test_initials_and_titles(self):
        text = "Mr. J.R.R. Tolkien wrote many books. They were popular."
        expected = ["Mr. J.R.R. Tolkien wrote many books.", "They were popular."]
        self.assertEqual(sentence_split(text), expected)

    def test_single_letter_abbreviation(self):
        text = "E. coli is a bacteria. Dr. E. Stone confirmed it."
        expected = ["E. coli is a bacteria.", "Dr. E. Stone confirmed it."]
        self.assertEqual(sentence_split(text), expected)

    def test_quote_handling(self):
        text = 'She said, "It works!" Then she smiled.'
        expected = ['She said, "It works!"', "Then she smiled."]
        self.assertEqual(sentence_split(text), expected)

    def test_suffix_handling(self):
        text = "Smith & Co. Ltd. is closed. We’re switching vendors."
        expected = ["Smith & Co. Ltd. is closed.", "We’re switching vendors."]
        self.assertEqual(sentence_split(text), expected)

    def test_no_trailing_dot(self):
        text = "This is a sentence without trailing punctuation"
        expected = ["This is a sentence without trailing punctuation"]
        self.assertEqual(sentence_split(text), expected)


if __name__ == "__main__":
    unittest.main()
