#!/usr/bin/env bash
set -e

DB_FEATS=$1
Q_FEATS=$2
OUT_FILE=$3

python3 - << EOF
import numpy as np
from indexer import generate_candidates

db = np.load("${DB_FEATS}")
q = np.load("${Q_FEATS}")

db_meta = np.load("${DB_FEATS}.meta.npy")
q_meta = np.load("${Q_FEATS}.meta.npy")

cands = generate_candidates(db, q, db_meta, q_meta)

with open("${OUT_FILE}", "w") as f:
    for i, cand in enumerate(cands):
        f.write(f"q # {i}\n")
        f.write("c # " + " ".join(map(str, cand)) + "\n")
EOF
