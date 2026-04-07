# 🏭 Autonomous Content Factory

A multi-agent AI system that transforms any source document into a full marketing campaign instantly.This system runs fully offline using TinyLlama, eliminating dependency on external APIs and enabling low-cost, privacy-preserving content generation.

## PROBLEM

Content creation is time-consuming and requires multiple steps such as research, fact-checking, drafting, and editing. Many individuals and teams struggle to consistently produce high-quality content due to limited time and resources.

## SOLUTION

The Autonomous Content Factory is a multi-agent AI system that automates the entire content creation pipeline. It uses specialized AI agents to perform research, generate fact sheets, and produce high-quality blog posts. The system also supports regeneration and refinement, improving efficiency and content quality.

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

## ⚙️ Tech Stack
🧑‍💻 Programming Languages
Python
🧰 Frameworks & Libraries
Streamlit - UI + Interaction
Custom Multi-Agent System
🔌 APIs & Tools
Tinyllama (Local LLM)

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
