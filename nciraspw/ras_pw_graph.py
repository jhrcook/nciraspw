"""Ras pathway graph."""

from typing import Any

import networkx as nx
import pandas as pd

from .read_data import read_edge_list, read_gene_names, read_node_groups


class DataMisalignmentError(BaseException):
    """Data misalignment error."""

    ...


def _split_alternative_gene_names(alt_gene_names: str) -> set[str]:
    return set([g.strip() for g in alt_gene_names.split(",")])


def _add_genes_to_graph(gr: nx.DiGraph, node_list: pd.DataFrame) -> None:
    node_info: list[tuple[str, dict[str, Any]]] = []
    for _, row in node_list.iterrows():
        alt_names = _split_alternative_gene_names(row["alt_gene_names"])
        node_info.append(
            (
                row["gene_name"],
                {
                    "protein_name": row["protein_name"],
                    "alt_gene_names": alt_names,
                    "group_id": row["group_id"],
                },
            )
        )
    gr.add_nodes_from(node_info)
    return None


def _check_all_edge_list_nodes_in_graph(
    gr: nx.DiGraph, edge_list: pd.DataFrame
) -> None:
    gr_nodes = set(gr.nodes)
    el_nodes = set(edge_list["from"].to_list() + edge_list["to"].to_list())
    extra_nodes = el_nodes.difference(gr_nodes)
    if len(extra_nodes) == 0:
        return None
    raise DataMisalignmentError(extra_nodes)


def _add_edges_to_graph(gr: nx.DiGraph, edge_list: pd.DataFrame) -> None:
    edge_info: list[tuple[str, str, dict[str, Any]]] = []
    for _, row in edge_list.iterrows():
        edge_info.append(
            (row["from"], row["to"], {"interaction": row["interaction_type"]})
        )
    gr.add_edges_from(edge_info)
    return None


def ras_pathway_graph() -> nx.DiGraph:
    """Generate the Ras pathway as a graph.

    Returns:
        nx.DiGraph: Ras pathway as a directed graph.
    """
    gr = nx.DiGraph(name="NCI Ras pathway 2.0")
    node_list = (
        read_gene_names()
        .merge(
            read_node_groups(),
            how="left",
            left_on="gene_name",
            right_on="node",
            validate="one_to_one",
        )
        .drop(columns=["node"])
    )
    _add_genes_to_graph(gr, node_list=node_list)
    edge_list = read_edge_list()
    _check_all_edge_list_nodes_in_graph(gr, edge_list=edge_list)
    _add_edges_to_graph(gr, edge_list=edge_list)
    assert nx.number_weakly_connected_components(gr) == 1
    return gr
