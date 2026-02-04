#!/usr/bin/env bash
set -e

GRAPH_PATH=$1
FEATURE_PATH=$2
OUT_PATH=$3

python3 - << EOF
import os
import pickle
import numpy as np
from indexer import convert

with open("${FEATURE_PATH}", "rb") as f:
    features = pickle.load(f)

graphs_txt = "${GRAPH_PATH}"
if os.path.isdir(graphs_txt):
    graphs_txt = os.path.join(graphs_txt, "graphs.txt")

X, meta = convert(
    graphs_txt=graphs_txt,
    features=features
)

# save feature vectors
np.save("${OUT_PATH}", X)

# save metadata alongside
np.save("${OUT_PATH}.meta", meta)
EOF
