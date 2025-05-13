#!/bin/bash

TOKEN=""
INPUT_DIR="/home/kat/Desktop/FPTAI/tmp" # Replace this to the folder contains all vlm generated results
OUTPUT_DIR="/home/kat/Desktop/FPTAI/IQBench/experiments/results" # Replace this to the folder that will contain all llmjudge generated results
MODEL="gpt-4o-mini" # Replace this to the model you want to use for llmjudge

mkdir -p "$OUTPUT_DIR"

# Loop over all JSON files in the input directory
for INPUT_FILE in "$INPUT_DIR"/*.json; do
  BASENAME=$(basename "$INPUT_FILE")                   # e.g., results_gemini-2.0-flash.json
  OUTPUT_FILE="$OUTPUT_DIR/${BASENAME%.json}_evaluate.json"  # e.g., results_gemini-2.0-flash_evaluate.json
  
  echo "Evaluating $MODEL on $BASENAME -> $OUTPUT_FILE"
  python -m experiments.llmjudge \
    --input_file "$INPUT_FILE" \
    --output_file "$OUTPUT_FILE" \
    --model_name "$MODEL" \
    --api_token "$TOKEN" \
    --num_samples 100
done
