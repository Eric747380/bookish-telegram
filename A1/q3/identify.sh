#!/bin/bash
set -e

DATASET_PATH=$1
FEATURE_OUT=$2

python3 - << EOF
import pickle
from indexer import mine_features

features = mine_features(
    graphs_txt="${DATASET_PATH}/graphs.txt",
    max_features=300
)

with open("${FEATURE_OUT}", "wb") as f:
    pickle.dump(features, f)
EOF

