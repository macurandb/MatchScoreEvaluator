import logging
from match_score_evaluator.contact_comparator import ContactComparator
from match_score_evaluator.duplicate_finder import DuplicateFinder
from match_score_evaluator.similarity_factory import SimilarityStrategyFactory
from match_score_evaluator.strategies import (
    NameSimilarity,
    EmailSimilarity,
    ZipCodeSimilarity,
    AddressSimilarity
)
from match_score_evaluator.utils.data_loader import load_contacts_from_csv, save_results_to_csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    file_path = "contacts1.csv"

    csv_mappings = {
        "contacts1.csv": {
            "contactID": "Contact ID",
            "name": "First Name",
            "name1": "Last Name",
            "email": "Email Address",
            "postalZip": "Zip Code",
            "address": "Address"
        },
        "contacts2.csv": {
            "Contact ID": "Contact ID",
            "First Name": "First Name",
            "Last Name": "Last Name",
            "Email Address": "Email Address",
            "Zip Code": "Zip Code",
            "Address": "Address"
        }
    }

    column_mapping = csv_mappings.get(file_path)
    if column_mapping is None:
        logging.error(f"No column mapping defined for file: {file_path}")
        exit(1)

    try:
        contacts_df = load_contacts_from_csv(file_path, column_mapping)
    except (FileNotFoundError, ValueError) as error:
        logging.error(error)
        exit(1)

    column_strategy_mapping = {
        'First Name': NameSimilarity(),
        'Last Name': NameSimilarity(),
        'Email Address': EmailSimilarity(),
        'Zip Code': ZipCodeSimilarity(),
        'Address': AddressSimilarity()
    }

    for column, strategy in column_strategy_mapping.items():
        SimilarityStrategyFactory.register_strategy(column, strategy)

    weights = {
        'First Name': 0.2,
        'Last Name': 0.2,
        'Email Address': 0.4,
        'Zip Code': 0.1,
        'Address': 0.1
    }

    comparator = ContactComparator(weights)
    finder = DuplicateFinder(comparator)

    try:
        results = finder.find_duplicates(contacts_df)
        save_results_to_csv(results, "output.csv")
        logging.info("Results saved to output.csv")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        exit(1)
