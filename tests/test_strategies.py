import pytest
from match_score_evaluator.strategies import (
    NameSimilarity,
    EmailSimilarity,
    ZipCodeSimilarity,
    AddressSimilarity
)


def test_name_similarity():
    """
    Test NameSimilarity with various levels of similarity.
    """
    strategy = NameSimilarity()

    # High similarity
    assert strategy.calculate("John", "Jon") > 0.9, "Expected high similarity between 'John' and 'Jon'"

    # Medium similarity
    assert 0.8 < strategy.calculate("John", "Johnny") < 0.95, "Expected medium similarity between 'John' and 'Johnny'"

    # Low similarity
    assert strategy.calculate("John", "Alice") < 0.5, "Expected low similarity between 'John' and 'Alice'"

    # Null or empty values
    assert strategy.calculate(None, "Alice") == pytest.approx(0.0), "Expected 0 similarity for None and 'Alice'"
    assert strategy.calculate("", "") == pytest.approx(1.0), "Expected perfect similarity for two empty strings"


def test_email_similarity():
    """
    Test EmailSimilarity with various levels of similarity.
    """
    strategy = EmailSimilarity()

    # High similarity
    assert strategy.calculate("user@example.com", "user@example.com") == pytest.approx(1.0), \
        "Expected perfect similarity for identical emails"

    # Medium similarity
    assert 0.8 < strategy.calculate("user@example.com", "usr@example.com") < 0.95, \
        "Expected medium similarity between slightly different emails"

    # Low similarity
    assert strategy.calculate("user@example.com", "admin@domain.com") < 0.5, \
        "Expected low similarity for different emails"

    # Null or empty values
    assert strategy.calculate(None, "user@example.com") == pytest.approx(0.0), \
        "Expected 0 similarity for None and an email"
    assert strategy.calculate("", "") == pytest.approx(1.0), \
        "Expected perfect similarity for two empty strings"


def test_zip_code_similarity():
    """
    Test ZipCodeSimilarity for exact matches and mismatches.
    """
    strategy = ZipCodeSimilarity()

    # Exact match
    assert strategy.calculate("12345", "12345") == pytest.approx(1.0), \
        "Expected perfect similarity for identical zip codes"

    # Mismatch
    assert strategy.calculate("12345", "67890") == pytest.approx(0.0), \
        "Expected 0 similarity for different zip codes"

    # Null or empty values
    assert strategy.calculate(None, "12345") == pytest.approx(0.0), \
        "Expected 0 similarity for None and a zip code"


def test_address_similarity():
    """
    Test AddressSimilarity based on shared words.
    """
    strategy = AddressSimilarity()

    # High similarity
    assert strategy.calculate("123 Main St", "123 Main St") == pytest.approx(1.0), \
        "Expected perfect similarity for identical addresses"

    # Partial similarity
    assert 0.5 <= strategy.calculate("123 Main St", "456 Main St") < 0.7, \
        "Expected partial similarity for addresses with shared words"

    # Low similarity
    assert strategy.calculate("123 Main St", "789 Elm St") < 0.5, \
        "Expected low similarity for addresses with no common words"

    # Null or empty values
    assert strategy.calculate(None, "123 Main St") == pytest.approx(0.0), \
        "Expected 0 similarity for None and an address"
    assert strategy.calculate("", "") == pytest.approx(0.0), \
        "Expected 0 similarity for two empty addresses"
