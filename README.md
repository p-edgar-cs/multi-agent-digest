# Multi-Agent Digest

An Automated Data Processing Pipeline built with Python and Docker. Four specialized AI agents run in sequence to transform raw text inputs into a prioritized daily digest, delivered to Slack.

## How It Works

```
data/input/notes.txt  (your raw text)
        ↓
  [Ingestor]
  Reads all files in data/input/ and combines them
  into one file → data/ingested.txt
        ↓
  [Summarizer]  ← uses Groq API (llama-3.1-8b-instant)
  Sends ingested.txt to the LLM
  Returns clean bullet points → data/summary.txt
        ↓
  [Prioritizer]
  Scores each bullet by urgency keywords
  Sorts highest score first → data/prioritized.txt
        ↓
  [Formatter]
  Writes Markdown report → output/daily_digest.md
  Writes run stats → output/metrics.json
  Posts high-priority items → Slack #daily-digest
```

## Agents

| Agent | Job | LLM Required |
|-------|-----|-------------|
| ingestor | Reads and combines input files | No |
| summarizer | Summarizes text into bullet points | Yes (Groq) |
| prioritizer | Scores items by urgency keywords | No |
| formatter | Writes digest, metrics, and Slack notification | No |

Each agent lives under `agents/<agent-name>`.

---

## Setup

### Prerequisites
- Docker Desktop
- Groq API key (free at console.groq.com)
- Slack webhook URL (optional, for notifications)

### Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=gsk_your-key-here
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
```

### Add Your Input

Drop any `.txt` files into `data/input/`:

```bash
cp your-notes.txt data/input/notes.txt
```

---

## Running the Pipeline

```bash
docker compose up --build
```

All four agents run in sequence automatically. When complete:

```bash
cat output/daily_digest.md   # your digest
cat output/metrics.json      # run stats
```

---

## Output Example

```markdown
# Your Daily AI Digest

**Date:** 2026-03-07

## Top Insights

- **Priority 2**: All team leads must submit Q1 reports by Friday deadline
- **Priority 1**: RFC document must be created by next Wednesday
- **Priority 0**: Team plans to migrate to microservices in Q2
```

---

## Scheduling Daily Runs (macOS)

Run the pipeline automatically every morning at 7am:

```bash
chmod +x schedule_cron.sh
./schedule_cron.sh
```

View logs after a scheduled run:

```bash
cat pipeline.log
```

---

## Running Tests

```bash
# create a venv (only once)
python3 -m venv .venv
source .venv/bin/activate

pip install pytest
python -m pytest tests/ -v
```

---

## Project Structure

```
multi-agent-digest/
├── agents/
│   ├── ingestor/
│   │   ├── app.py
│   │   └── Dockerfile
│   ├── summarizer/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt    ← groq>=1.0.0
│   ├── prioritizer/
│   │   ├── app.py
│   │   └── Dockerfile
│   └── formatter/
│       ├── app.py              ← Slack + metrics
│       ├── Dockerfile
│       └── requirements.txt    ← requests>=2.31
├── data/
│   └── input/                  ← drop your .txt files here
├── output/                     ← daily_digest.md + metrics.json
├── tests/
├── .env                        ← API keys (never commit this)
├── .gitignore
├── docker-compose.yml
├── run_pipeline.sh
├── schedule_cron.sh
└── README.md
```

---

## Tech Stack

- **Python 3.10**
- **Docker + Docker Compose**
- **Groq API** — llama-3.1-8b-instant (free tier)
- **Slack Incoming Webhooks** — for digest delivery
