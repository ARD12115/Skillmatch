import re

_EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
_PHONE = re.compile(r"(?<!\w)(?:\+?\d[\d().\s-]{5,}\d)(?!\w)")
_CONTACT_LINE = re.compile(r"(?im)^\s*(?:phone|mobile|email|address|contact)\s*:\s*.*$")


def normalize_text(text: str) -> str:
    """Normalize whitespace and case while preserving skill punctuation."""
    return re.sub(r"\s+", " ", text.casefold()).strip()


def remove_contact_details(text: str) -> str:
    """Remove common contact fields before computing semantic similarity."""
    without_contact_lines = _CONTACT_LINE.sub(" ", text)
    without_email = _EMAIL.sub(" ", without_contact_lines)
    return re.sub(r"\s+", " ", _PHONE.sub(" ", without_email)).strip()
