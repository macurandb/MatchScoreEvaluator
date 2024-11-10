class SimilarityCategorizer:
    """
        Categorizes similarity scores into predefined accuracy levels: High, Medium, or Low.

        This class provides an intuitive classification of similarity scores, making it easier
        to interpret the results of contact comparisons.

        Methods:
        - categorize(score): Categorizes a similarity score into High, Medium, or Low.
    """
    @staticmethod
    def categorize(score: float) -> str:
        if score >= 0.8:
            return "High"
        elif score >= 0.6:
            return "Medium"
        else:
            return "Low"
