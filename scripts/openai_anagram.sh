#!/bin/bash

TOKEN=""
# Replace this path to the questions_processed.json
INPUT_FILE="/home/kat/Desktop/FPTAI/IQBench/data/questions_processed.json"

declare -A MODELS
MODELS=(
  ["gpt-4o"]="results_gpt4o_anagram.json"
  # ["o4-mini"]="results_o4mini_anagram.json"
)

for MODEL in "${!MODELS[@]}"; do
  OUTPUT_FILE="/home/kat/Desktop/FPTAI/IQBench/experiments/results/${MODELS[$MODEL]}"
  echo "Evaluating $MODEL -> $OUTPUT_FILE"
  python -m experiments.evaluate_anagram \
    --input_file "$INPUT_FILE" \
    --output_file "$OUTPUT_FILE" \
    --model_name "$MODEL" \
    --api_token "$TOKEN" \
    --num_samples 100
done