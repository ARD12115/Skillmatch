from src.utils.text import normalize_text, remove_contact_details


def test_normalizes_case_and_whitespace():
    assert normalize_text("  Python \n ML  ") == "python ml"


def test_removes_email_phone_and_labeled_contact_lines():
    cleaned = remove_contact_details(
        "Email: person@example.com\nPhone: +1 (555) 222-1111\nPython developer"
    )

    assert "person@example.com" not in cleaned
    assert "555" not in cleaned
    assert "Python developer" in cleaned
