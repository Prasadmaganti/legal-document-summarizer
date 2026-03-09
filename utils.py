import pdfplumber
import re

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                # Keep page structure
                text += page_text + "\n\n"
    return text

def clean_text(text):
    # Remove redundant spaces but keep double newlines for sections
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()