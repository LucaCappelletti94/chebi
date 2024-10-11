"""Submodule providing the settings for constructing versions of the ChEBI dataset."""

import os
from typing import Any, Dict, List
import compress_json
from chebi.exceptions import VersionException, UnavailableEntry
from chebi.utils import DownloadObjective


class DatasetSettings:
    """Class defining the settings for constructing versions of the ChEBI dataset."""

    def __init__(self, version: str):
        """Initialize the settings for constructing versions of the ChEBI dataset."""
        local_version_path = os.path.join(
            os.path.dirname(__file__), "versions", f"{version}.json"
        )

        if not os.path.exists(local_version_path):
            available_versions = os.listdir(
                os.path.join(os.path.dirname(__file__), "versions")
            )
            raise VersionException(version, available_versions)

        self._version_metadata: Dict[str, Any] = compress_json.load(local_version_path)
        self._only_three_stars: bool = False
        self._generate_smiles: bool = False
        self._to_include: List[str] = []
        self._verbose: bool = False
        self._downloads_directory: str = "downloads"

    @staticmethod
    def available_versions() -> List[str]:
        """Return the available versions of the ChEBI dataset."""
        return [
            version.replace(".json", "")
            for version in os.listdir(
                os.path.join(os.path.dirname(__file__), "versions")
            )
        ]

    def download_objectives(self) -> List[DownloadObjective]:
        """Return the download objectives."""
        download_objectives: List[DownloadObjective] = []
        for included in self._to_include:
            data = self._version_metadata[included]
            if self._only_three_stars:
                url = data["three_stars"]
            else:
                url = data["all"]

            file_name = url.split("/")[-1]
            path = os.path.join(
                self._downloads_directory, self._version_metadata["version"], file_name
            )
            download_objectives.append(DownloadObjective(path, url))

        return download_objectives

    def into_dict(self) -> Dict[str, Any]:
        """Return the settings as a dictionary."""
        return {
            "version": self._version_metadata["version"],
            "year": self._version_metadata["year"],
            "month": self._version_metadata["month"],
            "day": self._version_metadata["day"],
            "only_three_stars": self._only_three_stars,
            "generate_smiles": self._generate_smiles,
            "to_include": self._to_include,
        }

    def include_only_three_star_entries(self) -> "DatasetSettings":
        """Include only entries with three stars."""
        self._only_three_stars = True
        return self

    def _include(self, key: str) -> "DatasetSettings":
        """Include a specific key."""
        if key not in self._version_metadata:
            raise UnavailableEntry(
                key,
                list(
                    {
                        key
                        for key in self._version_metadata.keys()
                        if key not in ["version", "year", "month", "day"]
                    }
                ),
            )
        if key not in self._to_include:
            self._to_include.append(key)
        return self

    def include_inchikeys(self) -> "DatasetSettings":
        """Sets to include InChIKeys when constructing the dataset."""
        return self._include("inchikeys")

    def set_downloads_directory(self, directory: str) -> "DatasetSettings":
        """Sets the directory to download files."""
        self._downloads_directory = directory
        return self

    @property
    def verbose(self) -> bool:
        """Return whether the settings are in verbose mode."""
        return self._verbose

    def set_verbose(self) -> "DatasetSettings":
        """Sets to verbose mode."""
        self._verbose = True
        return self

    def generate_smiles(self) -> "DatasetSettings":
        """Sets to generate SMILES when constructing the dataset."""
        self._generate_smiles = True
        return self._include("inchikeys")

    def include_chemical_data(self) -> "DatasetSettings":
        """Sets to include chemical data when constructing the dataset."""
        return self._include("chemical_data")

    def include_comments(self) -> "DatasetSettings":
        """Sets to include comments when constructing the dataset."""
        return self._include("comments")

    def include_compound_origins(self) -> "DatasetSettings":
        """Sets to include compound origins when constructing the dataset."""
        return self._include("compound_origins")

    def include_compounds(self) -> "DatasetSettings":
        """Sets to include compounds when constructing the dataset."""
        return self._include("compounds")

    def include_dataset_accession(self) -> "DatasetSettings":
        """Sets to include dataset accessions when constructing the dataset."""
        return self._include("dataset_accession")

    def include_names(self) -> "DatasetSettings":
        """Sets to include names when constructing the dataset."""
        return self._include("names")

    def include_reference(self) -> "DatasetSettings":
        """Sets to include references when constructing the dataset."""
        return self._include("reference")

    def include_relation(self) -> "DatasetSettings":
        """Sets to include relations when constructing the dataset."""
        return self._include("relation")

    def include_structures(self) -> "DatasetSettings":
        """Sets to include structures when constructing the dataset."""
        return self._include("structures")

    def include_all(self) -> "DatasetSettings":
        """Include all keys."""
        for key in self._version_metadata.keys():
            if key not in ["version", "year", "month", "day"]:
                self._to_include.append(key)
        return self
