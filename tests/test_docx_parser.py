from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

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


def test_rejects_archive_member_over_uncompressed_size_limit(monkeypatch):
    monkeypatch.setattr("src.parsing.docx_parser.MAX_DOCX_MEMBER_UNCOMPRESSED_BYTES", 10)
    output = BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        archive.writestr("large.xml", b"x" * 11)

    with pytest.raises(ParseError, match="archive member"):
        extract_text_from_docx(output.getvalue())


def test_rejects_total_uncompressed_size_over_limit(monkeypatch):
    monkeypatch.setattr("src.parsing.docx_parser.MAX_DOCX_MEMBER_UNCOMPRESSED_BYTES", 10)
    monkeypatch.setattr("src.parsing.docx_parser.MAX_DOCX_UNCOMPRESSED_BYTES", 12)
    output = BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        archive.writestr("first.xml", b"x" * 7)
        archive.writestr("second.xml", b"y" * 7)

    with pytest.raises(ParseError, match="safe parsing limit"):
        extract_text_from_docx(output.getvalue())
