import fitz  # PyMuPDF
import os 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if OPENAI_API_KEY:
#     os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


import fitz
import os

def extract_text_from_pdf(upload_file):
    """
    Extract text from a PDF file using PyMuPDF.

    Parameters
    ----------
    upload_file : str or file-like object
        Path to the PDF file or an uploaded PDF file object.

    Returns
    -------
    str
        Extracted text from all pages of the PDF.
    """
    # local system → treat as file path
    if isinstance(upload_file, str):
        if not os.path.exists(upload_file):
            raise FileNotFoundError(f"File not found: {upload_file}")
        with fitz.open(upload_file) as doc:
            return "".join(page.get_text() for page in doc)
    
    # streamlit library file-like object
    else:
        pdf_bytes = upload_file.read()
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc)



def ask_openai(query: str, max_tokens: int = None) -> str:
    """
    Ask OpenAI using system and user roles.

    Args:
        query (str): User input text
        max_tokens (int): Maximum output tokens

    Returns:
        str: Model response text
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    client = OpenAI(api_key=api_key)
    messages = [
        {
            "role": "system",
            "content": "You are a job recommendation assistant."
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = client.responses.create(
        model="gpt-4o-mini",          # cheapest good-performance model
        input=messages,
        max_output_tokens=max_tokens
    )

    return response.output_text

