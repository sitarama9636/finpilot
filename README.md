# 🧠 FinPilot – AI-Powered Financial Assistant (PoC)

FinPilot is an intelligent financial research assistant that uses LLMs (via LangChain and Ollama) to help users:

- ✅ Answer questions from uploaded financial reports
- ✅ Compare two companies using retrieved documents
- ✅ Perform financial ratio analysis
- ✅ Summarize financial text/PDFs
- ✅ Read results aloud via voice agent (TTS)
- ✅ Use multiple tools in a **multi-agent reasoning workflow**

---

## 🧩 Architecture Overview

# 🧠 FinPilot – AI-Powered Financial Assistant (PoC)


                                 ┌────────────────────┐
                                 │    AgentExecutor    │
                                 └─────────┬──────────┘
                                           │
            ┌──────────────────────────────┼───────────────────────────────┐
            │                              │                               │
   🛠️ compare_companies()        🧮 answer_financial_question()       📊 ratio_analysis()
            │                              │                               │
   🔍 Vector DB (Chroma)           🔍 Vector DB (Chroma)             🔍 Vector DB (Chroma)
            │                              │                               │
            ▼                              ▼                               ▼
       NVIDIA 10-Qs etc              Embedded PDF docs                Financials context

            ┌──────────────────────────────┼───────────────────────────────┐
            │                              │                               │
   📑 answer_pdf_question()      🗣️ speak_text()                  🧠 summarize_text_block()
         (via RAG on PDFs)       (Text-to-speech agent)              (LLM summarizer)



---

## ✅ Completed Functionality

| Feature                          | Status  |
|----------------------------------|---------|
| Financial Q&A via RAG            | ✅ Done |
| Compare two companies            | ✅ Done |
| Summarize financial reports      | ✅ Done |
| Extract insights from PDFs       | ✅ Done |
| Perform ratio analysis           | ✅ Done |
| Voice synthesis (TTS)            | ✅ Done |
| Agent orchestration              | ✅ Done |
| Multi-step reasoning             | ✅ Done |
| Real-time CLI interface          | ✅ Done |

---

## 🚧 What’s Left (for POC Completion)

| Task / Feature                                        | Status      |
|-------------------------------------------------------|-------------|
| Handle `OutputParserException` in agent (via `handle_parsing_errors=True`) | ✅ Done |
| Replace deprecated imports (LangChain ≥ 0.2)          | ⚠️ In Progress |
| Add robust fallback/retry logic                       | 🕓 Next |
| Add UI upload / file API                              | 🕓 Next |
| Add memory for context tracking                       | 🕓 Future |
| Web Interface (streamlit/Gradio)                      | 🔜 Optional |
| Real-time stock data integration                      | 🔜 Optional |

---

## 🏗️ Directory Structure

FinPilot/
├── app/
│ ├── agent_setup.py
│ ├── main_tools.py
│ └── tools/
│ ├── comparecompanies_tool.py
│ ├── financialqa_tool.py
│ ├── ratioanalysis_tool.py
│ ├── qa_tool.py
│ ├── voice_tool.py
│ └── pdfretriever.py
├── chroma_vectordb/
├── models/
├── .env.sample
├── requirements.txt
└── README.md


---

## 💻 Installation & Usage

### 🔧 Setup

```bash
git clone https://github.com/yourname/finpilot.git
cd finpilot
python -m venv .venv
.venv\Scripts\activate      # On Windows
# OR
source .venv/bin/activate   # On macOS/Linux

pip install -r requirements.txt


🚀 Run the Agent

python -m app.agent_setup
You’ll see:
🔁 Waiting for your input...
Ask your financial assistant: