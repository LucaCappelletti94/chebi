"""Class representing a ChEBI Dataset."""

from typing import Dict, Any, List
from downloaders import BaseDownloader
from chebi.settings import DatasetSettings


class Dataset:
    """Class representing a ChEBI Dataset."""

    def __init__(self, metadata: Dict[str, Any]):
        """Initialize the ChEBI Dataset."""

    @staticmethod
    def build(settings: DatasetSettings) -> "Dataset":
        """Build a ChEBI Dataset."""

        paths: List[str] = []
        urls: List[str] = []

        for objective in settings.download_objectives():
            paths.append(objective.path)
            urls.append(objective.url)

        BaseDownloader(
            process_number=1,
            verbose=settings.verbose,
            # We need to set the sleep time to 2 seconds
            # to avoid being blocked by the server.
            sleep_time=2,
        ).download(urls=urls, paths=paths)

        return Dataset(metadata=settings.into_dict())
