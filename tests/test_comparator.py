import pytest
from match_score_evaluator.contact_comparator import ContactComparator
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


def test_calculate_score_high_similarity():
    """
    Test calculate_score with highly similar contacts.
    """
    comparator = ContactComparator(weights={
        'First Name': 0.3,
        'Last Name': 0.3,
        'Email Address': 0.2,
        'Zip Code': 0.1,
        'Address': 0.1
    })

    contact1 = {
        'First Name': 'John',
        'Last Name': 'Doe',
        'Email Address': 'john.doe@example.com',
        'Zip Code': '12345',
        'Address': '123 Main St'
    }

    contact2 = {
        'First Name': 'John',
        'Last Name': 'Doe',
        'Email Address': 'john.doe@example.com',
        'Zip Code': '12345',
        'Address': '123 Main St'
    }

    score = comparator.calculate_score(contact1, contact2)
    assert score == pytest.approx(1.0), f"Expected score to be ~1.0, got {score}"


def test_calculate_score_medium_similarity():
    """
    Test calculate_score with medium similarity between contacts.
    """
    comparator = ContactComparator(weights={
        'First Name': 0.3,
        'Last Name': 0.3,
        'Email Address': 0.2,
        'Zip Code': 0.1,
        'Address': 0.1
    })

    contact1 = {
        'First Name': 'John',
        'Last Name': 'Smith',
        'Email Address': 'john.smith@example.com',
        'Zip Code': '12345',
        'Address': '123 Main St'
    }

    contact2 = {
        'First Name': 'Jon',
        'Last Name': 'Doe',
        'Email Address': 'jon.doe@example.com',
        'Zip Code': '12345',
        'Address': '456 Main St'
    }

    score = comparator.calculate_score(contact1, contact2)
    assert 0.4 < score < 0.8, f"Expected score to be between 0.4 and 0.8, got {score}"


def test_calculate_score_low_similarity():
    """
    Test calculate_score with low similarity between contacts.
    """
    comparator = ContactComparator(weights={
        'First Name': 0.3,
        'Last Name': 0.3,
        'Email Address': 0.2,
        'Zip Code': 0.1,
        'Address': 0.1
    })

    contact1 = {
        'First Name': 'John',
        'Last Name': 'Smith',
        'Email Address': 'john.smith@example.com',
        'Zip Code': '12345',
        'Address': '123 Main St'
    }

    contact2 = {
        'First Name': 'Alice',
        'Last Name': 'Johnson',
        'Email Address': 'alice.johnson@example.com',
        'Zip Code': '67890',
        'Address': '789 Elm St'
    }

    score = comparator.calculate_score(contact1, contact2)
    assert score < 0.4, f"Expected score to be < 0.4, got {score}"


def test_calculate_score_missing_field():
    """
    Test calculate_score when one of the contacts has a missing field.
    """
    comparator = ContactComparator(weights={
        'First Name': 0.3,
        'Last Name': 0.3,
        'Email Address': 0.2,
        'Zip Code': 0.1,
        'Address': 0.1
    })

    contact1 = {
        'First Name': 'John',
        'Last Name': 'Doe',
        'Email Address': 'john.doe@example.com',
        'Zip Code': '12345',
        'Address': '123 Main St'
    }

    contact2 = {
        'First Name': 'John',
        'Last Name': None,  # Missing last name
        'Email Address': 'john.doe@example.com',
        'Zip Code': '12345',
        'Address': '123 Main St'
    }

    score = comparator.calculate_score(contact1, contact2)
    assert score < 1.0, f"Expected score to be < 1.0, got {score}"
