import os
import json
import logging
import time
import requests
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("formatter")

INPUT_FILE = "/data/prioritized.txt"
OUTPUT_FILE = "/output/daily_digest.md"
METRICS_FILE = "/output/metrics.json"

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

def format_to_markdown(lines):
    today = datetime.now().strftime('%Y-%m-%d')
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# Your Daily AI Digest\n\n")
        out.write(f"**Date:** {today}\n\n")
        out.write("## Top Insights\n\n")
        for line in lines:
            if '] ' in line:
                score = line.split(']')[0][1:]
                content = line.split('] ', 1)[1]
                out.write(f"- **Priority {score}**: {content}\n")
            else:
                out.write(f"- {line}\n")
    logger.info(f"Digest written to {OUTPUT_FILE}")
    return today

def write_metrics(today, lines, duration_seconds):
    high_priority = [l for l in lines if '] ' in l and int(l.split(']')[0][1:]) >= 2]
    metrics = {
        "date": today,
        "run_timestamp": datetime.utcnow().isoformat() + "Z",
        "duration_seconds": round(duration_seconds, 2),
        "total_items": len(lines),
        "high_priority_items": len(high_priority),
        "output_file": OUTPUT_FILE,
        "status": "success"
    }
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"Metrics written to {METRICS_FILE}: {metrics}")

def send_to_slack(lines, today):
    if not SLACK_WEBHOOK_URL:
        logger.info("No SLACK_WEBHOOK_URL set — skipping Slack notification.")
        return
    high_priority = [
        l.split('] ', 1)[1] for l in lines
        if '] ' in l and int(l.split(']')[0][1:]) >= 2
    ]
    if high_priority:
        items_text = "\n".join(f"• {item}" for item in high_priority)
        message = f":newspaper: *Daily Digest — {today}*\n\n*High Priority Items:*\n{items_text}"
    else:
        message = f":newspaper: *Daily Digest — {today}*\n\nNo high priority items today."
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        resp.raise_for_status()
        logger.info("Slack notification sent successfully.")
    except requests.exceptions.RequestException as e:
        logger.warning(f"Slack notification failed (non-fatal): {e}")

def main():
    start_time = time.time()
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    today = format_to_markdown(lines)
    duration = time.time() - start_time
    write_metrics(today, lines, duration)
    send_to_slack(lines, today)

if __name__ == "__main__":
    main()