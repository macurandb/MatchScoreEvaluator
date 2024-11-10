from .strategies import SimilarityStrategy


class SimilarityStrategyFactory:
    """
        Manages the registration and retrieval of similarity strategies for specific fields.

        This class provides a dynamic mechanism to associate fields with their corresponding
        similarity strategies, enabling flexible and extensible configuration.

        Attributes:
        - _strategies (dict[str, SimilarityStrategy]): A dictionary mapping field names to similarity strategies.

        Methods:
        - register_strategy(field_type, strategy): Registers a similarity strategy for a given field.
        - get_strategy(field_type): Retrieves the registered similarity strategy for a given field.
        """

    _strategies: dict[str, SimilarityStrategy] = {}

    @staticmethod
    def register_strategy(field_type: str, strategy: SimilarityStrategy) -> None:
        """
        Registers a similarity strategy for a specific field type.

        Parameters:
        - field_type (str): The name of the field (e.g., 'First Name').
        - strategy (SimilarityStrategy): An instance of the similarity strategy.
        """
        SimilarityStrategyFactory._strategies[field_type] = strategy

    @staticmethod
    def get_strategy(field_type: str) -> SimilarityStrategy:
        """
        Retrieves the similarity strategy for a given field type.

        Parameters:
        - field_type (str): The name of the field.

        Returns:
        - SimilarityStrategy: The registered strategy.
        """
        if field_type not in SimilarityStrategyFactory._strategies:
            raise ValueError(f"No strategy registered for field type: {field_type}")
        return SimilarityStrategyFactory._strategies[field_type]
