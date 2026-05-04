"""Project-specific exception types."""


class NeksusError(Exception):
    """Base exception for Neksus errors."""


class FileSystemError(NeksusError):
    """Raised for filesystem-related failures."""


class ConfigError(NeksusError):
    """Raised for project config errors."""


class JobSpecParseError(NeksusError):
    """Raised when a JobSpec YAML file cannot be parsed."""


class JobSpecValidationError(NeksusError):
    """Raised when a JobSpec fails schema validation."""


class UnsupportedFormatError(NeksusError):
    """Raised when a render format is unsupported."""
