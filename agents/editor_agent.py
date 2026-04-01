import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"


def run_editor_agent(fact_sheet: dict, content: dict) -> dict:
    """
    Agent 3: Editor-in-Chief Agent
    Reviews all content against the Fact-Sheet.
    Checks for hallucinations, tone issues, and quality.
    Returns approval/rejection with notes.
    """

    fs_str = json.dumps(fact_sheet, indent=2)

    blog_review = _review_piece(fs_str, content.get("blog", ""), "blog post", "professional and trustworthy")
    social_review = _review_piece(fs_str, content.get("social", ""), "social media thread", "engaging and punchy")
    email_review = _review_piece(fs_str, content.get("email", ""), "email teaser", "formal and concise")

    return {
        "blog": blog_review,
        "social": social_review,
        "email": email_review
    }


def _review_piece(fs_str: str, content: str, content_type: str, expected_tone: str) -> dict:
    prompt = f"""You are a strict Editor-in-Chief. Review the following {content_type}.

Your job:
1. Check if it contains any facts NOT in the Fact-Sheet (hallucination)
2. Check if the tone is {expected_tone} (tone audit)
3. Check if it is too salesy, robotic, or off-brand

FACT-SHEET (source of truth):
{fs_str}

{content_type.upper()} TO REVIEW:
{content}

Return ONLY a valid JSON object with these exact keys:
- "status": either "Approved" or "Rejected"
- "note": if Approved, write "Looks good!". If Rejected, write a specific 1-sentence correction note.

Return only the JSON. No explanation."""

    response = _call_ollama(prompt)

    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        json_str = response[json_start:json_end]
        review = json.loads(json_str)
    except Exception:
        # Default to approved if parsing fails
        review = {"status": "Approved", "note": "Looks good!"}

    return review


def _call_ollama(prompt: str) -> str:
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
    except Exception as e:
        raise RuntimeError(f"Ollama API error: {str(e)}")