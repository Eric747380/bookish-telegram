#!/bin/bash
UNIVERSAL_ITEMSET=$1
NUM_TRANS=$2

python3 generate_dataset.py "$UNIVERSAL_ITEMSET" $NUM_TRANS

