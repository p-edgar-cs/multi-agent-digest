# Multi-Agent Digest# Multi-Agent Digest















```docker-compose up --build```bashTo run locally with Docker Compose:Each agent lives under `agents/<agent-name>` and exposes a simple HTTP health endpoint.- formatter- prioritizer- summarizer- ingestorThis repository contains a small multi-agent digest prototype with four agents:
This repository contains a small multi-agent digest prototype with four agents:
- ingestor
- summarizer
- prioritizer
- formatter

Each agent lives under `agents/<agent-name>` and exposes a simple HTTP health endpoint.

To run locally with Docker Compose:

```bash
docker-compose up --build
```
