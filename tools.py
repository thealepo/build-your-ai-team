import json
import re
from pathlib import Path


RESOURCE_CATALOG_PATH = Path(__file__).parent / 'data' / 'resources.json'

RESOURCE_SEARCH_TOOL = {
    'type': 'function',
    'name': 'search_hackathon_resources',
    'description': (
        'Search the supplied hackathon catalog for services and official coding '
        'docs. Use a few separate keywords, such as "firebase authentication".'
    ),
    'parameters': {
        'type': 'object',
        'properties': {'query': {'type': 'string'}},
        'required': ['query'],
    },
}

def search_hackathon_resources(query: str) -> list[dict]:
    with RESOURCE_CATALOG_PATH.open(encoding='utf-8') as catalog_file:
        catalog = json.load(catalog_file)

    query_words = set(re.findall(r"[a-z0-9]+", query.lower()))
    matches = []
    for resource in catalog:
        searchable_text = ' '.join(
            [resource['name'], *resource['tags'], resource['summary']]
        )
        resource_words = set(re.findall(r'[a-z0-9]+', searchable_text.lower()))
        score = len(query_words & resource_words)
        if score:
            matches.append((score, resource))

    matches.sort(key=lambda match: match[0], reverse=True)
    return [resource for _, resource in matches[:3]]
