"""Submodule defining exceptions used across the ChEBI package."""

from chebi.exceptions.version_exception import VersionException
from chebi.exceptions.unavailable_entry import UnavailableEntry

__all__ = [
    "VersionException",
    "UnavailableEntry",
]
