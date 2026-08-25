"""
Analisis de grafos de pases con NetworkX.
Centralidad, comunidades, PageRank, metricas de red.
"""

import json
from pathlib import Path

try:
    import csv

    import networkx as nx
    from networkx.algorithms.community import greedy_modularity_communities

    AVAILABLE = True
except ImportError:
    AVAILABLE = False


def build_graph(csv_path: Path) -> "nx.DiGraph":
    G = nx.DiGraph()
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            src = row.get("source", "")
            tgt = row.get("target", "")
            w = int(row.get("weight", 1))
            if src and tgt:
                G.add_edge(src, tgt, weight=w)
    return G


def run_graph_analysis(
    data_dir: Path = Path("data/export"), output_dir: Path = Path("data/export")
) -> dict:
    if not AVAILABLE:
        print("[GRAPH] networkx no instalado")
        return {}

    results = {}
    for csv_file in data_dir.glob("*.csv"):
        G = build_graph(csv_file)
        if len(G.nodes) < 2:
            continue

        name = csv_file.stem
        betweenness = nx.betweenness_centrality(G)
        pagerank = nx.pagerank(G)
        degree = nx.degree_centrality(G)

        G_undir = G.to_undirected()
        try:
            communities = list(greedy_modularity_communities(G_undir))
            n_comm = len(communities)
        except Exception:
            n_comm = 0

        metrics = {
            "nodes": len(G.nodes),
            "edges": len(G.edges),
            "density": round(nx.density(G), 4),
            "n_communities": n_comm,
            "top_betweenness": [
                {"player": p, "score": round(s, 4)}
                for p, s in sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
            ],
            "top_pagerank": [
                {"player": p, "score": round(s, 4)}
                for p, s in sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:5]
            ],
            "top_degree": [
                {"player": p, "score": round(s, 4)}
                for p, s in sorted(degree.items(), key=lambda x: x[1], reverse=True)[:5]
            ],
        }
        results[name] = metrics
        print(
            f"[GRAPH] {name}: {metrics['nodes']} nodos, {metrics['edges']} aristas, {n_comm} comunidades"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "graph_analysis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results


if __name__ == "__main__":
    run_graph_analysis()
