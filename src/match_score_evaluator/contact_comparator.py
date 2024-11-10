from typing import Dict, Any
from .similarity_factory import SimilarityStrategyFactory


class ContactComparator:
    """
        Calculates a similarity score between two contacts based on multiple fields.

        Each field's similarity is determined by a specific strategy, and the total score
        is a weighted sum of the field scores.

        Attributes:
        - weights (dict[str, float]): A dictionary where keys are field names, and values are
          their respective weights in the total score calculation.

        Methods:
        - calculate_score(contact1, contact2): Computes the weighted similarity score for a pair of contacts.
    """

    def __init__(self, weights: dict[str, float]):
        self.weights = weights

    def calculate_score(self, contact1: Dict[str, Any], contact2: Dict[str, Any]) -> float:
        """
            Calculates the similarity score between two contacts based on the provided field weights.

            Steps:
            1. For each field in the weights dictionary:
               a. Retrieve the corresponding similarity strategy using the field name.
               b. Calculate the similarity score between the two contact values for that field.
               c. Multiply the similarity score by the field's weight and add it to the total score.
            2. Return the cumulative similarity score for the two contacts.

            Parameters:
            - contact1 (dict): A dictionary containing the first contact's field values.
            - contact2 (dict): A dictionary containing the second contact's field values.

            Returns:
            - float: The weighted similarity score between the two contacts.
        """
        score: float = 0.0
        for field, weight in self.weights.items():
            strategy = SimilarityStrategyFactory.get_strategy(field)
            similarity = strategy.calculate(contact1[field], contact2[field])
            score += weight * similarity
        return score
