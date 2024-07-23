"""
Module for BigQuery CRUD operations.
"""
import pandas as pd
from google.cloud import bigquery
import logging


class BigQueryHandler:
    """
    A class to handle BigQuery operations, including CRUD.

    Attributes:
        project_id (str): The ID of the Google Cloud project.
        client (bigquery.Client): A BigQuery client instance.
    """

    def __init__(self, project_id: str) -> None:
        """
        Initializes the BigQueryHandler with a project ID.

        Args:
            project_id (str): The ID of the Google Cloud project.
        """
        assert isinstance(project_id, str), "project_id must be a string."

        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)
        self.job_config = bigquery.QueryJobConfig()
        logging.info("BigQueryHandler initialized with project ID: %s", project_id)

    def run_bigquery(self, query: str) -> pd.DataFrame:
        """
        Executes a BigQuery query.

        Args:
            query (str): The SQL query to execute.

        Returns:
            DataFrame: A DataFrame containing the query results.
        """

        assert isinstance(query, str), "query must be a string."

        try:
            self.job_config.use_legacy_sql = False
            query_job = self.client.query(query, job_config=self.job_config)
            results = query_job.result()
            return results.to_dataframe()
        except Exception as e:
            logging.error("Error running BigQuery query: %s", e)
            return None

    def create_table(self, dataset_name: str, table_name: str, schema: list) -> None:
        """
        Creates a new table in BigQuery.

        Args:
            dataset_name (str): The name of the dataset.
            table_name (str): The name of the table.
            schema (list): A list of bigquery.SchemaField defining the schema.
        """

        assert isinstance(dataset_name, str), "dataset_name must be a string."
        assert isinstance(table_name, str), "table_name must be a string."
        assert isinstance(schema, list), "schema must be a list."

        dataset_ref = self.client.dataset(dataset_name)
        table_ref = dataset_ref.table(table_name)
        table = bigquery.Table(table_ref, schema=schema)
        try:
            self.client.create_table(table)
            logging.info("Created table %s.%s", dataset_name, table_name)
        except Exception as e:
            logging.error("Error creating table %s.%s: %s", dataset_name, table_name, e)

    def insert_data(self, dataset_name: str, table_name: str, rows_to_insert: list):
        """
        Inserts data into a table in BigQuery.

        Args:
            dataset_name (str): The name of the dataset.
            table_name (str): The name of the table.
            rows_to_insert (list): A list of dictionaries representing rows to insert.
        """
        assert isinstance(dataset_name, str), "dataset_name must be a string."
        assert isinstance(table_name, str), "table_name must be a string."
        assert isinstance(rows_to_insert, list), "rows_to_insert must be a list."

        table_ref = self.client.dataset(dataset_name).table(table_name)
        try:
            errors = self.client.insert_rows_json(table_ref, rows_to_insert)
            if errors == []:
                logging.info("Inserted rows into table %s.%s", dataset_name, table_name)
            else:
                logging.error("Errors occurred while inserting rows: %s", errors)
        except Exception as e:
            logging.error(
                "Error inserting data into table %s.%s: %s", dataset_name, table_name, e
            )

    def update_data(self, query: str) -> None:
        """
        Updates data in a BigQuery table using a SQL query.

        Args:
            query (str): The SQL update query.
        """

        assert isinstance(query, str), "query must be a string."

        try:
            query_job = self.client.query(query)
            query_job.result()  # Waits for the query to finish
            logging.info("Update query executed successfully.")
        except Exception as e:
            logging.error("Error executing update query: %s", e)

    def delete_data(self, query: str) -> None:
        """
        Deletes data from a BigQuery table using a SQL query.

        Args:
            query (str): The SQL delete query.
        """

        assert isinstance(query, str), "query must be a string."

        try:
            query_job = self.client.query(query)
            query_job.result()  # Waits for the query to finish
            logging.info("Delete query executed successfully.")
        except Exception as e:
            logging.error("Error executing delete query: %s", e)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bq = BigQueryHandler("bigquery-public-data")
    query = """
    SELECT * 
    FROM `bigquery-public-data.census_bureau_usa.population_by_zip_2000` 
    LIMIT 1000"""
    results = bq.run_bigquery(query)
    print(results)