import pytest

class TestPhraseLength:
    def test_phrase_length(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, 'Length of phrase is more than 15 symbols'