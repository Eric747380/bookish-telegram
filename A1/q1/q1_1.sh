#!/bin/bash
APRIORI=$1
FP=$2
DATA=$3
OUT=$4
mkdir -p $OUT
THRESHOLDS=(5 10 25 50 90)
TIMES=()

for t in "${THRESHOLDS[@]}"; do
    timeout 3600 /usr/bin/time -f "%e" "$APRIORI" -s"$t" "$DATA" "$OUT/ap$t" > /dev/null 2> ap_time$t.txt
    last_line=$(tail -n 1 ap_time$t.txt 2>/dev/null)  # Get last line, suppress errors if file missing
    atime=0
    if echo "$last_line" | grep -Eq '^[0-9]+(\.[0-9]+)?$'; then  # Check if it's a float (int or decimal)
        atime="$last_line"
    else
        atime=3600
    fi
    TIMES+=("${atime:-0}")

    timeout 3600 /usr/bin/time -f "%e" "$FP" -s"$t" "$DATA" "$OUT/fp$t" > /dev/null 2> fp_time$t.txt
    last_line=$(tail -n 1 fp_time$t.txt 2>/dev/null)  # Get last line, suppress errors if file missing
    ftime=0
    if echo "$last_line" | grep -Eq '^[0-9]+(\.[0-9]+)?$'; then  # Check if it's a float (int or decimal)
        ftime="$last_line"
    else
        ftime=3600
    fi
    TIMES+=("${ftime:-0}")
done

python3 plot_q1_1.py "${THRESHOLDS[@]}" "${TIMES[@]}" $OUT/plot.png
