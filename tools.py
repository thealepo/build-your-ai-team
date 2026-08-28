from google.genai import types

def google_search_tool() -> types.Tool:
    """Give Gemini access to Google Search grounding.

    Only the Research Agent uses this tool. Keeping tools attached to the
    agents that need them makes the architecture easier to understand.
    """
    return types.Tool(google_search=types.GoogleSearch())
