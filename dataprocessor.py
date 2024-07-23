import pandas as pd
import numpy as np
import re
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataFrameCleaner:
    """
    A class used to clean a pandas DataFrame.

    Attributes:
        dataframe : pd.DataFrame
            The dataframe to be cleaned.
    """

    def __init__(self, dataframe) -> None:
        """
        Initializes the DataFrameCleaner with a dataframe.

        Args:
            dataframe (pd.DataFrame): The dataframe to be cleaned.
        """
        assert isinstance(dataframe, pd.DataFrame), "dataframe must be a DataFrame."

        self.dataframe = dataframe
        logging.info("DataFrame initialized for cleaning")

    def change_index(self, column) -> None:
        """Change the index of the DataFrame to the specified column."""
        
        assert column in self.dataframe.columns, "column must be in DataFrame columns."

        self.dataframe = self.dataframe.set_index(column)
        logging.info(f"Index changed to {column}")

    def remove_duplicates(self)-> None:
        """Remove duplicate rows from DataFrame."""
        self.dataframe = self.dataframe.drop_duplicates()
        logging.info("Duplicates removed from DataFrame")

    def remove_missing_values(self) -> None:
        """Remove rows with missing values from DataFrame."""
        self.dataframe = self.dataframe.dropna()
        logging.info("Missing values removed from DataFrame")

    def remove_outliers(self, column:str, threshold:float) -> None:
        """Remove outliers from a specified column based on Z-score threshold."""

        assert column in self.dataframe.columns, "column must be in DataFrame columns."
        assert isinstance(threshold, (int, float)), "threshold must be a number."
        assert isinstance(column, str), "column must be a string."

        z_scores = (
            self.dataframe[column] - self.dataframe[column].mean()
        ) / self.dataframe[column].std()
        self.dataframe = self.dataframe[
            (z_scores < threshold) & (z_scores > -threshold)
        ]
        logging.info(
            f"Outliers removed from column {column} with threshold {threshold}"
        )

    def convert_data_types(self, column:str, new_type: str) -> None:
        """Convert data type of a specified column."""

        assert column in self.dataframe.columns, "column must be in DataFrame columns."
        assert isinstance(new_type, str), "new_type must be a string."

        if new_type == "int":
            self.dataframe[column] = self.dataframe[column].fillna(0).astype(int)
        else:
            self.dataframe[column] = self.dataframe[column].astype(new_type)
        logging.info(f"Column {column} converted to type {new_type}")

    def remove_columns(self, columns: list) -> None:
        """Remove specified columns from DataFrame."""

        assert isinstance(columns, list), "columns must be a list."
        assert columns in self.dataframe.columns, "columns must be in DataFrame columns."

        self.dataframe = self.dataframe.drop(columns, axis=1)
        logging.info(f"Columns {columns} removed from DataFrame")

    def lower_case_column(self, column:str) -> None:
        """Convert all text in a specified column to lowercase."""

        assert column in self.dataframe.columns, "column must be in DataFrame columns."
        assert isinstance(column, str), "column must be a string."
        
        self.dataframe[column] = self.dataframe[column].str.lower()
        logging.info(f"Text in column {column} converted to lowercase")

    def remove_white_spaces(self, column:str) -> None:
        """Remove leading and trailing white spaces in a specified column."""

        assert column in self.dataframe.columns, "column must be in DataFrame columns."
        assert isinstance(column, str), "column must be a string."

        self.dataframe[column] = self.dataframe[column].str.strip()
        logging.info(f"Leading and trailing whitespaces removed from column {column}")

    def remove_special_characters(self, column):
        """Remove special characters in a specified column."""

        assert column in self.dataframe.columns, "column must be in DataFrame columns."
        assert isinstance(column, str), "column must be a string."

        self.dataframe[column] = self.dataframe[column].str.replace(
            r"[^a-zA-Z0-9]", "", regex=True
        )
        logging.info(f"Special characters removed from column {column}")

    def clean_text_column(self, column:str) -> None:
        """Clean text in a specified column by converting to lowercase, removing white spaces and special characters."""
        
        assert isinstance(column, str), "column must be a string."
        assert column in self.dataframe.columns, "column must be in DataFrame columns."
        
        self.lower_case_column(column)
        self.remove_white_spaces(column)
        self.remove_special_characters(column)
        logging.info(f"Text column {column} cleaned")

    def get_cleaned_dataframe(self) -> pd.DataFrame:
        """Return the cleaned DataFrame."""
        logging.info("Returning cleaned DataFrame")
        return self.dataframe

if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    cleaner = DataFrameCleaner(df)
    cleaner.change_index("id")
    cleaner.remove_duplicates()
    cleaner.remove_missing_values()
    cleaner.remove_outliers("age", 2)
    cleaner.convert_data_types("age", "int")
    cleaner.remove_columns(["dob"])
    cleaner.clean_text_column("name")
    cleaned_df = cleaner.get_cleaned_dataframe()
    print(cleaned_df.head())