from agents import (
    AgentError,
    create_client,
    run_engineering_agent,
    run_manager_agent,
    run_product_agent,
    run_research_agent,
)
from config import load_config

def print_header() -> None:
    print("=" * 48)
    print("                 HACKTEAM AI")
    print("=" * 48)
    print("Your AI-powered hackathon planning team.\n")

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
        print("Please enter at least one sentence so the agents have something to work with.\n")

def run_app() -> None:
    print_header()

    try:
        config = load_config()
    except ValueError as error:
        print(error)
        return

    idea = ask_for_idea()
    context = ask_multiline(
        "Anything else we should know? Team size, skills, timeline, constraints, or goals are helpful."
    )

    client = create_client(config.api_key)

    try:
        print("\nBuilding your AI team...\n")

        print("[Researcher] Searching for useful tools and context...")
        research_results = run_research_agent(client , config.model , idea , context)

        print("[Product] Designing a focused MVP...")
        product_plan = run_product_agent(client , config.model , idea , context)

        print("[Engineer] Planning the simplest workable architecture...")
        engineering_plan = run_engineering_agent(client , config.model , idea , context)

        print("[Manager] Building your final hackathon blueprint...")
        blueprint = run_manager_agent(
            client=client,
            model=config.model,
            idea=idea,
            context=context,
            research_results=research_results,
            product_plan=product_plan,
            engineering_plan=engineering_plan,
        )
    except AgentError as error:
        print("\n" + str(error))
        return

    print("\n" + "=" * 48)
    print("             YOUR HACKATHON PLAN")
    print("=" * 48)
    print(blueprint)

def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
