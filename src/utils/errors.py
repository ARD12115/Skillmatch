class SkillMatchError(Exception):
    """Base class for expected, user-facing application errors."""


class UnsupportedFileError(SkillMatchError):
    """The uploaded file type or signature is unsupported."""


class FileTooLargeError(SkillMatchError):
    """The uploaded file exceeds the configured size limit."""


class EmptyDocumentError(SkillMatchError):
    """A document contains no extractable text."""


class ParseError(SkillMatchError):
    """A document could not be parsed."""


class TaxonomyError(SkillMatchError):
    """The skill taxonomy is invalid or cannot be loaded."""
