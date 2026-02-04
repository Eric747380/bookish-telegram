import networkx as nx
import numpy as np
from collections import Counter
from networkx.algorithms import isomorphism
from functools import lru_cache


# ============================================================
# GRAPH PARSING
# ============================================================

def load_graphs(graphs_txt_path):
    graphs = []
    G = None

    with open(graphs_txt_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("#"):
                if G is not None:
                    graphs.append(G)
                G = nx.Graph()

            elif line.startswith("v"):
                _, vid, label = line.split()
                G.add_node(int(vid), label=label)

            elif line.startswith("e"):
                _, u, v, label = line.split()
                G.add_edge(int(u), int(v), label=label)

        if G is not None:
            graphs.append(G)

    return graphs


# ============================================================
# SUBGRAPH ISOMORPHISM (CACHED)
# ============================================================

@lru_cache(maxsize=None)
def _iso_key(small_edges, big_edges):
    return small_edges, big_edges


def is_subgraph(small, big):
    nm = lambda a, b: a["label"] == b["label"]
    em = lambda a, b: a["label"] == b["label"]

    gm = isomorphism.GraphMatcher(
        big, small,
        node_match=nm,
        edge_match=em
    )
    return gm.subgraph_is_isomorphic()


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def edge_features(G):
    feats = []
    for u, v, data in G.edges(data=True):
        lu = G.nodes[u]["label"]
        lv = G.nodes[v]["label"]
        le = data["label"]
        feats.append(("E", lu, le, lv))
    return feats



def path2_features(G):
    feats = set()
    for v in G.nodes:
        lv = G.nodes[v]["label"]
        neigh = list(G.neighbors(v))
        for i in range(len(neigh)):
            for j in range(i + 1, len(neigh)):
                u, w = neigh[i], neigh[j]
                lu = G.nodes[u]["label"]
                lw = G.nodes[w]["label"]
                le1 = G[u][v]["label"]
                le2 = G[v][w]["label"]
                feats.add(("P2", lu, le1, lv, le2, lw))
    return feats


def mine_features(graphs_txt, max_features=700):
    graphs = load_graphs(graphs_txt)
    counter = Counter()

    for G in graphs:
        counter.update(path2_features(G))
        counter.update(edge_features(G))

    n_graphs = len(graphs)

    # frequency window
    min_freq = 3
    max_freq = int(0.08 * n_graphs)

    p2_feats = []
    edge_feats = []

    for f, c in counter.items():
        if f[0] == "P2":
            # strict frequency window for P2
            if min_freq <= c <= max_freq:
                p2_feats.append(f)
        else:
            # EDGE FALLBACK: ignore max_freq
            if c >= min_freq:
                edge_feats.append(f)


    # sort by rarity
    p2_feats.sort(key=lambda f: counter[f])
    edge_feats.sort(key=lambda f: counter[f])

    # FORCE edge fallback
    NUM_EDGE_FALLBACK = 80

    features = (
        p2_feats[: max_features - NUM_EDGE_FALLBACK] +
        edge_feats[: NUM_EDGE_FALLBACK]
    )

    return features


# ============================================================
# FEATURE → GRAPH
# ============================================================

def feature_to_graph(feat):
    if feat[0] == "E":
        _, lu, le, lv = feat
        G = nx.Graph()
        G.add_node(0, label=lu)
        G.add_node(1, label=lv)
        G.add_edge(0, 1, label=le)
        return G

    if feat[0] == "P2":
        _, lu, le1, lv, le2, lw = feat
        G = nx.Graph()
        G.add_node(0, label=lu)
        G.add_node(1, label=lv)
        G.add_node(2, label=lw)
        G.add_edge(0, 1, label=le1)
        G.add_edge(1, 2, label=le2)
        return G

    raise ValueError("Unknown feature type")


# ============================================================
# GRAPH → FEATURE VECTOR (+ STRUCTURAL METADATA)
# ============================================================

def graph_metadata(G):
    return (
        G.number_of_nodes(),
        G.number_of_edges(),
        max(dict(G.degree()).values()) if G.number_of_nodes() > 0 else 0
    )


def convert(graphs_txt, features):
    graphs = load_graphs(graphs_txt)
    feature_graphs = [feature_to_graph(f) for f in features]

    X = np.zeros((len(graphs), len(features)), dtype=np.uint8)
    meta = np.zeros((len(graphs), 3), dtype=np.int32)

    for i, G in enumerate(graphs):
        meta[i] = graph_metadata(G)
        edge_counts = Counter(edge_features(G))

        for j, fg in enumerate(features):
            if fg[0] == "E":
                X[i, j] = edge_counts.get(fg, 0)
            else:
                if is_subgraph(feature_graphs[j], G):
                    X[i, j] = 1

    return X, meta


# ============================================================
# CANDIDATE GENERATION (WITH STRUCTURAL FILTERS)
# ============================================================

def generate_candidates(db_vecs, q_vecs, db_meta, q_meta):
    results = []

    for qi in range(q_vecs.shape[0]):
        qv = q_vecs[qi]
        qn, qe, qd = q_meta[qi]
        valid = []

        for gi in range(db_vecs.shape[0]):
            dn, de, dd = db_meta[gi]

            # structural necessary conditions
            if qn > dn or qe > de or qd > dd:
                continue

            if np.all(qv <= db_vecs[gi]):
                valid.append(gi)

        results.append(valid)

    return results
