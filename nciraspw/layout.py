"""Pathway plotting layout."""

from typing import Callable

import janitor  # noqa: F401
import networkx as nx
import numpy as np
import pandas as pd

from nciraspw.read_data import read_node_groups

GraphLayout = dict[str, tuple[float, float]]


def _group_layout_positions(
    node_group: pd.DataFrame,
    scale: float = 1,
    eps: float = 0.5,
    layout_fxn: Callable[[nx.Graph], GraphLayout] = nx.spring_layout,
) -> pd.DataFrame:
    scale = scale * len(node_group) ** eps
    comp_gr = nx.complete_graph(n=len(node_group))
    layout = layout_fxn(comp_gr)
    x = np.asarray([pos[0] for pos in layout.values()])
    y = np.asarray([pos[1] for pos in layout.values()])
    node_group["x"] = node_group["x"] + (x * scale)
    node_group["y"] = node_group["y"] + (y * scale)
    return node_group


def nci_ras_pathway_positions(
    gr: nx.DiGraph,
    scale: float = 10,
    eps: float = 0.5,
    layout_fxn: Callable[[nx.Graph], GraphLayout] = nx.spring_layout,
) -> GraphLayout:
    """Graph layout for the Ras pathway.

    Args:
        gr (nx.DiGraph): Graph pathway graph object.
        scale (float, optional): Multiplier to scale the spread of the groups of nodes.
        Defaults to 10.
        eps (float, optional): Scaler to increase the spread for larger groups of nodes.
        A value of 0 results in no difference in spread based on sie of rhe graph. The
        value provided is used as the exponent on the number of nodes which is then
        multiplied by the scale value. Defaults to 1.
        layout_fxn (Callable[[nx.Graph], GraphLayout], optional): Function to provide
        the layout for each group of nodes. Defaults to nx.spring_layout.

    Returns:
        GraphLayout: Graph layout as a dictionary of node names to (x,y) position.
    """
    node_groups = (
        read_node_groups()
        .filter_column_isin("node", gr.nodes)
        .groupby(["group_id"])
        .apply(_group_layout_positions, scale=scale, eps=eps, layout_fxn=layout_fxn)
    )
    positions: dict[str, tuple[float, float]] = {}
    for _, row in node_groups.iterrows():
        positions[row["node"]] = (row["x"], -row["y"])
    return positions
