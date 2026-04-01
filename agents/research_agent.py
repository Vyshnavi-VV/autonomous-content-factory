import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"


def run_research_agent(raw_text: str) -> dict:
    """
    Agent 1: Lead Research & Fact-Check Agent
    Asks each field separately so small models like tinyllama work reliably.
    """

    doc = raw_text[:2000]

    product_name = _ask(f"What is the product or topic name in this text? Reply in 5 words or less, no explanation.\n\n{doc}")
    target_audience = _ask(f"Who is the target audience for this product? Reply in one sentence only, no explanation.\n\n{doc}")
    value_proposition = _ask(f"What is the main benefit or unique selling point of this product? One sentence only, no explanation.\n\n{doc}")
    features_raw = _ask(f"List up to 5 key features of this product. Each feature on a new line starting with a dash (-). No explanation.\n\n{doc}")
    ambiguous_raw = _ask(f"List any vague or unclear statements in this text. Each on a new line starting with a dash (-). If none, just reply: None\n\n{doc}")

    # Parse features into a clean list
    key_features = [
        line.lstrip("- ").strip()
        for line in features_raw.splitlines()
        if line.strip().startswith("-") and len(line.strip()) > 2
    ]
    if not key_features:
        key_features = [features_raw.strip()]

    # Parse ambiguous statements
    if "none" in ambiguous_raw.lower()[:20]:
        ambiguous_statements = []
    else:
        ambiguous_statements = [
            line.lstrip("- ").strip()
            for line in ambiguous_raw.splitlines()
            if line.strip().startswith("-") and len(line.strip()) > 2
        ]

    fact_sheet = {
        "product_name": product_name.strip(),
        "key_features": key_features[:6],
        "target_audience": target_audience.strip(),
        "value_proposition": value_proposition.strip(),
        "ambiguous_statements": ambiguous_statements
    }

    return fact_sheet


def _ask(prompt: str) -> str:
    """Ask a single focused question to the model."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception:
        return "Not identified"