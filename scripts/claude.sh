#!/bin/bash

TOKEN=""
# Replace this path to the questions_processed.json
INPUT_FILE="/home/kat/Desktop/FPTAI/IQBench/data/questions_processed.json"

declare -A MODELS
MODELS=(
  ["claude-3-5-sonnet-20240620"]="results_claude-3-5-sonnet-20240620.json"
  ["claude-3-7-sonnet-20250219"]="results_claude-3-7-sonnet-20250219.json"
)

for MODEL in "${!MODELS[@]}"; do
  OUTPUT_FILE="/home/kat/Desktop/FPTAI/IQBench/experiments/results/${MODELS[$MODEL]}"
  echo "Evaluating $MODEL -> $OUTPUT_FILE"
  python -m experiments.evaluate \
    --input_file "$INPUT_FILE" \
    --output_file "$OUTPUT_FILE" \
    --model_name "$MODEL" \
    --api_token "$TOKEN" \
    --num_samples 100
done
