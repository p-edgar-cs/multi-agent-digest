#!/bin/bash
# Run this ONCE to schedule the pipeline every day at 7am.
# Usage: chmod +x schedule_cron.sh && ./schedule_cron.sh

PROJECT_DIR="/Users/edgarpalaquibay/Desktop/AI_Projects/multi-agent-digest"
RUN_SCRIPT="$PROJECT_DIR/run_pipeline.sh"

chmod +x "$RUN_SCRIPT"

CRON_JOB="0 7 * * * $RUN_SCRIPT"
( crontab -l 2>/dev/null | grep -v "$RUN_SCRIPT"; echo "$CRON_JOB" ) | crontab -

echo "✅ Cron job scheduled! Pipeline will run every day at 7:00 AM."
echo "To verify: crontab -l"
echo "To view logs: cat $PROJECT_DIR/pipeline.log"
echo "To remove: crontab -e (delete the line)"