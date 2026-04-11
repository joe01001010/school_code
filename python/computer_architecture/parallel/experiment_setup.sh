#!/usr/bin/env bash

for num in {1,2,4,8,16}; do
  echo "Running with ${num} threads"
  export OMP_NUM_THREADS=${num}
  export MKL_NUM_THREADS=${num}
  export OPENBLAS_NUM_THREADS=${num}
  python ./incline_compute_graphing.py
done
