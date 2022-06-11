import pandas as pd

from nciraspw import read_data


def test_read_edge_list() -> None:
    edge_list = read_data.read_edge_list()
    assert isinstance(edge_list, pd.DataFrame)
    assert len(edge_list) > 0


def test_read_gene_names() -> None:
    gene_names = read_data.read_gene_names()
    assert isinstance(gene_names, pd.DataFrame)
    assert len(gene_names) > 0
