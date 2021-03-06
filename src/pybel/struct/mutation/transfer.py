# -*- coding: utf-8 -*-

"""This module facilitates the transfer of knowledge through ontological relationships."""

from ...constants import ANNOTATIONS, CAUSAL_RELATIONS, CITATION, EVIDENCE, IS_A, OBJECT, RELATION, SUBJECT
from ...dsl import BaseEntity

__all__ = [
    'infer_child_relations'
]


def iter_children(graph, node):
    """Iterate over children of the node.

    :type graph: pybel.BELGraph
    :type node: BaseEntity
    :rtype: iter[BaseEntity]
    """
    for u, _, d in graph.in_edges(node, data=True):
        if d[RELATION] != IS_A:
            continue
        yield u


def transfer_causal_edges(graph, source, target):
    """Transfer causal edges that the source has to the target.

    :param pybel.BELGraph graph:
    :type source: BaseEntity
    :type target: BaseEntity
    """
    for _, v, data in graph.out_edges(source, data=True):
        if data[RELATION] not in CAUSAL_RELATIONS:
            continue

        graph.add_qualified_edge(
            target,
            v,
            relation=data[RELATION],
            evidence=data[EVIDENCE],
            citation=data[CITATION],
            annotations=data.get(ANNOTATIONS),
            subject_modifier=data.get(SUBJECT),
            object_modifier=data.get(OBJECT)
        )

    for u, _, data in graph.in_edges(source, data=True):
        if data[RELATION] not in CAUSAL_RELATIONS:
            continue

        graph.add_qualified_edge(
            u,
            target,
            relation=data[RELATION],
            evidence=data[EVIDENCE],
            citation=data[CITATION],
            annotations=data.get(ANNOTATIONS),
            subject_modifier=data.get(SUBJECT),
            object_modifier=data.get(OBJECT)
        )


def infer_child_relations(graph, node):
    """Propagate causal relations to children.

    :param pybel.BELGraph graph: A BEL graph
    :param node: A PyBEL node tuple, on which to propagate the children's relations
    :type node: tuple or BaseEntity
    """
    if not isinstance(node, BaseEntity):
        raise TypeError

    for child in iter_children(graph, node):
        transfer_causal_edges(graph, node, child)
        infer_child_relations(graph, child)
