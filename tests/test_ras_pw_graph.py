import networkx as nx

from nciraspw.ras_pw_graph import ras_pathway_graph


def test_reading_ras_pathway_graph() -> None:
    gr = ras_pathway_graph()
    assert isinstance(gr, nx.DiGraph)
    assert gr.number_of_edges() > 1
    assert gr.number_of_nodes() > 1
    assert nx.is_directed(gr)
    return None


def test_ras_pathway_graph_single_component() -> None:
    gr = ras_pathway_graph()
    assert nx.number_weakly_connected_components(gr) == 1
    return None
