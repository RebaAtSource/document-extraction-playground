from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_path


def extract_text_from_pdf(pdf_file):
    # Extract text using PyPDF2
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    # If text extraction is empty, use OCR
    if not text.strip():
        images = convert_from_path(pdf_file)
        for image in images:
            text += pytesseract.image_to_string(image)

    return text 