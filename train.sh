#!/bin/bash

# Usage: ./run_experiment.sh <SEED>
SEED=$1

# Source your Condor environment setup
source /nethome/pjajoria/condor_setup.sh alignment

# Run training with the provided seed
$PYTHON_BIN/python /nethome/pjajoria/Github/lyrics-aligner/train.py \
    --epochs 15 \
    --save_steps 0 \
    --run_name "augmentation$(date +'%d%m_%H%M')" \
    --lr 1e-5 \
    --accumulation_steps 4 \
    --dataset_path "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset" \
    --seed "${SEED}"
    # --forward_pass_sanity


#$PYTHON_BIN/python /nethome/pjajoria/Github/lyrics-aligner/benchmark_forced_aligner.py