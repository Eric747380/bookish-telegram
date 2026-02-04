#!/bin/bash
GS=$1; FS=$2; GT=$3; DS=$4; OUT=$5
mkdir -p $OUT
python3 convert_yeast_to_dat.py $DS yeast_gspan.dat
python3 convert_yeast_to_fsg.py $DS yeast_fsg.dat
python3 convert_yeast_to_gaston.py $DS yeast_gaston.dat
num_graphs=$(grep -c '^#' $DS)
supports=(5 10 25 50 95)
for s in "${supports[@]}"; do
  frac_sup=$(echo "scale=2; ($s) / 100" | bc)
  abs_sup=$(echo "scale=0; ($s * $num_graphs) / 100" | bc)
  timeout 3600 /usr/bin/time -f "%e" -o $OUT/gspan$s.time $GS -f yeast.dat -s $frac_sup -o /dev/null > /dev/null 2>&1
  timeout 3600 /usr/bin/time -f "%e" -o $OUT/fsg$s.time $FS yeast_fsg.dat -s$s /dev/null > /dev/null 2>&1
  timeout 3600 /usr/bin/time -f "%e" -o $OUT/gaston$s.time $GT -s $abs_sup -f yeast_gaston.dat /dev/null > /dev/null 2>&1
done
python3 plot_q2.py $OUT
