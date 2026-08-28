from google import genai
from google.genai import types

from tools import google_search_tool


class AgentError(Exception):
    """A beginner-friendly error raised when an agent cannot complete its job."""

def create_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)

def call_gemini(
    client: genai.Client,
    model: str,
    system_instruction: str,
    user_prompt: str,
    tools: list[types.Tool] | None = None,
) -> str:
    """Send one prompt to Gemini and return plain text.

    This helper keeps Gemini-specific code in one place so the agent functions
    below can stay focused on their roles and responsibilities.
    """
    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools,
            temperature=0.7,
        )
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=config,
        )
    except Exception as error:
        raise AgentError(
            "HackTeam could not reach Gemini right now.\n\n"
            "Possible causes:\n"
            "- API rate limit reached\n"
            "- Invalid Gemini API key\n"
            "- Temporary network issue\n\n"
            f"Original error: {error}"
        ) from error

    text = getattr(response , "text" , None)
    if not text or not text.strip():
        raise AgentError(
            "Gemini returned an empty response. Try again with a little more detail in your idea."
        )

    return text.strip()


def build_project_prompt(idea: str , context: str) -> str:
    extra_context = context.strip() or "No extra context was provided."
    return f"""
Hackathon idea:
{idea.strip()}

Extra context:
{extra_context}
""".strip()

def run_research_agent(client: genai.Client , model: str , idea: str , context: str = "") -> str:
    system_instruction = """
You are the Research Agent for HackTeam AI.

Your job is to investigate the ecosystem around a hackathon project idea.
Focus on practical information a student team can use quickly:
- relevant APIs, services, libraries, datasets, and docs
- similar products or examples worth knowing about
- shortcuts that make the project easier to build in a hackathon
- risks caused by unavailable APIs, pricing, auth, or data access

Use Google Search grounding when useful. Prefer actionable findings over exhaustive research.
Avoid academic depth unless it directly helps the team build.

Output a concise research brief with bullets and links or named resources when available.
""".strip()

    prompt = build_project_prompt(idea , context)
    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
        tools=[google_search_tool()],
    )

def run_product_agent(client: genai.Client , model: str , idea: str , context: str = "") -> str:
    system_instruction = """
You are the Product Agent for HackTeam AI.

Your job is to turn the idea into a focused hackathon product.
Focus on:
- target users
- the real problem
- the core value proposition
- a small MVP that can be finished
- what to avoid so the team does not scope creep
- stretch goals only after the MVP works
- a demo story that judges can understand quickly

Be practical, opinionated, and ruthless about scope.
Avoid suggesting too many features, platforms, or complex product directions.

Output a concise product brief.
""".strip()

    prompt = build_project_prompt(idea , context)
    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )

def run_engineering_agent(client: genai.Client , model: str , idea: str , context: str = "") -> str:
    system_instruction = """
You are the Engineering Agent for HackTeam AI.

Your job is to convert the project idea into a realistic technical plan.
Focus on:
- the simplest workable architecture
- frontend, backend, database, AI, and external services if needed
- important implementation steps
- technical risks and simpler alternatives
- choices that a student team could finish during a hackathon

Prefer boring, reliable tools over impressive complexity.
Avoid microservices, Kubernetes, event buses, custom infrastructure, and unnecessary AI complexity.

Output a concise engineering brief.
""".strip()

    prompt = build_project_prompt(idea , context)
    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )

def run_manager_agent(
    client: genai.Client,
    model: str,
    idea: str,
    context: str,
    research_results: str,
    product_plan: str,
    engineering_plan: str,
) -> str:
    system_instruction = """
You are the Manager Agent for HackTeam AI.

Your job is to synthesize the Research, Product, and Engineering agents into one coherent hackathon blueprint.
Do not simply paste their outputs together. Reconcile conflicts and make final decisions.
Keep the plan useful, readable, and realistic for a student hackathon team.

Use this structure:
# Project Name
## The Idea
## Problem
## Target User
## Core Value Proposition
## MVP
## Suggested Tech Stack
## Useful APIs / Tools
## Architecture
## Build Plan
### Phase 1
### Phase 2
### Phase 3
## Team Split
## Stretch Goals
## Risks / Things to Watch
## Demo Strategy

Be specific, but do not be unnecessarily verbose.
""".strip()

    prompt = f"""
Original hackathon idea:
{idea.strip()}

Extra context:
{context.strip() or "No extra context was provided."}

Research Agent output:
{research_results}

Product Agent output:
{product_plan}

Engineering Agent output:
{engineering_plan}

Create the final hackathon blueprint.
""".strip()

    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )

def build_hackathon_blueprint(client: genai.Client , model: str , idea: str , context: str = "") -> str:
    """Run the simple multi-agent workflow from specialists to manager."""
    research_results = run_research_agent(client , model , idea , context)
    product_plan = run_product_agent(client , model , idea , context)
    engineering_plan = run_engineering_agent(client , model , idea , context)

    return run_manager_agent(
        client=client,
        model=model,
        idea=idea,
        context=context,
        research_results=research_results,
        product_plan=product_plan,
        engineering_plan=engineering_plan,
    )
