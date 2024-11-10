import polars as pl
import os
from typing import Dict


def load_contacts_from_csv(file_path: str, column_mapping: Dict[str, str], delimiter: str = ',',
                           has_header: bool = True) -> pl.DataFrame:
    """
    Loads contact data from a CSV file into a Polars DataFrame and standardizes column names.

    Parameters:
    - file_path (str): Path to the CSV file.
    - column_mapping (Dict[str, str]): Mapping of input column names to standard column names.
    - delimiter (str): Delimiter used in the CSV file (default is ',').
    - has_header (bool): Whether the CSV file contains a header row (default is True).

    Returns:
    - pl.DataFrame: Polars DataFrame with standardized column names.

    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - ValueError: If the file cannot be parsed as a CSV.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist. Please check the file path.")

    try:
        df = pl.read_csv(file_path, separator=delimiter, has_header=has_header)
        return df.rename(column_mapping)
    except Exception as e:
        raise ValueError(f"Failed to read or process CSV file '{file_path}': {e}")


def save_results_to_csv(results: pl.DataFrame, file_path: str) -> None:
    """
    Saves the results DataFrame to a CSV file.

    Parameters:
    - results (pl.DataFrame): The Polars DataFrame to save.
    - file_path (str): Path to the output CSV file.

    Raises:
    - IOError: If the file cannot be written.
    """
    try:
        results.write_csv(file_path)
    except Exception as e:
        raise IOError(f"Failed to write CSV file '{file_path}': {e}")
