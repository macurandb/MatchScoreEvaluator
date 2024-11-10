# MatchScoreEvaluator

**MatchScoreEvaluator** is a Python tool for identifying and evaluating potential duplicate contacts in datasets. It leverages configurable similarity strategies and weights to calculate and categorize duplicate scores. The results help streamline data cleaning processes and maintain data quality.

## Features

- **Customizable Similarity Strategies**: Dynamically configure different similarity algorithms for each field (e.g., name, email, address).
- **Weighted Scoring**: Assign weights to fields to prioritize specific attributes in the duplicate detection process.
- **Categorized Accuracy Levels**: Categorize matches into `High`, `Medium`, or `Low` similarity based on customizable thresholds.
- **Efficient Pair Comparison**: Uses cross joins and filters to compare all unique pairs in the dataset.
- **Logging**: Detailed logging of similarity scores and accuracy levels for traceability.

## Installation

### Prerequisites

- Python 3.8+
- Poetry (for dependency management)

### Clone the Repository

```bash
git clone https://github.com/yourusername/MatchScoreEvaluator.git
cd MatchScoreEvaluator
```

### Install Dependencies

Using Poetry:

```bash
poetry install
```

### Run Tests

```bash
pytest tests/
```
## Usage

### Input

Provide a CSV file containing the contact data. Ensure each contact has a unique `Contact ID`.

Example CSV (`contacts.csv`):

```csv
Contact ID,First Name,Last Name,Email Address,Zip Code,Address
1001,John,Doe,john.doe@example.com,12345,123 Main St
1002,Jon,Doe,jon.doe@example.com,12345,123 Main St
1003,Alice,Smith,alice.smith@example.com,67890,456 Elm St
```

### Run the Program 

```bash
poetry run python src/main.py
```

This will:

1. Load the `contacts.csv` file.
2. Identify potential duplicates by calculating similarity scores.
3. Save the results to `output.csv`.

### Output

The results will be saved in `output.csv`:

```csv
ContactID Source,ContactID Match,Accuracy
1001,1002,High
1001,1003,Low
1002,1003,Low
```

## Folder Structure

### Key Components:
- **`src/`**: Contains all source code for the project.
  - **`main.py`**: Entry point for the application.
  - **`match_score_evaluator/`**: Core logic for evaluating duplicates.
    - **`utils/`**: Utility functions like CSV loading and saving.
- **`tests/`**: Unit tests for various components.
- **`contacts.csv`**: Sample input file for demonstration or testing purposes.
- **`output.csv`**: Resulting output file containing potential duplicates.
- **`pyproject.toml`**: Defines dependencies and project configuration for Poetry.
- **`.gitignore`**: Specifies files and directories to exclude from version control.


## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`feature/my-feature`).
3. Commit your changes.
4. Push to the branch and open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
