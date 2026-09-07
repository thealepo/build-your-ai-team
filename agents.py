import json
from google import genai
from tools import RESOURCE_SEARCH_TOOL, search_hackathon_resources


def create_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def request_gemini(client, model, instruction, prompt, tools=None):
    generation_config = {}
    if tools:
        generation_config['tool_choice'] = 'any'
    return client.interactions.create(
        model=model,
        input=prompt,
        system_instruction=instruction,
        tools=tools or [],
        generation_config=generation_config,
        store=False,
    )

def call_gemini(client, model, system_instruction, user_prompt):
    response = request_gemini(client, model, system_instruction, user_prompt)
    return response.output_text

def build_project_prompt(idea: str, context: str) -> str:
    extra_context = context.strip() or 'No extra context was provided.'
    return f"""
Hackathon idea:
{idea.strip()}

Extra context:
{extra_context}
""".strip()

def run_research_agent(client, model, idea, context="", reporter=None):
    instruction = """
You are the Research Agent in this multi-agent hackathon planning team.
Find practical services and coding docs for this hackathon idea.
Request up to three focused keyword searches in your first response.
The supplied catalog is a snapshot, not live web search.
Recommend only relevant matches; say when evidence is missing.
Respect the user's Google-only and no-billing constraints when selecting results.
Cite exact catalog documentation URLs and preserve cost caveats.
Free documentation does not mean free hosting or API usage.
Write a brief explaining which resources fit, their limitations, and a
recommended combination. Label assumptions instead of inventing facts.
""".strip()
    prompt = build_project_prompt(idea, context)

    # gemini selects search arguments. Only Research receives a tool.
    response = request_gemini(
        client, model, instruction, prompt, tools=[RESOURCE_SEARCH_TOOL]
    )
    calls = [step for step in response.steps if step.type == 'function_call']

    # python runs the requested searches locally
    resources = []
    for call in calls[:3]:
        query = call.arguments['query']
        matches = search_hackathon_resources(query)
        resources.extend(matches)

        if reporter:
            reporter(f"    [Researcher -> Tool] Search: {query}")
            names = ", ".join(item['name'] for item in matches) or 'No matches'
            reporter(f"    [Tool -> Researcher] {names}")

    # return evidence in a fresh prompt without tools, so the search stops
    evidence = "\n\nCatalog evidence (original records):\n" + json.dumps(resources)
    brief = call_gemini(
        client,
        model,
        instruction,
        prompt + evidence + "\nWrite the research brief using these results.",
    )
    # keep original sources available to Engineering and Manager as well
    return brief + evidence

def run_product_agent(
    client: genai.Client, model: str, idea: str, context: str = ''
) -> str:
    system_instruction = """
You are the Product Agent in this multi-agent hackathon planning team.

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

Label proposed user needs as hypotheses; do not invent market research or
facts about a university or existing products.
Output a concise product brief.
""".strip()

    prompt = build_project_prompt(idea, context)
    return call_gemini(
        client=client,
        model=model,
        system_instruction=system_instruction,
        user_prompt=prompt,
    )

def run_engineering_agent(
    client: genai.Client,
    model: str,
    idea: str,
    context: str = '',
    research_results: str = '',
) -> str:
    system_instruction = """
You are the Engineering Agent in this multi-agent hackathon planning team.

Your job is to convert the project idea into a realistic technical plan.
Focus on:
- the simplest workable architecture
- frontend, backend, database, AI, and external services if needed
- important implementation steps
- technical risks and simpler alternatives
- choices that a student team could finish during a hackathon

Prefer boring, reliable tools over impressive complexity.
Avoid microservices, Kubernetes, event buses, custom infrastructure, and unnecessary AI complexity.

Treat constraints in the user's extra context as requirements. If the user
requests Google-only or no-billing services, do not silently recommend an
outside provider or a billing-required service. Explain any tradeoff instead.

Use the original catalog records when supplied. Cite exact documentation
links for technical recommendations and label unsupported details as needing
verification. Free documentation does not imply free hosting or API usage.
An email suffix check alone is not authentication or proof of ownership.
For demos without login, use local mock data or an emulator, not open cloud
read/write permissions. Distinguish frontend hosting from database storage.

Output a concise engineering brief.
""".strip()

    prompt = build_project_prompt(idea, context)
    if research_results:
        prompt += "\n\nResearch findings and catalog evidence:\n" + research_results
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
You are the Manager Agent in this multi-agent hackathon planning team.

Your job is to synthesize the Research, Product, and Engineering agents into one coherent hackathon blueprint.
Do not simply paste their outputs together. Reconcile conflicts and make final decisions.
Keep the plan useful, readable, and realistic for a student hackathon team.

Treat the original constraints as requirements. For external APIs and
services, only recommend resources supported by the Research Agent output or
explicitly named by the user. Do not introduce a second AI provider. If a
Google-only, no-billing constraint makes part of the plan impossible, state
the tradeoff and choose a local demo rather than silently breaking it.

Prefer original catalog records over a specialist's unsupported assertions.
Include exact documentation links and resource IDs for recommended resources.
Clearly label design choices, user-need hypotheses, and facts needing
verification. Do not claim to have browsed the linked pages. A catalog entry
is a short reviewed description, not a copy of the full documentation.

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


def build_hackathon_blueprint(
    client: genai.Client, model: str, idea: str, context: str = ''
) -> str:
    research_results = run_research_agent(client , model , idea , context)
    product_plan = run_product_agent(client , model , idea , context)
    engineering_plan = run_engineering_agent(
        client , model , idea , context , research_results=research_results
    )

    return run_manager_agent(
        client=client,
        model=model,
        idea=idea,
        context=context,
        research_results=research_results,
        product_plan=product_plan,
        engineering_plan=engineering_plan,
    )
