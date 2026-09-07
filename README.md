# HackTeam AI

A beginner workshop project: four Gemini agents turn a hackathon idea into a
full blueprint. Research alone uses a tool. Product scopes the MVP, Engineering
proposes an implementation, and Manager reconciles their work into the final plan.

## Setup

Before the two-hour session, install Python 3.11+, create a Gemini API key in
[Google AI Studio](https://aistudio.google.com/app/apikey), and install dependencies:

```bash
git clone https://github.com/thealepo/init-ai-preshell-2.git
cd init-ai-preshell-2
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and copy with
`Copy-Item .env.example .env`. On Debian/Ubuntu, install `python3-venv` if
environment creation reports missing `ensurepip`.

Put your key in `.env`; keep this file private and excluded from Git:

```dotenv
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Run `python main.py`. Enter your idea and optional context, pressing Enter
twice after each answer.

## What students build

- `tools.py`: one function declaration and a keyword search over supplied data.
- `agents.py`: one Gemini request pattern, four roles, and explicit orchestration.
- `main.py`: idea/context input, progress messages, and blueprint display.
- `config.py`: load the API key and model setting.

The 62-entry catalog in `data/resources.json` is supplied, not typed live.
The instructor tests in `test.py` are also outside the live-coding scope.
See [WORKSHOP.md](WORKSHOP.md) for the two-hour build sequence.

## How it works

All agents use `client.interactions.create`. Ordinary agents send a role and
prompt and read `output_text`.

Research adds one visible tool round:

1. Gemini receives the search declaration and chooses keyword queries.
2. Python runs up to three local searches, returning three records per search.
3. The same Gemini API receives the original task and results in a fresh
   prompt without tools and produces the research brief.

No agent other than Research receives a tool declaration. Engineering and
Manager receive Research's brief plus the original records as text evidence;
receiving evidence is not permission to call a tool.

The complete sequence is Research (two requests), Product, Engineering, Manager:
five application requests. There is no application retry loop or agent loop.
The SDK may apply its own transport retries.

Search counts matching words in resource names, tags, and summaries. It has no
category filter, provider filter, weighted ranking, dispatcher, or vector store.
Google preferences are expressed in the user's context and agent instructions;
they are not enforced by a search filter. Records retain provider and cost
information so the agents can explain choices.

The Manager retains the full blueprint: idea, problem, target user, value,
MVP, stack, APIs/tools, architecture, build phases, team split, stretch goals,
risks, and demo strategy.

## Why a catalog instead of Google Search?

The free-tier project encountered grounding quota/billing problems. Google's
[current pricing](https://ai.google.dev/gemini-api/docs/pricing) lists Search
grounding as unavailable on the Gemini 3.x API free tier. The local catalog
requires no search credentials or billing and exposes how a custom tool works.

It contains reviewed summaries and official links, not full pages or live web
results. Free documentation does not imply free hosted services. Generated
plans still require judgment; a citation is not proof of every claim.
See [data/README.md](data/README.md) for source and maintenance details.

## Verify and prepare

```bash
python test.py
```

Offline checks cover catalog retrieval, all four agents, tool isolation,
source handoff, and the CLI. They do not call Gemini or use quota.

Before the workshop, run one real idea using a student-style free-tier project.
Each student should have their own project and key: quotas are per project,
not per key. Daily limits reset at midnight Pacific; other limits may require
waiting briefly. Check [active quotas](https://ai.dev/rate-limit) and
[model availability](https://ai.google.dev/gemini-api/docs/models) before class.

The live-build files intentionally have no custom exception class or
`try`/`except` wrapper: Gemini SDK errors remain visible and teachable. The one
application validation retained is the missing-key check in `config.py`. If a
request fails, check the key, quota, and connection before rerunning; keep a
successful blueprint available for discussion if the provider is unavailable.

API reference: [Google's Interactions guide](https://ai.google.dev/gemini-api/docs/interactions-overview).
