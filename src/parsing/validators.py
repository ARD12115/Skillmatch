import os
from pathlib import PurePath

from src.utils.errors import FileTooLargeError, UnsupportedFileError

DEFAULT_MAX_UPLOAD_MB = 5


def max_upload_bytes() -> int:
    raw_limit = os.getenv("MAX_UPLOAD_MB", str(DEFAULT_MAX_UPLOAD_MB))
    try:
        limit_mb = int(raw_limit)
    except ValueError as exc:
        raise ValueError("MAX_UPLOAD_MB must be a positive integer.") from exc
    if limit_mb < 1:
        raise ValueError("MAX_UPLOAD_MB must be a positive integer.")
    return min(limit_mb, DEFAULT_MAX_UPLOAD_MB) * 1024 * 1024


def validate_upload(name: str, data: bytes) -> None:
    """Validate extension, non-empty content, upload size, and file signature."""
    if not data:
        raise UnsupportedFileError("The uploaded file is empty.")
    if len(data) > max_upload_bytes():
        limit_mb = max_upload_bytes() // (1024 * 1024)
        raise FileTooLargeError(f"File exceeds the {limit_mb} MB upload limit.")

    suffix = PurePath(name).suffix.casefold()
    if suffix == ".pdf" and data.startswith(b"%PDF-"):
        return
    if suffix == ".docx" and data.startswith(b"PK\x03\x04"):
        return
    raise UnsupportedFileError("Upload a valid PDF or DOCX file.")
