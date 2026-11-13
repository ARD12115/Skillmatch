from io import BytesIO
from zipfile import BadZipFile, ZipFile

from docx import Document

from src.utils.errors import EmptyDocumentError, ParseError

MAX_DOCX_UNCOMPRESSED_BYTES = 25 * 1024 * 1024
MAX_DOCX_MEMBERS = 1000
MAX_DOCX_TEXT_CHARACTERS = 500_000


def extract_text_from_docx(data: bytes) -> str:
    """Extract text from a DOCX while limiting archive expansion."""
    try:
        with ZipFile(BytesIO(data)) as archive:
            members = archive.infolist()
            if len(members) > MAX_DOCX_MEMBERS:
                raise ParseError("DOCX archive contains too many files.")
            if (
                sum(member.file_size for member in members)
                > MAX_DOCX_UNCOMPRESSED_BYTES
            ):
                raise ParseError("DOCX contents exceed the safe parsing limit.")
        document = Document(BytesIO(data))
        parts = [paragraph.text for paragraph in document.paragraphs]
        for table in document.tables:
            parts.extend(cell.text for row in table.rows for cell in row.cells)
        text = "\n".join(parts).strip()
    except ParseError:
        raise
    except (BadZipFile, KeyError, ValueError, OSError) as exc:
        raise ParseError("Unable to read this DOCX. Please try another file.") from exc
    except Exception as exc:
        raise ParseError("Unable to read this DOCX. Please try another file.") from exc
    if len(text) > MAX_DOCX_TEXT_CHARACTERS:
        raise ParseError("DOCX text exceeds the safe parsing limit.")
    if not text:
        raise EmptyDocumentError("We couldn't read any text from this DOCX.")
    return text
