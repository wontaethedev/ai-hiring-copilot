from docx import Document

def extract_text_from_word(file_path: str) -> str:
  """
  Given the path to a DOCX file, extracts just the text from the file as a string.
  """

  doc = Document(file_path)
  full_text = [para.text for para in doc.paragraphs]
  return '\n'.join(full_text)
