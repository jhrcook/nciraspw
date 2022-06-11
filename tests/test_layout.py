import random

import networkx as nx
import numpy as np

from nciraspw.layout import GraphLayout, nci_ras_pathway_positions
from nciraspw.ras_pw_graph import ras_pathway_graph


def _check_layout(layout: GraphLayout, gr: nx.Graph) -> None:
    assert len(layout) == gr.number_of_nodes()
    coords = np.asarray(list(layout.values()))
    assert np.all(~np.isnan(coords))
    assert np.all(np.isfinite(coords))


def test_ras_pw_layout() -> None:
    gr = ras_pathway_graph()
    layout = nci_ras_pathway_positions(gr)
    _check_layout(layout, gr)


def test_ras_pw_layout_on_partial_graph() -> None:
    nodes = list(ras_pathway_graph().nodes)
    for _ in range(5):
        sub_gr = nx.subgraph(ras_pathway_graph(), random.sample(nodes, 25))
        layout = nci_ras_pathway_positions(sub_gr)
        _check_layout(layout, sub_gr)
