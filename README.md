# 🏭 Autonomous Content Factory

A multi-agent AI system that transforms any source document into a full marketing campaign instantly.

## 🤖 Agents
- **Agent 1 — Research Agent:** Extracts a structured Fact-Sheet from the source document
- **Agent 2 — Copywriter Agent:** Generates Blog Post, Social Media Thread, and Email Teaser
- **Agent 3 — Editor Agent:** Reviews all content for hallucinations and tone quality

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install and start Ollama
```bash
# Install from https://ollama.com
ollama pull llama2
ollama serve
```

### 3. Run the app
```bash
streamlit run app.py
```

## 🛠️ Tech Stack
- Python
- Streamlit
- Ollama (Llama2)
- PyPDF2
- BeautifulSoup4

## 📁 Project Structure
```
autonomous-content-factory/
├── agents/
│   ├── research_agent.py      # Agent 1: Fact extraction
│   ├── copywriter_agent.py    # Agent 2: Content generation
│   └── editor_agent.py        # Agent 3: Quality control
├── utils/
│   ├── document_parser.py     # PDF/TXT/URL parser
│   └── exporter.py            # ZIP export
├── app.py                     # Main Streamlit app
└── requirements.txt
```