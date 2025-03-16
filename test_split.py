# Unit Tests
import unittest
from chunkator import sentence_split

class TestSentenceSplit(unittest.TestCase):
    def test_basic(self):
        text = "Dr. Smith is here. She has a Ph.D. in Chemistry."
        expected = ["Dr. Smith is here.", "She has a Ph.D. in Chemistry."]
        self.assertEqual(sentence_split(text), expected)

    def test_multiple_dots(self):
        text = "Hello... Is it working?"
        expected = ["Hello...", "Is it working?"]
        self.assertEqual(sentence_split(text), expected)

if __name__ == "__main__":
    unittest.main()
