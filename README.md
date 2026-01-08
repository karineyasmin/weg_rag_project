# ⚙️ WEG Motor RAG Assistant

> Sistema inteligente de consulta a manuais técnicos usando Retrieval-Augmented Generation (RAG)

Este projeto implementa uma solução completa de RAG desenvolvida para o desafio de Machine Learning Engineering. O sistema permite upload de manuais técnicos em PDF e realiza consultas contextualizadas, fornecendo respostas precisas baseadas exclusivamente nos documentos indexados.

---

## 🎯 Visão Geral

O **WEG Motor RAG Assistant** resolve o problema de consulta rápida e precisa em documentação técnica extensa. Ao invés de buscar manualmente em PDFs, o usuário interage com um assistente que:

- 🔍 **Busca semântica** nos documentos usando embeddings
- 🤖 **Gera respostas contextualizadas** com LLMs de última geração
- 📚 **Cita fontes** (arquivo e página) para auditoria
- 🛡️ **Evita alucinações** rejeitando perguntas fora do contexto

---

## 🚀 Funcionalidades

### Core Features
- ✅ **Upload de Documentos**: Indexação de múltiplos arquivos PDF simultâneos
- ✅ **Processamento Inteligente**: Divisão automática em chunks com sobreposição
- ✅ **Busca Vetorial**: ChromaDB com embeddings multilíngues (HuggingFace)
- ✅ **Respostas Contextualizadas**: LLMs com prompt engineering anti-alucinação
- ✅ **Citação de Fontes**: Referências automáticas (arquivo + página)
- ✅ **Arquitetura Resiliente**: Fallback Gemini → Ollama/Mistral

### Diferenciais
- 🌐 **Suporte Multilíngue**: Responde na mesma língua da pergunta
- 🔄 **Hot-Reload**: Atualização de índice sem reiniciar o sistema
- 📊 **Logs Estruturados**: Rastreamento completo de requisições
- 🐳 **Deploy Simplificado**: Docker Compose com um comando

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| **API** | FastAPI | Alta performance, validação automática (Pydantic) |
| **Orquestração** | LangChain | Abstração para múltiplos LLMs e integrações |
| **Vector Store** | ChromaDB | Simplicidade + persistência local |
| **Embeddings** | HuggingFace MiniLM | Modelo multilíngue eficiente |
| **LLM Principal** | Google Gemini 1.5 Flash | Baixa latência e custo |
| **LLM Fallback** | Mistral (Ollama) | Execução local, sem dependências externas |
| **Frontend** | Streamlit | Prototipagem rápida de chat |
| **Containerização** | Docker Compose | Isolamento e reprodutibilidade |

---

## 📦 Instalação e Execução

### Pré-requisitos
- Docker `>= 20.10`
- Docker Compose `>= 2.0`
- Chave API do Google Gemini ([obtenha aqui](https://aistudio.google.com/app/apikey))

### 1️⃣ Configuração

Clone o repositório e configure as variáveis de ambiente:

```bash
git clone https://github.com/seu-usuario/rag_project.git
cd rag_project
```

Altere o arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_api_aqui
OLLAMA_BASE_URL=http://localhost:11434
PRIMARY_MODEL=gemini-2.5-flash
FALLBACK_MODEL=mistral
```

### 2️⃣ Inicialização

Execute todos os serviços com um único comando:

```bash
docker-compose up --build
```

**O que acontece:**
1. Build das imagens Python customizadas
2. Inicialização do serviço Ollama
3. Download automático do modelo Mistral
4. Subida da API (porta 8000) e Frontend (porta 8501)

### 3️⃣ Acesso

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Ollama API**: http://localhost:11434

---

## 📑 Documentação da API

### `POST /documents`
**Descrição**: Indexa manuais técnicos no sistema.

**Request**:
```bash
curl -X POST "http://localhost:8000/documents" \
  -F "files=@manual_motor.pdf" \
  -F "files=@manual_reducao.pdf"
```

**Response**:
```json
{
  "message": "Documents processed successfully",
  "documents_indexed": 2,
  "total_chunks": 347
}
```

---

### `POST /question`
**Descrição**: Realiza perguntas sobre os documentos indexados.

**Request**:
```bash
curl -X POST "http://localhost:8000/question" \
  -H "Content-Type: application/json" \
  -d '{"question": "Qual a potência nominal do motor W22?"}'
```

**Response**:
```json
{
  "answer": "A potência nominal do motor W22 varia de 0,12 a 355 kW, dependendo do modelo.",
  "references": [
    "Source: manual_w22.pdf (Page 12)",
    "Source: manual_w22.pdf (Page 34)"
  ]
}
```

---

## 💡 Exemplos de Uso

### ✅ Perguntas Técnicas
```
"O que é a Potência absorvida (Pa) de um motor?"
"Qual a fórmula para cálculo de torque mencionada no manual?"
"Quais os requisitos para instalação em ambiente explosivo?"
```

### ✅ Perguntas em Inglês
```
"What is the motor's power consumption?"
"How to verify insulation resistance?"
```

### ❌ Teste Anti-Alucinação
```
Pergunta: "Qual a previsão do tempo para amanhã?"
Resposta: "Information not found."
```
*(O sistema rejeita perguntas fora do contexto dos documentos)*

---

## 🏗️ Arquitetura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Streamlit  │─────▶│   FastAPI   │─────▶│  ChromaDB   │
│  Frontend   │      │     API     │      │ Vector Store│
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  LLM Manager │
                     │              │
                     │ ┌──────────┐ │
                     │ │  Gemini  │ │ (Primary)
                     │ └──────────┘ │
                     │      ▼       │
                     │ ┌──────────┐ │
                     │ │  Mistral │ │ (Fallback)
                     │ └──────────┘ │
                     └──────────────┘
```

### Fluxo de Processamento
1. **Ingestão**: PDF → PyPDF → RecursiveTextSplitter → Embeddings → ChromaDB
2. **Consulta**: Pergunta → Busca Semântica (top-k=3) → Prompt Engineering → LLM → Resposta

---

## 🧪 Testes

### Teste Manual (via cURL)
```bash
# 1. Indexar documento
curl -X POST "http://localhost:8000/documents" \
  -F "files=@data/manual_teste.pdf"

# 2. Fazer pergunta
curl -X POST "http://localhost:8000/question" \
  -H "Content-Type: application/json" \
  -d '{"question": "Qual a tensão nominal?"}'
```

### Logs de Depuração
```bash
docker-compose logs -f api
```

---

## 🔧 Configurações Avançadas

### Ajustar Tamanho dos Chunks
Edite [`app/services/ingestion.py`](app/services/ingestion.py):
```python
self.splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,      # Aumentar para chunks maiores
    chunk_overlap=300     # Aumentar sobreposição
)
```

### Trocar Modelo de Embeddings
Edite [`app/providers/vector_store.py`](app/providers/vector_store.py):
```python
self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  # Modelo alternativo
)
```

### Usar Apenas Ollama (sem Gemini)
No [`.env`](.env):
```env
GEMINI_API_KEY=""  # Deixar vazio força fallback
```

---

## 📂 Estrutura do Projeto

```
rag_project/
├── app/
│   ├── api/              # Rotas FastAPI
│   ├── config/           # Variáveis de ambiente
│   ├── models/           # Schemas Pydantic
│   ├── providers/        # Integrações (LLM, Vector Store)
│   ├── services/         # Lógica de negócio
│   └── utils/            # Logging
├── data/
│   ├── vector_store/     # Banco de vetores persistido
│   └── temp_uploads/     # PDFs temporários
├── app_frontend.py       # Interface Streamlit
├── docker-compose.yml    # Orquestração de containers
├── Dockerfile            # Imagem Python customizada
└── pyproject.toml        # Dependências do projeto
```

---

## 🐛 Troubleshooting

### Erro: `Ollama connection refused`
**Solução**: Aguarde ~30s para o modelo Mistral ser baixado:
```bash
docker-compose logs ollama-pull-model
```

### Erro: `Gemini API key invalid`
**Solução**: Verifique se a chave está correta no [`.env`](.env) e reinicie:
```bash
docker-compose down
docker-compose up --build
```

### Embeddings lentos na primeira execução
**Solução**: O modelo HuggingFace é baixado no primeiro uso (~400MB). Aguarde o download.

---

## 📄 Licença

Este projeto foi desenvolvido como parte de um desafio técnico e está disponível sob a licença MIT.

---

## 👤 Autor

**Karine**  
📧 Email: [karine.y.ribeiro@gmail.com](mailto:karine.y.ribeiro@gmail.com)  
🔗 LinkedIn: [Karine Yasmin Ribeiro](https://linkedin.com/in/karine-yasmin)

---

**Desenvolvido com ❤️ usando Python e LangChain**