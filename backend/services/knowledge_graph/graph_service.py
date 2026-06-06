import networkx as nx
from sqlalchemy.orm import Session
from backend.models.schemas import ResearchPaper, KnowledgeGraphEdge

# in-memory graph, rebuilt when needed
_graph = None


def build_graph(db: Session) -> nx.Graph:
    global _graph
    _graph = nx.Graph()

    papers = db.query(ResearchPaper).all()

    for paper in papers:
        # add paper node
        _graph.add_node(
            paper.id,
            label=paper.title[:40],
            node_type="paper"
        )

        # connect paper to its algorithms
        for algo in (paper.algorithms_used or []):
            algo_node = f"algo_{algo}"
            if not _graph.has_node(algo_node):
                _graph.add_node(algo_node, label=algo, node_type="algorithm")
            _graph.add_edge(paper.id, algo_node, relationship="uses")

        # connect paper to its datasets
        for dataset in (paper.datasets_used or []):
            ds_node = f"dataset_{dataset}"
            if not _graph.has_node(ds_node):
                _graph.add_node(ds_node, label=dataset, node_type="dataset")
            _graph.add_edge(paper.id, ds_node, relationship="uses_dataset")

        # connect paper to authors
        for author in (paper.authors or []):
            author_node = f"author_{author}"
            if not _graph.has_node(author_node):
                _graph.add_node(author_node, label=author, node_type="author")
            _graph.add_edge(paper.id, author_node, relationship="written_by")

    return _graph


def get_graph_data(db: Session) -> dict:
    graph = build_graph(db)

    nodes = []
    for node_id, data in graph.nodes(data=True):
        nodes.append({
            "id": node_id,
            "label": data.get("label", node_id),
            "type": data.get("node_type", "unknown")
        })

    edges = []
    for source, target, data in graph.edges(data=True):
        edges.append({
            "source": source,
            "target": target,
            "relationship": data.get("relationship", "")
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "total_nodes": len(nodes),
        "total_edges": len(edges)
    }


def get_graph_stats(db: Session) -> dict:
    graph = build_graph(db)

    if len(graph.nodes) == 0:
        return {"message": "No data yet, upload some papers first"}

    # most connected nodes = most influential papers/algorithms
    degree_centrality = nx.degree_centrality(graph)
    top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]

    node_types = {}
    for _, data in graph.nodes(data=True):
        t = data.get("node_type", "unknown")
        node_types[t] = node_types.get(t, 0) + 1

    return {
        "total_nodes": graph.number_of_nodes(),
        "total_edges": graph.number_of_edges(),
        "node_type_breakdown": node_types,
        "most_connected": [
            {"node": n, "score": round(s, 3)} for n, s in top_nodes
        ]
    }