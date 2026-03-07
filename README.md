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

---

## Potential Applications

The multi-agent pipeline pattern used here is not limited to daily digests. The same architecture — ingest, transform, prioritize, deliver — applies across a wide range of real-world problems. Swapping out the input data and agent logic is all it takes to adapt it.

### Data Engineering
The pipeline mirrors a classic ETL (Extract, Transform, Load) workflow. Instead of personal notes, point it at raw datasets and each agent handles one step of the data processing chain.

| Agent | ETL Role | Example |
|-------|----------|---------|
| Ingestor | Extract | Pull provider records from multiple state databases |
| Summarizer | Transform | Normalize, clean, and classify records using LLM |
| Prioritizer | Business Logic | Score records by compliance rules or urgency |
| Formatter | Load | Write results to a database, CSV, or dashboard |

Real-world example: a healthcare company could use this to process insurance network provider data across all 50 states, flag adequacy gaps, and deliver a daily compliance report.

### Full Stack Integration
The pipeline can sit behind a Django REST API, turning it into a backend service that a React frontend can trigger and display results from.

```
React Frontend
    ↓ user uploads a document or triggers a run
Django API
    ↓ kicks off the pipeline
Multi-Agent Pipeline
    ↓ processes data and writes results
Django API
    ↓ serves results back as JSON
React Frontend
    displays prioritized insights to the user
```

### Business Intelligence
Replace the notes file with sales data, customer feedback, or support tickets. The summarizer extracts key themes, the prioritizer surfaces urgent issues, and the formatter delivers a daily business briefing to a Slack channel.

### Content Moderation
Feed user-generated content through the pipeline. The summarizer classifies content, the prioritizer flags high-risk items, and the formatter routes flagged content to a moderation queue.

### Security & DevOps
Point the ingestor at server logs or security alerts. The summarizer groups related events, the prioritizer scores by severity, and the formatter delivers a daily incident report with only the critical items highlighted.

### Research & Competitive Intelligence
Feed the pipeline news articles, academic papers, or competitor announcements. The summarizer extracts key findings, the prioritizer ranks by relevance to your domain, and the formatter delivers a structured briefing every morning.