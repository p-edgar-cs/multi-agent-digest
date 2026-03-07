#!/bin/bash
PROJECT_DIR="/Users/edgarpalaquibay/Desktop/AI_Projects/multi-agent-digest"
LOG_FILE="$PROJECT_DIR/pipeline.log"

echo "$(date): Starting pipeline run" >> "$LOG_FILE"
cd "$PROJECT_DIR" && docker compose up --build >> "$LOG_FILE" 2>&1
echo "$(date): Pipeline complete" >> "$LOG_FILE"