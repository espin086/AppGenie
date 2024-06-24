import pandas as pd
import snowflake.connector as snf
import logging
from argparse import ArgumentParser

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SnowflakeQueryRunner:
    """
    A class to run optimized SQL queries on a Snowflake database.

    Attributes:
        connection_params (dict): Dictionary containing Snowflake connection parameters.
    """

    def __init__(self, connection_params: dict):
        """
        Initializes the SnowflakeQueryRunner with connection parameters.

        Args:
            connection_params (dict): Snowflake connection parameters.
        """
        self.connection_params = connection_params
        self.connection = None

    def connect_to_snowflake(self):
        """
        Connects to the Snowflake database.

        Raises:
            Exception: If connection fails.
        """
        try:
            self.connection = snf.connect(**self.connection_params)
            logging.info("Connected to Snowflake.")
        except Exception as e:
            logging.error(f"Failed to connect to Snowflake: {e}")
            raise

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Executes a query and returns the result as a DataFrame.

        Args:
            query (str): The SQL query to execute.

        Returns:
            pd.DataFrame: The result of the query as a DataFrame.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("alter session set rows_per_resultset = 0")
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            logging.info(f"Snowflake Query ID: {cursor.sfqid}")
            return pd.DataFrame(result, columns=columns)
        except Exception as e:
            logging.error(f"Failed to execute query: {e}")
            return None

    def close_connection(self):
        """
        Closes the connection to Snowflake.
        """
        if self.connection:
            self.connection.close()
            logging.info("Disconnected from Snowflake.")


def main():
    """The main function to run the Snowflake Query Runner."""
    parser = ArgumentParser(description="Snowflake Query Runner")
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="The SQL query to execute on Snowflake.",
    )
    parser.add_argument(
        "--email_id", type=str, required=True, help="Your email ID for authentication."
    )
    parser.add_argument(
        "--schema", type=str, required=True, help="Snowflake schema name."
    )
    parser.add_argument(
        "--database", type=str, required=True, help="Snowflake database name."
    )
    parser.add_argument(
        "--warehouse", type=str, required=True, help="Snowflake warehouse name."
    )
    parser.add_argument(
        "--role", type=str, required=True, help="Snowflake role for access."
    )

    args = parser.parse_args()

    connection_params = {
        "user": args.email_id,
        "account": "xxxxxxxxxx.us-east-1",
        "schema": args.schema,
        "database": args.database,
        "warehouse": args.warehouse,
        "role": args.role,
        "authenticator": "externalbrowser",
    }

    runner = SnowflakeQueryRunner(connection_params)
    runner.connect_to_snowflake()

    df = runner.execute_query(args.query)

    if df is not None:
        print(df)

    runner.close_connection()


if __name__ == "__main__":
    main()
