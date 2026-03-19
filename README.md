# 🌾 FarmGenius - Smart Agriculture Assistant

**FarmGenius** is an intelligent agriculture chatbot designed specifically for Indian farmers. It combines Retrieval-Augmented Generation (RAG), live web search, and a local language model to provide practical, actionable farming guidance on crop selection, soil health, pest control, irrigation, and market prices.

> **No internet/API keys required** — runs entirely on your local machine using Ollama.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Setup Instructions](#-setup-instructions)
  - [1. Clone/Setup the Project](#1-clonesetup-the-project)
  - [2. Create Virtual Environment](#2-create-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Install Ollama & LLM Model](#4-install-ollama--llm-model)
  - [5. Add Agriculture Documents](#5-add-agriculture-documents)
  - [6. Run the App](#6-run-the-app)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [API & Components](#-api--components)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)

---

## ✨ Features

### 🎯 Core Capabilities
- **Crop Selection** — Recommends the best crops for your soil type, season, region, and climate
- **Soil Health** — Advice on soil testing, fertility management, pH optimization, and organic matter
- **Weather Guidance** — Interprets weather patterns and provides farming recommendations
- **Pest & Disease Control** — Identifies pests/diseases and suggests organic & chemical remedies
- **Fertilizers & Irrigation** — Fertilizer schedules, dosages, and irrigation techniques (drip, sprinkler, flood)
- **Market Prices** — Guidance on MSP (Minimum Support Price), mandi prices, and when to sell

### 🧠 Intelligence Sources
1. **Knowledge Base** — Indexes your agriculture PDF documents for smart retrieval
2. **Live Web Search** — DuckDuckGo integration for current market prices, weather, pest alerts
3. **Built-in LLM Knowledge** — Llama 3.2:3b model with comprehensive agriculture expertise

### 💬 Conversation Features
- **Context Awareness** — Maintains conversation history for personalized responses
- **Multi-turn Dialog** — Asks clarifying questions and builds on previous answers
- **Smart Formatting** — Responses use bullet points, numbered steps, and clear structure

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| **Frontend UI** | Streamlit 1.32+ |
| **LLM** | Ollama (llama3.2:3b) |
| **RAG Pipeline** | LangChain Core 0.2+ |
| **Vector DB** | ChromaDB 0.5+ |
| **Text Processing** | Sentence Transformers (embeddings), PyPDF (document loading) |
| **Web Search** | DuckDuckGo (DDGS) |
| **Language** | Python 3.8+ |

---

## 📦 Prerequisites

Before starting, ensure you have:

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Ollama installed and running**
   - Download from: https://ollama.ai
   - Verify it's running: `ollama serve`

3. **Git (optional, for cloning)**

---

## 🚀 Setup Instructions

### 1. Clone/Setup the Project

Navigate to your desired folder and download/create the FarmGenius directory:

```bash
# Option A: Clone from Git (if available)
git clone https://github.com/yourusername/FarmGenius.git
cd FarmGenius

# Option B: Create folder manually and copy files
mkdir FarmGenius
cd FarmGenius
# Copy all project files into this directory
```

### 2. Create Virtual Environment

Create an isolated Python environment to avoid package conflicts:

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — web UI framework
- `langchain-core`, `langchain-community`, `langchain-text-splitters` — RAG pipeline
- `langchain-chroma` — vector database wrapper  
- `langchain-ollama` — Ollama LLM integration
- `chromadb` — vector storage engine
- `sentence-transformers` — embedding model
- `pymupdf` — PDF document loading
- `ddgs` — DuckDuckGo search API

### 4. Install Ollama & LLM Model

**Step 1:** Download and install Ollama from https://ollama.ai

**Step 2:** In a separate terminal (with Ollama running), pull the required model:

```bash
ollama pull llama3.2:3b
```

This downloads ~7GB of the llama3.2:3b model. First run takes a few minutes.

**Verify it works:**
```bash
ollama ls
# Should show: llama3.2:3b     5.5 GB
```

### 5. Add Agriculture Documents

The app works best with your own agriculture PDFs. Here's how to add them:

**Create the data folder and add PDFs:**

```bash
# Create data directory
mkdir data

# Copy your PDFs into it
# Examples of supported filenames:
# - farm-Training-Manual-English.pdf
# - fundamental-of-agriculture.pdf
# - crop-guide.pdf
# - soil-health.pdf
# - pest-disease-control.pdf
# - market-prices.pdf
```

**Supported PDFs** (currently in the data folder):
- `farm-Training-Manual-English.pdf` — Farm training & practices (439 chunks)
- `food-security-challange.pdf` — Food security topics (142 chunks)
- `fundamental-of-agriculture.pdf` — Agriculture fundamentals (594 chunks)
- `inovative-agriculture.pdf` — Innovative farming techniques (1,301 chunks)

**Total:** 2,476 document chunks ready for retrieval.

> **Note:** On first run, the app creates a `chroma_db/` folder and indexes all PDFs. Subsequent runs load the cached index instantly. If you add new PDFs, delete `chroma_db/` to force re-indexing.

### 6. Run the App

**Start Ollama** (if not already running):
```bash
ollama serve
```

**In a new terminal, activate venv and run:**

**Windows (PowerShell):**
```powershell
# Activate virtual environment
venv\Scripts\activate

# Run the Streamlit app
streamlit run main.py
```

**macOS/Linux:**
```bash
# Activate virtual environment
source venv/bin/activate

# Run the Streamlit app
streamlit run main.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.106:8501
```

Open http://localhost:8501 in your browser. That's it! 🎉

---

## 📁 Project Structure

```
FarmGenius/
├── main.py                          # Streamlit UI & session management
├── rag_chain.py                     # FarmGenius AI engine (RAG + LLM + web search)
├── vector.py                        # ChromaDB vector store wrapper
├── load_documents.py                # PDF loader & text chunker
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── data/                            # Agriculture PDFs (you add these)
│   ├── farm-Training-Manual-English.pdf
│   ├── food-security-challange.pdf
│   ├── fundamental-of-agriculture.pdf
│   └── inovative-agriculture.pdf
├── chroma_db/                       # Auto-generated vector database
│   └── chroma.sqlite3
└── venv/                            # Python virtual environment
```

### File Descriptions

- **`main.py`** — Streamlit web interface, session management, sidebar with settings
- **`rag_chain.py`** — Core FarmGenius class: RAG retrieval + LLM + web search + prompt engineering
- **`vector.py`** — VectorStore class: loads PDFs, creates embeddings, manages ChromaDB
- **`load_documents.py`** — Document loader: reads PDFs from `data/`, chunks them intelligently
- **`requirements.txt`** — Python package dependencies with pinned versions
- **`data/`** — Directory for agriculture PDF documents (auto-loads on startup)
- **`chroma_db/`** — Persistent vector database (auto-created on first run)

---

## 💬 Usage Guide

### Starting a Conversation

1. **Open the app** at http://localhost:8501
2. **See the topic badges** at the top (Crop Selection, Soil Health, Weather, etc.)
3. **Type your farming question** in the chat box at the bottom
4. **FarmGenius responds** with advice drawn from:
   - Agriculture PDFs (knowledge base)
   - Live web search results
   - Built-in LLM knowledge

### Example Questions

```
"What are the best crops to grow in black soil during monsoon?"

"How do I treat powdery mildew on my wheat?"

"What's the current MSP for rice in my area?"

"How often should I irrigate tomatoes in summer?"

"Which fertilizer should I use for poor soil?"
```

### Sidebar Features

- **🔍 Web Search Status** — Shows if DuckDuckGo is active
- **🗑️ Clear Chat History** — Starts a fresh conversation
- **ℹ️ Info Box** — Displays data sources (PDFs, web, LLM)

---

## 🔧 API & Components

### FarmGenius Class (`rag_chain.py`)

```python
from rag_chain import FarmGenius
from vector import VectorStore

# Initialize with vector store
vector_store = VectorStore()
vector_store.load_vector_store()
farm_genius = FarmGenius(vector_store)

# Get response with conversation history
response = farm_genius.get_response(
    query="Best crops for sandy soil?",
    chat_history=[...]
)
```

### VectorStore Class (`vector.py`)

```python
from vector import VectorStore
from load_documents import get_document_chunks

# Create vector store from documents
chunks = get_document_chunks()
vs = VectorStore()
vs.create_vector_store(chunks)

# Load existing vector store
vs.load_vector_store()

# Search for relevant documents
docs = vs.similarity_search("crop selection", k=5)
```

### Document Loading (`load_documents.py`)

```python
from load_documents import get_document_chunks

# Load all PDFs from data/ folder
chunks = get_document_chunks()
print(f"Loaded {len(chunks)} chunks")
```

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:** Activate virtual environment and reinstall dependencies
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Issue: DuckDuckGo search says "disabled"
**Solution:** Install or reinstall the DDGS package
```bash
pip install --upgrade ddgs
```

### Issue: "Could not connect to Ollama"
**Solution:** Ensure Ollama is running in a separate terminal
```bash
ollama serve
```

### Issue: Very slow on first run
**Solution:** First run indexes all PDFs (~2,476 chunks). This takes 2-5 minutes. Subsequent runs use the cached `chroma_db/` and are instant.

### Issue: Chroma database is corrupted
**Solution:** Delete the cache and rebuild
```bash
rm -r chroma_db/  # macOS/Linux
rmdir /s chroma_db  # Windows
# Then restart the app
streamlit run main.py
```

### Issue: "No agriculture documents were successfully loaded"
**Solution:** Ensure PDF files are in the `data/` folder
```bash
# Check what files are there
ls data/  # macOS/Linux
dir data  # Windows

# If empty, copy PDFs there
# Examples: farm-Training-Manual-English.pdf, fundamental-of-agriculture.pdf, etc.
```

---

## 🚀 Future Enhancements

Potential features for future versions:

- [ ] **Multi-language support** — Hindi, Marathi, Tamil, Telugu, Kannada, etc.
- [ ] **Voice input/output** — Speak questions in local languages
- [ ] **Real-time weather data** — Integration with weather APIs
- [ ] **Mandi price API** — Live market data from government databases
- [ ] **Soil testing upload** — Analyze soil reports and get recommendations
- [ ] **Farmer profiles** — Save region, soil type, crops for personalized advice
- [ ] **Image-based pest identification** — Upload crop leaf photos for diagnosis
- [ ] **Subsidy & scheme info** — Government welfare program guidance
- [ ] **Export recommendations** — Generate PDF reports of conversations
- [ ] **Mobile app** — Native Android/iOS versions

---

## 📝 License

This project is open source. Feel free to modify and redistribute.

---

## 👥 Contributing

To improve FarmGenius:

1. Add more agriculture PDFs to the `data/` folder
2. Test with local farmers and collect feedback
3. Report bugs or suggest features via GitHub issues
4. Submit pull requests for improvements

---

## 📞 Support

For issues or questions:

1. Check the **Troubleshooting** section above
2. Ensure all packages are up to date: `pip install -r requirements.txt --upgrade`
3. Verify Ollama is running: `ollama serve`
4. Check that agriculture PDFs are in the `data/` folder

---

## 🌾 About FarmGenius

FarmGenius was created to bridge the knowledge gap for Indian farmers by providing instant access to expert agriculture advice. By combining:

- **Curated agriculture documents** (from training manuals and research)
- **Live web search** (for current prices and alerts)
- **State-of-the-art LLM** (for personalized guidance)

...we empower farmers to make data-driven decisions on crop selection, soil health, pest management, irrigation, and market timing.

**Made with ❤️ for Indian Agriculture**

---

**Last Updated:** March 2026  
**Version:** 1.0  
**Status:** Ready for deployment
