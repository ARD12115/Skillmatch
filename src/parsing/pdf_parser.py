from io import BytesIO

import pdfplumber

from src.utils.errors import EmptyDocumentError, ParseError

MAX_PDF_PAGES = 10


def extract_text_from_pdf(data: bytes) -> str:
    """Extract text from a text-based PDF, enforcing a page limit."""
    try:
        with pdfplumber.open(BytesIO(data)) as pdf:
            if len(pdf.pages) > MAX_PDF_PAGES:
                raise ParseError(f"PDF exceeds the {MAX_PDF_PAGES}-page limit.")
            text = "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except ParseError:
        raise
    except Exception as exc:
        raise ParseError("Unable to read this PDF. Please try another file.") from exc
    if not text:
        raise EmptyDocumentError(
            "We couldn't read text from this PDF. Please upload a text-based PDF."
        )
    return text
