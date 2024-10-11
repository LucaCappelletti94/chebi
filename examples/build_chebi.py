"""Example script to build a ChEBI version."""

import argparse
from tqdm.auto import tqdm
from chebi import Dataset, DatasetSettings


def build_chebi(version: str) -> Dataset:
    """Build a ChEBI version."""
    settings = DatasetSettings(version=version).include_all().set_verbose()
    return Dataset.build(settings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a ChEBI version.")
    parser.add_argument(
        "--version",
        type=str,
        help="The version of the ChEBI Dataset to build.",
    )
    args = parser.parse_args()

    if args.version == "all":
        versions = DatasetSettings.available_versions()
    else:
        versions = [args.version]

    for v in tqdm(
        versions,
        desc="Building ChEBI versions",
        unit="version",
        disable=len(versions) == 1,
    ):
        _dataset: Dataset = build_chebi(v)
