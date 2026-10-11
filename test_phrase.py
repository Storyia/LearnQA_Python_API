def test_phrase_length():
    phrase = input("Set a phrase: ")

    assert len(phrase) < 15, "Phrase is too long"
