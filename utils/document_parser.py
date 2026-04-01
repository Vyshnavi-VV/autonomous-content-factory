import requests
from bs4 import BeautifulSoup
import PyPDF2
import io


def parse_document(file=None, url=None, text=None):
    """
    Parse input from file, URL, or raw text.
    Returns a plain text string.
    """
    if file is not None:
        return _parse_file(file)
    elif url is not None:
        return _parse_url(url)
    elif text is not None:
        return text.strip()
    else:
        raise ValueError("Provide a file, url, or text.")


def _parse_file(file):
    filename = file.name.lower()

    if filename.endswith(".txt"):
        return file.read().decode("utf-8").strip()

    elif filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        if not text.strip():
            raise ValueError("Could not extract text from PDF. It may be scanned/image-based.")
        return text.strip()

    else:
        raise ValueError(f"Unsupported file type: {filename}. Please upload PDF or TXT.")


def _parse_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts, styles, nav, footer
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch URL: {str(e)}")