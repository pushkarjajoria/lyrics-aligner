#!/bin/bash

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Run the training script with specified options."
    echo ""
    echo "Options:"
    echo "  --epochs <value>             Number of epochs for training (default is 50 in train.py)"
    echo "  --save_steps <value>         Number of steps to save (default is 10). Set 0 for not saving intermediate checkpoints."
    echo "  --run_name <value>           Name of the run (default is current date-time in train.py)"
    echo "  --lr <value>                 Learning rate (default is 1e-5 in train.py)"
    echo "  --accumulation_steps <value> Accumulation steps for gradient accumulation (default is 3 in train.py)"
    echo "  --forward_pass_sanity        Run a single forward pass for sanity check (default is off)"
    echo "  -h, --help                   Display this help and exit"
}

# If the first argument is -h or --help, display usage and exit.
if [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
    usage
    exit 0
fi

# Change directory to the project root
cd ~/Git/lyrics-aligner/

# Activate the conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate aligner_train

# Load necessary modules
module load cuda/11.4

# Set wandb to offline mode
export WANDB_MODE=offline

# Variables to store arguments if provided
EPOCHS_ARG=""
SAVE_STEPS_ARG=""
RUN_NAME_ARG=""
FORWARD_PASS_SANITY_ARG=""
LR_ARG=""
ACCUMULATION_STEPS_ARG=""

# Process input arguments: validates numeric inputs for --epochs and --save_steps,
# ensures valid string for --run_name, and checks presence of --forward_pass_sanity
while (( "$#" )); do
  case "$1" in
    --epochs)
      if [[ $2 =~ ^[0-9]+$ ]]; then
        EPOCHS_ARG="--epochs $2"
        shift 2
      else
        echo "Error: Expected a numeric value after --epochs."
        exit 1
      fi
      ;;
    --save_steps)
      if [[ $2 =~ ^[0-9]+$ ]]; then
        SAVE_STEPS_ARG="--save_steps $2"
        shift 2
      else
        echo "Error: Expected a numeric value after --save_steps."
        exit 1
      fi
      ;;
    --run_name)
      if [[ -n $2 && ! $2 =~ ^-- ]]; then
        RUN_NAME_ARG="--run_name $2"
        shift 2
      else
        echo "Error: Expected a string value after --run_name."
        exit 1
      fi
      ;;
    --lr)
      if [[ $2 =~ ^[0-9.]+$ ]]; then  # Regexp also checks for float values
        LR_ARG="--lr $2"
        shift 2
      else
        echo "Error: Expected a numeric value after --lr."
        exit 1
      fi
      ;;
    --accumulation_steps)
      if [[ $2 =~ ^[0-9]+$ ]]; then
        ACCUMULATION_STEPS_ARG="--accumulation_steps $2"
        shift 2
      else
        echo "Error: Expected a numeric value after --accumulation_steps."
        exit 1
      fi
      ;;
    --forward_pass_sanity)
      FORWARD_PASS_SANITY_ARG="--forward_pass_sanity"
      shift 1
      ;;
    *)
      echo "Error: Unknown argument $1"
      exit 1
      ;;
  esac
done

# Run the training script
python train.py $EPOCHS_ARG $SAVE_STEPS_ARG $RUN_NAME_ARG $FORWARD_PASS_SANITY_ARG $LR_ARG $ACCUMULATION_STEPS_ARG
