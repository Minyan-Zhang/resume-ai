import pdfplumber
from docx import Document


def read_resume(file_path: str) -> str:
    """Read PDF or DOCX resume file and return plain text"""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Only PDF or DOCX formats are supported")
