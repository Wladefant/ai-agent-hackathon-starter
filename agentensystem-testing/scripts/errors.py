"""
Custom Exception classes for the project.

Only the exceptions actually raised/caught by the current scripts are kept here.
Earlier deterministic-scorer and Python-remediation scripts (and their bespoke
exceptions) were removed when validation/remediation moved to the LLM bridges.
"""


class ProjectError(Exception):
    """Base exception class for the project."""
    pass


class FileOperationError(ProjectError):
    """Exception raised for errors during file operations."""
    pass

