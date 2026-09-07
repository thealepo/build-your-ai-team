# Multi-Agent AI Workshop -- Hackathon Blueprint System

A hands-on workshop project regarding agents and multi-agent systems: four Gemini agents turn a hackathon idea into a
full blueprint. Research alone uses a tool. Product scopes the MVP, Engineering
proposes an implementation, and Manager reconciles their work into the final plan.

## Setup

Install Python 3.11+, create a Gemini API key in
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

## Future Directions

There are many directions and features you can add onto this template to
create a much more robust project. A few of the features you can add
onto this are:

- Implementing a `write_file` tool, in which the Manager agent writes the
hackathon blueprint into a `.md` or `.txt` file (among others), allowing you
to save the blueprint permanently on your machine.

- Implementing an official Google Search tool. This may require a subscription
due to Google's [current pricing](https://ai.google.dev/gemini-api/docs/pricing)
listing Search grounding as unavailable on the Gemini 3.x API free tier.

- Switching from the Gemini API to another API, such as the OpenAI API or
Anthropic's API.

## Gemini API Reference

API reference: [Google's Interactions guide](https://ai.google.dev/gemini-api/docs/interactions-overview).
