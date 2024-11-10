import pytest
from match_score_evaluator.similarity_factory import SimilarityStrategyFactory
from match_score_evaluator.strategies import (
    SimilarityStrategy,
    NameSimilarity,
    EmailSimilarity
)


def test_register_and_get_strategy():
    """
    Test that strategies can be registered and retrieved correctly.
    """
    # Register a strategy for 'First Name'
    SimilarityStrategyFactory.register_strategy('First Name', NameSimilarity())
    strategy = SimilarityStrategyFactory.get_strategy('First Name')

    assert isinstance(strategy, NameSimilarity), "Expected NameSimilarity for 'First Name'"


def test_register_multiple_strategies():
    """
    Test registering multiple strategies for different fields.
    """
    SimilarityStrategyFactory.register_strategy('Email Address', EmailSimilarity())
    email_strategy = SimilarityStrategyFactory.get_strategy('Email Address')

    SimilarityStrategyFactory.register_strategy('First Name', NameSimilarity())
    name_strategy = SimilarityStrategyFactory.get_strategy('First Name')

    assert isinstance(email_strategy, EmailSimilarity), "Expected EmailSimilarity for 'Email Address'"
    assert isinstance(name_strategy, NameSimilarity), "Expected NameSimilarity for 'First Name'"


def test_get_strategy_not_registered():
    """
    Test that requesting an unregistered strategy raises a ValueError.
    """
    with pytest.raises(ValueError, match="No strategy registered for field type: Unregistered Field"):
        SimilarityStrategyFactory.get_strategy('Unregistered Field')


def test_overwrite_registered_strategy():
    """
    Test that registering a new strategy for the same field overwrites the old one.
    """
    SimilarityStrategyFactory.register_strategy('First Name', NameSimilarity())
    initial_strategy = SimilarityStrategyFactory.get_strategy('First Name')

    # Register a different strategy for 'First Name'
    SimilarityStrategyFactory.register_strategy('First Name', EmailSimilarity())
    new_strategy = SimilarityStrategyFactory.get_strategy('First Name')

    assert isinstance(initial_strategy, NameSimilarity), "Expected initial strategy to be NameSimilarity"
    assert isinstance(new_strategy, EmailSimilarity), "Expected new strategy to be EmailSimilarity after overwrite"
