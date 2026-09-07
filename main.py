from agents import (
    create_client,
    run_engineering_agent,
    run_manager_agent,
    run_product_agent,
    run_research_agent,
)
from config import load_config


def print_header() -> None:
    print("=" * 48)
    print("Your Multi-Agent AI Hackathon Planning Team.")
    print("=" * 48)


def ask_multiline(prompt: str) -> str:
    print(prompt)
    print("Type your answer. Press Enter twice when done.\n")

    lines = []
    while True:
        line = input("> ")
        if line == "":
            break
        lines.append(line)

    return "\n".join(lines).strip()


def ask_for_idea() -> str:
    while True:
        idea = ask_multiline("What's your hackathon idea?")
        if idea:
            return idea
        print("Please enter an idea so the agents have something to work with.\n")


def build_blueprint() -> str:
    """Collect input and run the four-agent workflow."""
    api_key, model = load_config()
    client = create_client(api_key)

    idea = ask_for_idea()
    context = ask_multiline(
        "Anything else we should know? Team size, skills, timeline, "
        "constraints, or goals are helpful."
    )

    print("\nBuilding your AI team...\n")

    print("[Researcher] Searching the hackathon resource catalog...")
    research = run_research_agent(
        client, model, idea, context, reporter=print
    )

    print("[Product] Designing a focused MVP...")
    product = run_product_agent(client, model, idea, context)

    print("[Engineer] Planning the simplest workable architecture...")
    engineering = run_engineering_agent(
        client, model, idea, context, research_results=research
    )

    print("[Manager] Building your final hackathon blueprint...")
    return run_manager_agent(
        client=client,
        model=model,
        idea=idea,
        context=context,
        research_results=research,
        product_plan=product,
        engineering_plan=engineering,
    )


def run_app() -> None:
    print_header()

    blueprint = build_blueprint()

    print("\n" + "=" * 48)
    print("             YOUR HACKATHON PLAN")
    print("=" * 48)
    print(blueprint)


if __name__ == "__main__":
    run_app()
