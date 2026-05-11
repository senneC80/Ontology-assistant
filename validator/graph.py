"""JSON → (gen_graph, rdf_graph) via ontouml-json2graph + NetworkX."""
from __future__ import annotations
import json
import os
import tempfile

import networkx as nx
from rdflib import Graph, Namespace

from json2graph.decode import decode_ontouml_json2graph

ONTOUML = Namespace("https://w3id.org/ontouml#")


def build_graphs(project: dict) -> tuple[nx.DiGraph, Graph]:
    """Build a NetworkX generalization graph and an RDFLib graph.

    gen_graph nodes carry 'name' and 'stereotype' attributes; edges go
    specific → general. gen_graph.graph['full_undirected'] is an undirected
    Graph with all class connections (relations + generalizations) for
    island detection.
    """
    contents = project.get("model", {}).get("contents", [])

    classes = {}
    for elem in contents:
        if elem.get("type") == "Class":
            classes[elem["id"]] = {
                "name": _resolve_name(elem.get("name", "")),
                "stereotype": elem.get("stereotype", ""),
            }

    gen_graph = nx.DiGraph()
    for cid, info in classes.items():
        gen_graph.add_node(cid, name=info["name"], stereotype=info["stereotype"])

    for elem in contents:
        if elem.get("type") == "Generalization":
            s = elem.get("specific", {}).get("id")
            g = elem.get("general", {}).get("id")
            if s and g:
                if s not in gen_graph:
                    gen_graph.add_node(s, name="", stereotype="")
                if g not in gen_graph:
                    gen_graph.add_node(g, name="", stereotype="")
                gen_graph.add_edge(s, g)

    full = nx.Graph()
    for cid in classes:
        full.add_node(cid)
    for elem in contents:
        if elem.get("type") == "Generalization":
            s = elem.get("specific", {}).get("id")
            g = elem.get("general", {}).get("id")
            if s and g:
                full.add_node(s); full.add_node(g)
                full.add_edge(s, g)
        elif elem.get("type") == "Relation":
            props = elem.get("properties", [])
            ends = [
                p.get("propertyType", {}).get("id")
                for p in props
                if p.get("propertyType", {}).get("id")
            ]
            for i in range(len(ends)):
                for j in range(i + 1, len(ends)):
                    full.add_edge(ends[i], ends[j])
    gen_graph.graph["full_undirected"] = full

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    try:
        json.dump(project, tmp)
        tmp.close()
        rdf_graph = decode_ontouml_json2graph(
            tmp.name, execution_mode="test", silent=True
        )
    finally:
        os.unlink(tmp.name)

    return gen_graph, rdf_graph


def _resolve_name(name) -> str:
    """Handle both plain strings and {'en': 'Name'} multilingual format."""
    if isinstance(name, dict):
        return name.get("en") or next(iter(name.values()), "")
    return str(name) if name else ""