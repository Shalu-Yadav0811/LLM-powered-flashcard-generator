import PyPDF2


def extract_text_from_pdf(pdf_file):
    """Extract text content from a PDF file stream."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
    except Exception as e:
        raise ValueError(f'Failed to extract text from PDF: {str(e)}')
