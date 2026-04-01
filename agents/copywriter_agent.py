import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"


def run_copywriter_agent(fact_sheet: dict, regenerate: str = None, note: str = None) -> dict:
    """
    Agent 2: Creative Copywriter Agent
    Generates Blog Post, Social Media Thread, and Email Teaser from Fact-Sheet.
    If regenerate is set ('blog', 'social', 'email'), regenerates only that piece with correction note.
    """

    fs_str = json.dumps(fact_sheet, indent=2)

    if regenerate:
        return _regenerate_single(fact_sheet, regenerate, note)

    blog = _generate_blog(fs_str)
    social = _generate_social(fs_str)
    email = _generate_email(fs_str)

    return {
        "blog": blog,
        "social": social,
        "email": email
    }


def _generate_blog(fs_str: str) -> str:
    prompt = f"""You are a professional content writer. Using the fact-sheet below, write a 500-word blog post.

Tone: Professional, trustworthy, and informative.
Requirements:
- Start with an engaging headline
- Include an introduction, 2-3 body sections, and a conclusion
- Highlight the value proposition clearly
- Do NOT invent features not in the fact-sheet

FACT-SHEET:
{fs_str}

Write the blog post now:"""

    return _call_ollama(prompt)


def _generate_social(fs_str: str) -> str:
    prompt = f"""You are a social media expert. Using the fact-sheet below, write a 5-post Twitter/X thread.

Tone: Engaging, punchy, and conversational.
Requirements:
- Post 1: Hook that grabs attention
- Posts 2-4: One key feature or benefit each
- Post 5: Call to action
- Each post max 280 characters
- Separate posts with a blank line
- Number each post (1/, 2/, etc.)
- Do NOT invent features not in the fact-sheet

FACT-SHEET:
{fs_str}

Write the social thread now:"""

    return _call_ollama(prompt)


def _generate_email(fs_str: str) -> str:
    prompt = f"""You are an email marketing specialist. Using the fact-sheet below, write a 1-paragraph email teaser.

Tone: Formal, concise, and compelling.
Requirements:
- Subject line included at the top
- Single paragraph body (3-4 sentences max)
- End with a clear call to action
- Do NOT invent features not in the fact-sheet

FACT-SHEET:
{fs_str}

Write the email teaser now:"""

    return _call_ollama(prompt)


def _regenerate_single(fact_sheet: dict, content_type: str, note: str) -> dict:
    fs_str = json.dumps(fact_sheet, indent=2)

    correction = f"\n\nEDITOR'S CORRECTION NOTE: {note}\nPlease fix these issues in your rewrite." if note else ""

    if content_type == "blog":
        return {"blog": _call_ollama(_generate_blog.__doc__ + f"\n\nFACT-SHEET:\n{fs_str}{correction}\n\nRewrite the blog post now:")}
    elif content_type == "social":
        return {"social": _call_ollama(f"Rewrite the social media thread based on this fact-sheet:\n{fs_str}{correction}")}
    elif content_type == "email":
        return {"email": _call_ollama(f"Rewrite the email teaser based on this fact-sheet:\n{fs_str}{correction}")}

    return {}


def _call_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        raise RuntimeError(f"Ollama API error: {str(e)}\nMake sure Ollama is running: ollama serve")