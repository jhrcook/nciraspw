"""Read the data files."""

import importlib.resources as pkg_resources
from enum import Enum

import janitor  # noqa: F401
import pandas as pd

from . import ras_pw_data
from .files import RasPathwayDataFile, ras_pw_file_exists, ras_pw_file_name


class MissingRasPwDataError(BaseException):
    """Missing Ras pathway data error."""

    ...


def _check_and_read_csv(data_file: RasPathwayDataFile) -> pd.DataFrame:
    if not ras_pw_file_exists(data_file):
        raise MissingRasPwDataError(data_file.value)

    with pkg_resources.path(ras_pw_data, ras_pw_file_name(data_file)) as fpath:
        edge_list = pd.read_csv(str(fpath))

    return edge_list


class Interaction(Enum):
    """Protein-protein interaction types."""

    ACTIVATING = "ACTIVATING"
    INHIBITORY = "INHIBITORY"
    SCAFFOLDING = "SCAFFOLDING"
    PROTEIN_COMPLEX = "PROTEIN_COMPLEX"


def read_gene_names() -> pd.DataFrame:
    """Read Ras pathway gene names file."""
    gene_name_files = [
        RasPathwayDataFile.GENE_NAMES,
        RasPathwayDataFile.GENE_NAMES_CUSTOM,
    ]
    return (
        pd.concat([_check_and_read_csv(f) for f in gene_name_files])
        .reset_index(drop=True)
        .clean_names()
        .rename(
            columns={
                "protein_name_from_biogps": "protein_name",
                "alternative_gene_names_from_biogps": "alt_gene_names",
            }
        )
    )


def _split_node_groups(grp: str) -> list[str]:
    return [x.upper().strip() for x in grp.split(",")]


def read_node_groups(expand: bool = True) -> pd.DataFrame:
    """Read Ras pathway node groups file.

    Args:
        expand (bool, optional): Expand the node groups to nodes. Defaults to True.

    Returns:
        pd.DataFrame: Node groups data frame.
    """
    node_groups = _check_and_read_csv(RasPathwayDataFile.NODE_GROUPS).astype(
        {"group_id": str}
    )
    if not expand:
        return node_groups

    nodes: list[str] = []
    infos: list[pd.Series] = []
    for group, info in node_groups.set_index("nodes").iterrows():
        assert isinstance(group, str)
        grp_nodes = _split_node_groups(group)
        nodes += grp_nodes
        infos = infos + ([info] * len(grp_nodes))
    assert len(nodes) == len(infos)
    return pd.DataFrame(infos).reset_index(drop=True).assign(node=nodes)


def read_node_group_interactions() -> pd.DataFrame:
    """Read Ras pathway node group interactions data.

    Returns:
        pd.DataFrame: Node group interactions data frame.
    """
    return (
        _check_and_read_csv(RasPathwayDataFile.GROUP_EDGE_LIST)
        .astype({"from": str, "to": str})
        .rename(columns={"from": "from_grp", "to": "to_grp"})
    )


def read_edge_list() -> pd.DataFrame:
    """Read the Ras pathway edge list.

    Returns:
        pd.DataFrame: Edge list.
    """
    node_grps = read_node_groups(expand=True)
    edge_grps = read_node_group_interactions()

    return (
        edge_grps.copy()
        .merge(node_grps, how="left", left_on="from_grp", right_on="group_id")
        .rename(columns={"node": "from"})
        .drop(columns=["group_id"])
        .merge(node_grps, how="left", left_on="to_grp", right_on="group_id")
        .rename(columns={"node": "to"})
        .drop(columns=["group_id"])[["from", "to", "interaction_type"]]
    )
