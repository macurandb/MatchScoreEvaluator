import polars as pl
import logging
from .contact_comparator import ContactComparator
from .similarity_categorizer import SimilarityCategorizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DuplicateFinder:
    """
        Identifies potential duplicate contacts in a dataset by comparing all unique pairs.

        This class uses a comparator to calculate similarity scores and a categorizer
        to classify the similarity accuracy for each pair.

        Attributes:
        - comparator (ContactComparator): Used to compute similarity scores between contacts.

        Methods:
        - find_duplicates(contacts): Finds potential duplicates and returns a DataFrame with match details.
    """

    def __init__(self, comparator: ContactComparator):
        self.comparator = comparator

    def find_duplicates(self, contacts: pl.DataFrame) -> pl.DataFrame:
        """
        Identifies potential duplicate contacts from the given DataFrame.

        Steps:
        1. Creates all possible unique pairs of contacts by performing a cross join.
        2. Filters out pairs where the left contact ID is not less than the right contact ID to avoid duplicate comparisons.
        3. Calculates similarity scores for each pair of contacts using the provided comparator.
        4. Categorizes the similarity score into High, Medium, or Low accuracy.
        5. Collects all pairs and their corresponding accuracy levels into a new DataFrame.

        Parameters:
        - contacts (pl.DataFrame): A DataFrame containing contact information. Each contact must have a unique 'Contact ID'.

        Returns:
        - pl.DataFrame: A DataFrame containing the following columns:
          * 'ContactID Source' - The ID of the first contact in the pair.
          * 'ContactID Match' - The ID of the second contact in the pair.
          * 'Accuracy' - The categorized similarity score for the contact pair.
        """
        results = []
        contact_pairs = contacts.rename({col: f"{col}_left" for col in contacts.columns}).join(
            contacts.rename({col: f"{col}_right" for col in contacts.columns}), how="cross"
        ).filter(pl.col("Contact ID_left") < pl.col("Contact ID_right"))

        for row in contact_pairs.rows(named=True):
            contact1 = {key.replace('_left', ''): value for key, value in row.items() if '_left' in key}
            contact2 = {key.replace('_right', ''): value for key, value in row.items() if '_right' in key}

            score = self.comparator.calculate_score(contact1, contact2)
            accuracy = SimilarityCategorizer.categorize(score)

            logging.info(
                f"Score between {contact1['Contact ID']} and {contact2['Contact ID']}: {score}, Accuracy: {accuracy}")

            results.append({
                'ContactID Source': contact1['Contact ID'],
                'ContactID Match': contact2['Contact ID'],
                'Accuracy': accuracy
            })

        return pl.DataFrame(results)
