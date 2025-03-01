# nlp_utils/extractor.py

import PyPDF2

def extract_text_from_pdf(file_storage) -> str:
    """
    Extract text from a PDF file using PyPDF2.
    """
    pdf_reader = PyPDF2.PdfReader(file_storage)
    text_pages = []
    for page in pdf_reader.pages:
        text_pages.append(page.extract_text())
    return "\n".join(text_pages)

def extract_text_from_txt(file_storage) -> str:
    """
    Extract text from a plain text file.
    """
    file_content = file_storage.read()
    return file_content.decode("utf-8", errors="replace")

def extract_text(file_storage) -> str:
    """
    Determine file type and extract text accordingly.
    """
    filename = file_storage.filename.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_storage)
    else:
        return extract_text_from_txt(file_storage)