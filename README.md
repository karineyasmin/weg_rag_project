# ⚙️ WEG Motor RAG Assistant

> Intelligent system for technical manual queries using Retrieval-Augmented Generation (RAG)

This project implements a complete RAG solution developed for a Machine Learning Engineering challenge. The system allows technical manuals in PDF format to be uploaded and performs contextualized queries, providing accurate answers based exclusively on the indexed documents.

---

## 🎯 Overview

The **WEG Motor RAG Assistant** solves the problem of fast and accurate information retrieval in extensive technical documentation. Instead of manually searching through PDFs, users interact with an assistant that:

- 🔍 **Performs semantic search** across documents using embeddings.
- 🤖 **Generates contextualized answers** using state-of-the-art LLMs.
- 📚 **Cites sources** (file and page number) for auditability.
- 🛡️ **Prevents hallucinations** by rejecting out-of-scope questions.

---

## 🚀 Features

### Core Features
- ✅ **Document Upload**: Index multiple PDF files simultaneously.
- ✅ **Smart Processing**: Automatic text splitting into chunks with overlap.
- ✅ **Vector Search**: ChromaDB powered by multilingual embeddings (HuggingFace).
- ✅ **Contextual Answers**: LLMs with anti-hallucination prompt engineering.
- ✅ **Source Citation**: Automatic references (file name + page).
- ✅ **Resilient Architecture**: Primary Gemini → Ollama/Mistral fallback system.

### Highlights
- 🌐 **Multilingual Support**: Responds in the same language as the query.
- 🔄 **Hot-Reload**: Update the vector index without restarting the system.
- 📊 **Structured Logs**: Full request and execution tracing.
- 🐳 **Simplified Deployment**: Docker Compose setup with a single command.

---

## 🛠️ Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **API** | FastAPI | High performance and automatic validation (Pydantic). |
| **Orchestration** | LangChain | Abstraction for multiple LLMs and integrations. |
| **Vector Store** | ChromaDB | Simplicity combined with local persistence. |
| **Embeddings** | HuggingFace MiniLM | Efficient and lightweight multilingual model. |
| **Primary LLM** | Google Gemini 2.5 Flash | Low latency and cost-effectiveness. |
| **Fallback LLM** | Mistral (Ollama) | Local execution, eliminating external dependencies. |
| **Frontend** | Streamlit | Rapid chat interface prototyping. |
| **Containerization** | Docker Compose | Environment isolation and reproducibility. |

---

## 📦 Installation & Execution

### Prerequisites
- Docker `>= 20.10`
- Docker Compose `>= 2.0`
- Google Gemini API Key ([get it here](https://aistudio.google.com/app/apikey))

### 1️⃣ Configuration

Clone the repository and set up the environment variables:

```bash
git clone https://github.com/karineyasmin/weg_rag_project
cd weg_rag_project
```

Edit the `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
PRIMARY_MODEL=gemini-2.5-flash
FALLBACK_MODEL=mistral
OLLAMA_URL=http://ollama:11434
```

### 2️⃣ Initialization

Run all services with a single command:

```bash
docker-compose up --build
```

What happens:
- Builds custom Python images.
- Initializes the Ollama service.
- Automatically downloads the Mistral model.
- Starts the API (port 8000) and Frontend (port 8501).

### 3️⃣ Access

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Ollama API**: http://localhost:11434

---

## 📑 API Documentation

### POST /documents

Description: Indexes technical manuals into the system.

**Request:**

```bash
curl -X POST "http://localhost:8000/documents" \
  -F "files=@motor_manual.pdf" \
  -F "files=@gearbox_manual.pdf"
```

**Response:**

```json
{
  "message": "Documents processed successfully",
  "documents_indexed": 2,
  "total_chunks": 347
}
```

### POST /question

Description: Ask questions regarding the indexed documents.

**Request:**

```bash
curl -X POST "http://localhost:8000/question" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the nominal power of the W22 motor?"}'
```

**Response:**

```json
{
  "answer": "The nominal power of the W22 motor ranges from 0.12 to 355 kW, depending on the model.",
  "references": [
    "Source: manual_w22.pdf (Page 12)",
    "Source: manual_w22.pdf (Page 34)"
  ]
}
```

---

## 💡 Usage Examples

### ✅ Technical Questions
- "What is the absorbed power (Pa) of a motor?"
- "What is the formula for calculating torque mentioned in the manual?"
- "What are the requirements for installation in explosive environments?"

### ✅ English Questions
- "What is the motor's power consumption?"
- "How to verify insulation resistance?"

### ❌ Anti-Hallucination Test
- **Question**: "What is the weather forecast for tomorrow?"
- **Answer**: "Information not found." (The system rejects questions outside the context of the uploaded documents)

---

## 🏗️ Architecture

### Processing Flow
- **Ingestion**: PDF → PyPDF → RecursiveTextSplitter → Embeddings → ChromaDB.
- **Query**: Question → Semantic Search (top-k=3) → Prompt Engineering → LLM → Answer.

---

## 🧪 Testing

### Manual Test (via cURL)

1. Index a document
    ```bash
    curl -X POST "http://localhost:8000/documents" \
      -F "files=@data/test_manual.pdf"
    ```

2. Ask a question
    ```bash
    curl -X POST "http://localhost:8000/question" \
      -H "Content-Type: application/json" \
      -d '{"question": "What is the nominal voltage?"}'
    ```

### Debug Logs

```bash
docker-compose logs -f api
```

---

## 🔧 Advanced Configuration

### Adjust Chunk Size

Edit `app/services/ingestion.py`:

```python
self.splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,      # Increase for larger chunks
    chunk_overlap=300     # Increase overlap
)
```

### Change Embeddings Model

Edit `app/providers/vector_store.py`:

```python
self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  # Alternative model
)
```

### Use Only Ollama (No Gemini)

In the `.env` file:

```env
GEMINI_API_KEY=""  # Leaving this empty forces the fallback to Mistral
```

---

## 📂 Project Structure

```
rag_project/
├── app/
│   ├── api/              # FastAPI routes
│   ├── config/           # Environment variables
│   ├── models/           # Pydantic schemas
│   ├── providers/        # Integrations (LLM, Vector Store)
│   ├── services/         # Business logic
│   └── utils/            # Logging
├── data/
│   ├── vector_store/     # Persisted vector database
│   └── temp_uploads/     # Temporary PDF uploads
├── app_frontend.py       # Streamlit interface
├── docker-compose.yml    # Container orchestration
├── Dockerfile            # Custom Python image
└── pyproject.toml        # Project dependencies
```

---

## 🐛 Troubleshooting

### Error: Ollama connection refused

**Solution**: Wait approximately 30 seconds for the Mistral model to finish downloading:

```bash
docker-compose logs ollama-pull-model
```

### Error: Gemini API key invalid

**Solution**: Double-check the key in the `.env` file and restart the containers:

```bash
docker-compose down
docker-compose up --build
```

### Slow embeddings on first run

**Solution**: The HuggingFace model is downloaded during first use (~400MB). Please wait for the download to complete.

---

## 📄 License

This project was developed as part of a technical challenge and is available under the MIT License.

---

## 👤 Author

**Karine**  
📧 Email: karine.y.ribeiro@gmail.com  
🔗 LinkedIn: Karine Yasmin Ribeiro

Built with ❤️ using Python and LangChain
