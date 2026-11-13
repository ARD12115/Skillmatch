import pytest

from src.parsing.validators import validate_upload
from src.utils.errors import FileTooLargeError, UnsupportedFileError


def test_accepts_pdf_and_docx_signatures():
    validate_upload("resume.pdf", b"%PDF-1.7 data")
    validate_upload("resume.docx", b"PK\x03\x04data")


@pytest.mark.parametrize(
    ("name", "data"),
    [
        ("resume.pdf", b"not a pdf"),
        ("resume.txt", b"%PDF-1.7 data"),
        ("resume.docx", b""),
    ],
)
def test_rejects_empty_or_mismatched_files(name, data):
    with pytest.raises(UnsupportedFileError):
        validate_upload(name, data)


def test_rejects_oversized_upload(monkeypatch):
    monkeypatch.setenv("MAX_UPLOAD_MB", "1")

    with pytest.raises(FileTooLargeError, match="1 MB"):
        validate_upload("resume.pdf", b"%PDF-" + b"x" * (1024 * 1024))


def test_invalid_size_configuration_is_reported(monkeypatch):
    monkeypatch.setenv("MAX_UPLOAD_MB", "large")

    with pytest.raises(ValueError, match="positive integer"):
        validate_upload("resume.pdf", b"%PDF-data")
