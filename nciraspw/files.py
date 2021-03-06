"""Data files."""


import importlib.resources as pkg_resources
from enum import Enum
from typing import Final

from . import ras_pw_data


class RasPathwayDataFile(Enum):
    """Ras pathway data files."""

    GENE_NAMES = "GENE_NAMES"
    GENE_NAMES_CUSTOM = "GENE_NAMES_CUSTOM"
    NODE_GROUPS = "NODE_GROUPS"
    GROUP_EDGE_LIST = "GROUP_EDGE_LIST"
    PROTEIN_COMPLEXES = "PROTEIN_COMPLEXES"


def ras_pw_file_name(ras_pw_file: RasPathwayDataFile) -> str:
    """File name for a Ras pathway data file."""
    file_map: Final[dict[RasPathwayDataFile, str]] = {
        RasPathwayDataFile.GENE_NAMES: "ras-pathway-gene-names.csv",
        RasPathwayDataFile.GENE_NAMES_CUSTOM: "ras-pathway-gene-names_custom.csv",
        RasPathwayDataFile.NODE_GROUPS: "ras-pathway-node-groups.csv",
        RasPathwayDataFile.GROUP_EDGE_LIST: "ras-pathway-group-interactions.csv",
        RasPathwayDataFile.PROTEIN_COMPLEXES: "ras-pathway-protein-complexes.txt",
    }
    return file_map[ras_pw_file]


def ras_pw_file_exists(ras_pw_file: RasPathwayDataFile) -> bool:
    """Does the Ras pathway data file exist?"""
    return pkg_resources.is_resource(ras_pw_data, ras_pw_file_name(ras_pw_file))
