# HackTeam AI

HackTeam AI is an AI-powered hackathon planning team for the INIT AI Explore workshop, "Teamwork Makes the Dream Work: Building Your First Multi-Agent AI".

Give it a hackathon idea and optional context. Four simple Python agents turn that idea into a practical blueprint:

1. Research Agent with Google Search grounding
2. Product Agent
3. Engineering Agent
4. Manager Agent

The project intentionally avoids agent frameworks so beginners can see the orchestration directly in the code.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and replace `your_api_key_here` with your Gemini API key.

You can get a key from Google AI Studio:

https://aistudio.google.com/app/apikey

## Run

```bash
python main.py
```

Example idea:

```text
An app that helps FIU students find study partners based on their classes and availability.
```

Example context:

```text
Team of 3. We know Python and React. We have 36 hours.
```

## Project Structure

```text
main.py              CLI and visible orchestration flow
agents.py            Four agent functions plus shared Gemini helper
tools.py             Google Search tool configuration
config.py            Environment loading and model configuration
requirements.txt     Minimal dependencies
.env.example         Safe environment template
```

## Teaching Goal

This repository shows that an agent can be understood as:

```text
LLM + role + instructions + context + optional tools
```

The multi-agent workflow is intentionally simple:

```text
Idea
  +-> Research Agent
  +-> Product Agent
  +-> Engineering Agent
          |
          v
     Manager Agent
          |
          v
 Hackathon Blueprint
```

## Notes

- The Gemini model is centralized in `config.py`.
- The API key should live only in `.env`.
- The Research Agent is the only agent with Google Search grounding.
- No agent framework is used.
