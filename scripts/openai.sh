#!/bin/bash

TOKEN=""
# Replace this path to the questions_processed.json
INPUT_FILE="/home/kat/Desktop/FPTAI/IQBench/data/questions_processed.json"

declare -A MODELS
MODELS=(
  ["gpt-4o-mini"]="results_gpt4o.json"
  ["o4-mini"]="results_o4mini.json"
)

for MODEL in "${!MODELS[@]}"; do
  OUTPUT_FILE="/home/kat/Desktop/FPTAI/IQBench/experiments/results/${MODELS[$MODEL]}"
  echo "Evaluating $MODEL -> $OUTPUT_FILE"
  python -m experiments.evaluate \
    --input_file "$INPUT_FILE" \
    --output_file "$OUTPUT_FILE" \
    --model_name "$MODEL" \
    --api_token "$TOKEN" \
    --num_samples 5
done