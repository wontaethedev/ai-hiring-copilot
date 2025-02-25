from pdfminer.high_level import extract_text


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Given the path to a PDF file, extracts just the text from the file as a string.
    """

    try:
        text: str = extract_text(pdf_path)
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")
