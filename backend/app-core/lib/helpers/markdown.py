import markdown
from bs4 import BeautifulSoup

def extract_text_from_markdown(markdown_path: str) -> str:
    """
    Given the path to a Markdown file, extracts just the text from the file as a string.
    """

    try:
        with open(markdown_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)

        # Parse the HTML and extract text
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()

        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from Markdown: {str(e)}")
