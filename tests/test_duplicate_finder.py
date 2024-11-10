import pytest
import polars as pl
from match_score_evaluator.contact_comparator import ContactComparator
from match_score_evaluator.duplicate_finder import DuplicateFinder
from match_score_evaluator.similarity_factory import SimilarityStrategyFactory
from match_score_evaluator.strategies import (
    NameSimilarity,
    EmailSimilarity,
    ZipCodeSimilarity,
    AddressSimilarity
)


# Setup: Register strategies before running tests
@pytest.fixture(autouse=True)
def register_strategies():
    SimilarityStrategyFactory.register_strategy('First Name', NameSimilarity())
    SimilarityStrategyFactory.register_strategy('Last Name', NameSimilarity())
    SimilarityStrategyFactory.register_strategy('Email Address', EmailSimilarity())
    SimilarityStrategyFactory.register_strategy('Zip Code', ZipCodeSimilarity())
    SimilarityStrategyFactory.register_strategy('Address', AddressSimilarity())


@pytest.fixture
def sample_contacts():
    """
    Fixture to provide sample contact data as a Polars DataFrame.
    """
    data = {
        'Contact ID': [1001, 1002, 1003],
        'First Name': ['John', 'Jon', 'Alice'],
        'Last Name': ['Doe', 'Doe', 'Smith'],
        'Email Address': ['john.doe@example.com', 'jon.doe@example.com', 'alice.smith@example.com'],
        'Zip Code': ['12345', '12345', '67890'],
        'Address': ['123 Main St', '123 Main St', '456 Elm St']
    }
    return pl.DataFrame(data)


def test_find_duplicates_high_similarity(sample_contacts):
    """
    Test that the function identifies high similarity duplicates.
    """
    comparator = ContactComparator(weights={
        'First Name': 0.3,
        'Last Name': 0.3,
        'Email Address': 0.2,
        'Zip Code': 0.1,
        'Address': 0.1
    })
    finder = DuplicateFinder(comparator)

    results = finder.find_duplicates(sample_contacts)

    # Check that 1001 and 1002 have High similarity
    assert len(results) > 0, "Expected at least one pair of duplicates"

    high_similarity_pair = results.filter(pl.col('ContactID Source') == 1001).filter(
        pl.col('ContactID Match') == 1002
    ).select('Accuracy').to_series().to_list()[0]  # Extract as list and get the first element

    assert high_similarity_pair == "High", f"Expected High similarity for 1001 and 1002, got {high_similarity_pair}"


def test_find_duplicates_low_similarity(sample_contacts):
    """
    Test that the function identifies low similarity contacts.
    """
    comparator = ContactComparator(weights={
        'First Name': 0.3,
        'Last Name': 0.3,
        'Email Address': 0.2,
        'Zip Code': 0.1,
        'Address': 0.1
    })
    finder = DuplicateFinder(comparator)

    results = finder.find_duplicates(sample_contacts)

    # Check that 1001 and 1003 have Low similarity
    low_similarity_pair = results.filter(pl.col('ContactID Source') == 1001).filter(
        pl.col('ContactID Match') == 1003
    ).select('Accuracy').to_series().to_list()[0]  # Extract as list and get the first element

    assert low_similarity_pair == "Low", f"Expected Low similarity for 1001 and 1003, got {low_similarity_pair}"


def test_find_duplicates_correct_number_of_pairs(sample_contacts):
    """
    Test that the correct number of contact pairs is generated.
    """
    comparator = ContactComparator(weights={
        'First Name': 0.3,
        'Last Name': 0.3,
        'Email Address': 0.2,
        'Zip Code': 0.1,
        'Address': 0.1
    })
    finder = DuplicateFinder(comparator)

    results = finder.find_duplicates(sample_contacts)

    # Check the number of pairs generated: 3 contacts should yield 3 unique pairs
    assert results.shape[0] == 3, f"Expected 3 pairs, but got {results.shape[0]}"


def test_find_duplicates_no_duplicates():
    """
    Test that no duplicates are found when all contacts are significantly different.
    """
    data = {
        'Contact ID': [2001, 2002, 2003],
        'First Name': ['Alice', 'Bob', 'Charlie'],
        'Last Name': ['Smith', 'Brown', 'Johnson'],
        'Email Address': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
        'Zip Code': ['11111', '22222', '33333'],
        'Address': ['1 A St', '2 B St', '3 C St']
    }
    contacts = pl.DataFrame(data)

    comparator = ContactComparator(weights={
        'First Name': 0.3,
        'Last Name': 0.3,
        'Email Address': 0.2,
        'Zip Code': 0.1,
        'Address': 0.1
    })
    finder = DuplicateFinder(comparator)

    results = finder.find_duplicates(contacts)

    # All contacts should have low similarity, so the accuracy of all results should be "Low"
    assert results.filter(pl.col("Accuracy") != "Low").shape[0] == 0, \
        "Expected no high or medium similarity pairs"
