import streamlit as st
import config
import zipfile
from io import BytesIO
import logging
from argparse import ArgumentParser
import os

# Necessary imports for various functionalities

from dataexplorer import DataFrameProfiler
from sqlitecrud import SQLiteCRUD
from csvhandler import CSVHandler
from streamlithandler import StreamlitApp
from excel import ExcelHandler
from bigqueryhandler import BigQueryHandler
from dataprocessor import DataFrameCleaner

from gpt import GPTModelHandler, TOCD, PromptOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Loading content of helper modules
file_names = [
    "bigqueryhandler.py",
    "csvhandler.py",
    "dataexplorer.py",
    "dataprocessor.py",
    "dedup.py",
    "excel.py",
    "gpt.py",
    "sqlitecrud.py",
    "snowflakehandler.py",
    "streamlithandler.py",
    "requirements.txt",
]

file_contents = {name: open(name).read() for name in file_names}

HOW_TO_SUMMARIZE = f"""You need to provide a python code.

Requirements for Code:
- Produce Docstrings for the module, classes, and functions, using the Google Docstring Format.
- Ensure usage of classes and best practices of object-oriented programming. You want to have a class that is responsible for the main functionality of the code.
- Develop a main function that uses the classes that accepts useful and important command line arguments via argparse (not sys).
- Operate logging for methods, functions, etc., using the logging library and consistent logging of info, warning, error, etc. where practical.
- Format the generated code beautifully following the Black standard.
- Add type hints to the functions and methods for both input and output.
- Add assert statements to check the input arguments and the output of the functions.
- Use try and except blocks to handle exceptions 
- Functions and methods should return values instead of printing them. If it makes sense you can also return True or False

Note: I have a set of classes already that I can import to make the code more modular and easier to write. Here are the classes I have:

"""

# Adding helper class details to the prompt
for name, content in file_contents.items():
    HOW_TO_SUMMARIZE += f"""
        Name: {name}

        Code: {content}
        """
HOW_TO_SUMMARIZE += """
Include the following:
- A class that is responsible for the main functionality of the code.
- A main function that uses the classes that accepts useful and important command line arguments via argparse (not sys).
- Operate logging for methods, functions, etc., using the logging library and consistent logging of info, warning, error, etc. where practical.
- Format the generated code beautifully following the Black standard.
- Can you provide a diagram showing how the code works? Say a sequence diagram, flowchart, or a UML diagram as well, this is required
- Ensure usage of classes and best practices of object-oriented programming. You want to have a class that is responsible for the main functionality of the code.
"""


def render_text_area(section_title: str, help_text: str) -> str:
    """Render a text area component in the Streamlit app.

    Args:
        section_title (str): The title for this section.
        help_text (str): The help text for the text area.

    Returns:
        str: The text entered by the user in the text area.
    """

    assert isinstance(section_title, str), "section_title must be a string."
    assert isinstance(help_text, str), "help_text must be a string."

    return st.text_area(section_title, help=help_text, key=section_title)


def render_summary_button() -> bool:
    """Render a button for summarizing the input.

    Returns:
        bool: True if the button is clicked, False otherwise.
    """
    return st.button("Write App", key="btn_summarize")


class CodeGeneratorApp(GPTModelHandler):
    """The Code Generator App class."""

    def __init__(self):
        super().__init__()
        st.set_page_config(page_title="Code Generator App", layout="centered")
        self.zip_buffer = BytesIO()  # Make zip_buffer an instance variable
        self.prompt = ""
        self.display_ui()

    def display_ui(self):
        """Renders the Streamlit UI components."""
        st.title("🚀 Welcome to AppGenie: the Best Python App Creator! 🚀")
        st.subheader(
            "Your one-stop solution for generating high-quality Python projects effortlessly."
        )
        st.markdown(
            """
            Imagine having a personal assistant that can generate well-documented, 
            beautifully formatted, and highly functional Python code for you. 
            That's exactly what our app does! Whether you're a seasoned developer 
            or just starting out, this app will save you countless hours of coding.
            """
        )
        st.write("---")

        st.header("Tell me about your app?")
        feature_input = render_text_area(
            "What should the code do?",
            "What is the specific issue or feature that the code needs to implement?",
        )
        st.write("---")

        self.prompt = f"""Here is your task {HOW_TO_SUMMARIZE}. 
        Here are the goals: {feature_input}. 
        """
        logging.info(f"Prompt: {self.prompt}")

        # optimizing the prompt using best practices
        oPromptOptimizer = PromptOptimizer(prompt=str(self.prompt))
        self.prompt = oPromptOptimizer.response()

        if render_summary_button():
            oTOCD = TOCD(
                task=self.prompt,
                output="write code, diagrams, and explanation",
                context="you are going to run this code locally so make it easy to run and understand.",
                data="Don't forget to include the classes I have in the prompt.",
            )
            summary = oTOCD.generate_response()

            st.success(
                "🎉 Your code has been generated successfully! Press DOWNLOAD at end of output below!!!"
            )
            st.code(summary, language="python")

            self.download_zip(option="Generate", summary=summary)
            st.info("Press button below to download your code/app!.")

    def download_zip(self, option: str, summary: str = None):
        """Enables downloading the helper modules and generated code as a zip file.

        Args:
            option (str): Option to cover either 'Generate' or 'Helper Modules'.
            summary (str, optional): Summary of the generated code. Defaults to None.
        """

        with zipfile.ZipFile(self.zip_buffer, "w") as zf:  # Use self.zip_buffer here
            for name, content in file_contents.items():
                zf.writestr(name, content)
            if option == "Generate" and summary:
                zf.writestr("main.py", summary)

        download_path = os.path.expanduser("AppGenie.zip")
        with open(download_path, "wb") as f:
            f.write(self.zip_buffer.getvalue())


if __name__ == "__main__":
    app = CodeGeneratorApp()

    # Download button

    with open("AppGenie.zip", "rb") as file:
        btn = st.download_button(
            label="Download App",
            data=file,
            file_name="appgenie.zip",
            mime="application/zip",
        )
