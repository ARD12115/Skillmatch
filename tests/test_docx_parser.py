from io import BytesIO

import pytest
from docx import Document

from src.parsing.docx_parser import extract_text_from_docx
from src.utils.errors import EmptyDocumentError, ParseError


def make_docx(*paragraphs):
    document = Document()
    for paragraph in paragraphs:
        document.add_paragraph(paragraph)
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def test_extracts_paragraph_text():
    data = make_docx("Python developer", "SQL projects")

    assert extract_text_from_docx(data) == "Python developer\nSQL projects"


def test_empty_docx_has_friendly_error():
    with pytest.raises(EmptyDocumentError):
        extract_text_from_docx(make_docx())


def test_invalid_archive_has_parse_error():
    with pytest.raises(ParseError, match="Unable to read"):
        extract_text_from_docx(b"not a docx archive")
