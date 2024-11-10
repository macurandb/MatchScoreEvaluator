import pytest
import polars as pl
from match_score_evaluator.utils.data_loader import load_contacts_from_csv, save_results_to_csv


SAMPLE_CSV_CONTENT = """contactID,name,name1,email,postalZip,address
1,Ciara,French,mollis.lectus.pede@outlook.net,39746,449-6990 Tellus. Rd.
2,Charles,Pacheco,nulla.eget@protonmail.couk,76837,Ap #312-8611 Lacus. Ave
"""

EXPECTED_DATA = {
    "Contact ID": [1, 2],
    "First Name": ["Ciara", "Charles"],
    "Last Name": ["French", "Pacheco"],
    "Email Address": ["mollis.lectus.pede@outlook.net", "nulla.eget@protonmail.couk"],
    "Zip Code": [39746, 76837],
    "Address": ["449-6990 Tellus. Rd.", "Ap #312-8611 Lacus. Ave"]
}

COLUMN_MAPPING = {
    "contactID": "Contact ID",
    "name": "First Name",
    "name1": "Last Name",
    "email": "Email Address",
    "postalZip": "Zip Code",
    "address": "Address"
}


@pytest.fixture
def sample_csv(tmp_path):
    """Fixture to create a temporary sample CSV file."""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(SAMPLE_CSV_CONTENT)
    return csv_file


@pytest.fixture
def output_csv(tmp_path):
    """Fixture for temporary output CSV file path."""
    return tmp_path / "output.csv"


def test_load_contacts_from_csv_success(sample_csv):
    """Test successful loading of a CSV file with column mapping."""
    df = load_contacts_from_csv(sample_csv, COLUMN_MAPPING)
    assert isinstance(df, pl.DataFrame), "Expected a Polars DataFrame"
    assert df.shape == (2, 6), "Unexpected DataFrame shape"
    assert df.columns == list(EXPECTED_DATA.keys()), "Column names do not match the expected standard"


def test_load_contacts_from_csv_file_not_found():
    """Test loading a non-existent CSV file."""
    with pytest.raises(FileNotFoundError, match="File 'nonexistent.csv' does not exist"):
        load_contacts_from_csv("nonexistent.csv", COLUMN_MAPPING)


def test_load_contacts_from_csv_invalid_format(tmp_path):
    """Test loading an invalid CSV file."""
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("invalid data without headers")

    with pytest.raises(ValueError, match="Failed to read or process CSV file"):
        load_contacts_from_csv(invalid_csv, COLUMN_MAPPING)


def test_save_results_to_csv_success(sample_csv, output_csv):
    """Test saving a DataFrame to a CSV file."""
    df = load_contacts_from_csv(sample_csv, COLUMN_MAPPING)
    save_results_to_csv(df, output_csv)

    assert output_csv.exists(), "Output CSV file was not created"
    saved_df = pl.read_csv(output_csv)
    assert saved_df.shape == df.shape, "Saved DataFrame does not match original"


def test_save_results_to_csv_io_error(tmp_path):
    """Test handling of I/O error during CSV saving."""
    invalid_path = tmp_path / "nonexistent_dir" / "output.csv"
    df = pl.DataFrame(EXPECTED_DATA)

    with pytest.raises(IOError, match="Failed to write CSV file"):
        save_results_to_csv(df, invalid_path)
