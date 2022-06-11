import pandas as pd
import pytest

from nciraspw import read_data


def test_read_edge_list() -> None:
    edge_list = read_data.read_edge_list()
    assert isinstance(edge_list, pd.DataFrame)
    assert len(edge_list) > 0


def test_read_gene_names() -> None:
    gene_names = read_data.read_gene_names()
    assert isinstance(gene_names, pd.DataFrame)
    assert len(gene_names) > 0


@pytest.mark.parametrize("expand", (True, False))
def test_read_node_groups(expand: bool) -> None:
    node_groups = read_data.read_node_groups(expand=expand)
    assert isinstance(node_groups, pd.DataFrame)
    assert len(node_groups) > 0


def test_read_node_group_interactions() -> None:
    node_groups = read_data.read_node_group_interactions()
    assert isinstance(node_groups, pd.DataFrame)
    assert len(node_groups) > 0


def test_read_protein_complexes() -> None:
    complexes = read_data.read_protein_complexes()
    assert len(complexes) > 0
    for complex in complexes:
        assert len(complex) > 1


def test_all_complex_nodes_in_gene_names() -> None:
    gene_names = set(read_data.read_gene_names()["gene_name"].unique())
    complexes = read_data.read_protein_complexes()
    complex_nodes: set[str] = set()
    for complex in complexes:
        complex_nodes = complex_nodes.union(complex)
    assert len(complex_nodes.difference(gene_names)) == 0
