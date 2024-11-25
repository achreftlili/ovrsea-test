from pdf2image import convert_from_path
import pytesseract
from langchain_community.document_loaders import PDFPlumberLoader


def convert_to_image(file_path):
    pages = convert_from_path(file_path)
    return pages

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def pdf_image_text(file_path):
    extracted_text = []
    pages = convert_to_image(file_path)
    for page_image in pages:
        # Step 3: Extract text using OCR
        text = extract_text_from_image(page_image)
        extracted_text.append(text)
    return extracted_text
    
def pdf_parser_text(uploaded_file_path):
    loader = PDFPlumberLoader(uploaded_file_path)
    docs = loader.load()
    return docs
