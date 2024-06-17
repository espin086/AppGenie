import streamlit as st
import pandas as pd
import plotly.express as px
import logging
from argparse import ArgumentParser
from sqlitecrud import SQLiteCRUD
from csvhandler import CSVHandler


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class StreamlitApp:
    """
    A template class for creating Streamlit applications with a sidebar and interactive data exploration.

    Attributes:
        title (str): The title of the Streamlit application.
        csv_handler (CSVHandler): An instance of the CSVHandler for CSV operations.
        db_handler (SQLiteCRUD): An instance of the SQLiteCRUD for database operations.
    """

    def __init__(self, title: str, csv_file: str, db_name: str):
        """
        Initializes the StreamlitApp with a title, CSV file, and SQLite database.


        Args:
            title (str): The title of the Streamlit application.
            csv_file (str): The path to the CSV file for data operations.
            db_name (str): The name of the SQLite database for data operations.
        """
        self.title = title
        self.csv_handler = CSVHandler(csv_file)
        self.db_handler = SQLiteCRUD(db_name)
        st.set_page_config(page_title=title)
        self.setup_sidebar()

    def setup_sidebar(self):
        """Sets up the sidebar for the Streamlit application."""
        st.sidebar.title("Navigation")
        selections = st.sidebar.radio("Go to", ["Home", "Data Sample", "Plots"])
        if selections == "Home":
            self.home_page()
        elif selections == "Data Sample":
            self.data_sample_page()
        elif selections == "Plots":
            self.plots_page()

    def home_page(self):
        """Displays the Home page."""
        st.title(self.title)
        st.write("Welcome to the Streamlit application template!")
        logging.info("Home page displayed.")

    def data_sample_page(self):
        """Displays the Data Sample page with the contents of the CSV."""
        st.title("Data Sample")
        dataframe = self.csv_handler.read_csv()
        st.write("Below is a sample of the CSV data:")
        st.dataframe(dataframe)
        st.write("Dataframe Info:")
        st.write(dataframe.info())
        st.write("Dataframe Description:")
        st.write(dataframe.describe())
        logging.info("Data Sample page displayed with data from CSV.")

    def plots_page(self):
        """Displays the Plots page for interactive plotly graphs."""
        st.title("Interactive Plots")
        dataframe = self.csv_handler.read_csv()
        if dataframe is not None and not dataframe.empty:
            columns = dataframe.columns.tolist()
            x_axis = st.selectbox("X-axis", columns)
            y_axis = st.selectbox("Y-axis", columns)
            plot = px.scatter(dataframe, x=x_axis, y=y_axis)
            st.plotly_chart(plot)
            logging.info("Plots page displayed with interactive plots.")
        else:
            st.write("No data available to plot.")
            logging.warning("No data available to plot in the Plots page.")

    def run(self):
        """Runs the Streamlit application."""
        logging.info("Streamlit application is running.")
        st.title(self.title)
        st.write("Use the sidebar to navigate through the app.")


def main():
    parser = ArgumentParser(description="Streamlit Multipage Application Template")
    parser.add_argument(
        "--title", type=str, default="Streamlit App", help="The title of the app."
    )
    parser.add_argument(
        "--csv_file", type=str, required=True, help="Path to the CSV file."
    )
    parser.add_argument(
        "--db_name", type=str, required=True, help="SQLite database name."
    )
    args = parser.parse_args()

    app = StreamlitApp(title=args.title, csv_file=args.csv_file, db_name=args.db_name)
    app.run()


if __name__ == "__main__":
    main()
