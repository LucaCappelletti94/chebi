"""Submodule defining the DownloadObjective dataclass."""

from dataclasses import dataclass


@dataclass
class DownloadObjective:
    """Dataclass defining the download objective."""

    path: str
    url: str
