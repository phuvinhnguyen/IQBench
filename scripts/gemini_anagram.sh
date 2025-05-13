#!/bin/bash

TOKEN=""
# Replace this path to the questions_processed.json
INPUT_FILE="/home/kat/Desktop/FPTAI/IQBench/data/questions_processed.json"

declare -A MODELS
MODELS=(
  ["gemini/gemini-2.0-flash"]="results_gemini-2.0-flash_anagram.json"
  ["gemini/gemini-2.5-flash-preview-04-17"]="results_gemini-2.5-flash-preview-04-17_anagram.json"
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