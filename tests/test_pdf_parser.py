from types import SimpleNamespace

import pytest

from src.parsing import pdf_parser
from src.utils.errors import EmptyDocumentError, ParseError


class FakePdf:
    def __init__(self, pages):
        self.pages = pages

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def test_extracts_text(monkeypatch):
    monkeypatch.setattr(
        pdf_parser.pdfplumber,
        "open",
        lambda _: FakePdf(
            [
                SimpleNamespace(extract_text=lambda: "Python"),
                SimpleNamespace(extract_text=lambda: "SQL"),
            ]
        ),
    )

    assert pdf_parser.extract_text_from_pdf(b"%PDF-content") == "Python\nSQL"


def test_empty_and_scanned_pdf_raise_clear_error(monkeypatch):
    monkeypatch.setattr(
        pdf_parser.pdfplumber,
        "open",
        lambda _: FakePdf([SimpleNamespace(extract_text=lambda: None)]),
    )

    with pytest.raises(EmptyDocumentError, match="text-based PDF"):
        pdf_parser.extract_text_from_pdf(b"%PDF-content")


def test_page_limit_is_enforced(monkeypatch):
    monkeypatch.setattr(
        pdf_parser.pdfplumber,
        "open",
        lambda _: FakePdf(
            [SimpleNamespace(extract_text=lambda: "text")]
            * (pdf_parser.MAX_PDF_PAGES + 1)
        ),
    )

    with pytest.raises(ParseError, match="page limit"):
        pdf_parser.extract_text_from_pdf(b"%PDF-content")


def test_parser_failure_is_converted(monkeypatch):
    def fail(_):
        raise RuntimeError("malformed")

    monkeypatch.setattr(pdf_parser.pdfplumber, "open", fail)

    with pytest.raises(ParseError, match="Unable to read"):
        pdf_parser.extract_text_from_pdf(b"%PDF-content")
