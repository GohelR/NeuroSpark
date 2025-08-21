# NeuroSpark — AI Campus Operations Agent

TL;DR: NeuroSpark answers FAQs with citations and auto-files/auto-routes complaints with SLA tracking.

See the `demo_script.txt` for a short 3-min video flow.

## Quickstart
1. Setup virtualenv and install requirements
2. Set `OPENAI_API_KEY`
3. `streamlit run app.py`

## Features
- RAG-based FAQ answers
- Ticket creation (auto-route metadata)
- Simple Staff dashboard to view tickets

Tech: Streamlit, FastAPI (optional), OpenAI, Sentence-Transformers, Chroma
