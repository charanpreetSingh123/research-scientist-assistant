# 🔬 AI Research Scientist Assistant

> Automated Literature Analysis & ML Experimentation Platform

An end-to-end AI-powered platform that automates research paper analysis, knowledge extraction, and machine learning experimentation. Built for researchers, data scientists, and ML engineers who want to move faster from raw literature to actionable insights.

---

## 📋 Features at a Glance

| Module | What it does |
|---|---|
| 📄 Paper Ingestion | Upload research PDFs, auto-extract title, authors, algorithms, datasets, metrics |
| 🔍 Semantic Search | Search across all papers using vector embeddings (ChromaDB) |
| 🕸️ Knowledge Graph | Visual graph of relationships between papers, algorithms, datasets, authors |
| 🔎 Gap Detection | Automatically identifies underexplored algorithms and missing research directions |
| 🧪 ML Engine | Auto-profiles datasets, trains 6+ models, selects best automatically |
| 🧠 Deep Learning | PyTorch feed-forward network for tabular data |
| 💡 Explainability | SHAP-based feature importance and model interpretation |
| 📝 Report Generator | Auto-generates structured PDF research reports |
| 📊 Analytics Dashboard | Interactive Plotly charts for trends, model comparison, experiment history |

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI, Python 3.13 |
| ML | Scikit-learn, XGBoost, PyTorch |
| NLP & Embeddings | Sentence-Transformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| Relational Database | PostgreSQL |
| Explainability | SHAP |
| Knowledge Graph | NetworkX, Plotly |
| PDF Processing | PyMuPDF, pdfplumber, ReportLab |
| Infra | Docker, Docker Compose |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker Desktop running
- Git

### 1. Clone the repo
```bash
git clone https://github.com/charanpreetSingh123/research-scientist-assistant.git
cd research-scientist-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment
```bash
cp .env.example .env
```

### 4. Start databases
```bash
docker-compose up -d
```

### 5. Initialize database tables
```bash
python3 scripts/init_db.py
```

### 6. Start the backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### 7. Start the frontend (new terminal)
```bash
streamlit run frontend/app.py
```

Visit **http://localhost:8501**

---

## 📂 Project Structure

```
research-scientist-assistant/
├── backend/
│   ├── api/
│   │   └── routes/
│   │       ├── papers.py          # paper upload and gap analysis
│   │       ├── knowledge.py       # semantic search and graph
│   │       ├── experiments.py     # ML experiment runner
│   │       ├── reports.py         # PDF report generation
│   │       └── analytics.py       # dashboard data
│   ├── services/
│   │   ├── research_parser/
│   │   │   ├── pdf_extractor.py   # raw text from PDF
│   │   │   ├── text_parser.py     # structure extraction
│   │   │   └── paper_service.py   # orchestration + DB
│   │   ├── ml_engine/
│   │   │   ├── data_profiler.py   # dataset analysis
│   │   │   ├── preprocessor.py    # cleaning + encoding
│   │   │   ├── trainer.py         # multi-model training
│   │   │   ├── explainer.py       # SHAP analysis
│   │   │   ├── deep_learning.py   # PyTorch network
│   │   │   └── experiment_service.py
│   │   ├── knowledge_graph/
│   │   │   └── graph_service.py   # NetworkX graph builder
│   │   ├── vector_store/
│   │   │   └── embeddings.py      # ChromaDB operations
│   │   └── report_generator/
│   │       └── pdf_report.py      # ReportLab PDF builder
│   ├── models/
│   │   ├── database.py            # SQLAlchemy engine
│   │   └── schemas.py             # table definitions
│   ├── config.py
│   └── main.py
├── frontend/
│   ├── pages/
│   │   ├── upload_papers.py
│   │   ├── knowledge_base.py
│   │   ├── ml_experiment.py
│   │   ├── analytics.py
│   │   └── reports.py
│   └── app.py
├── tests/
│   ├── test_parser.py
│   ├── test_profiler.py
│   ├── test_preprocessor.py
│   └── test_trainer.py
├── scripts/
│   └── init_db.py
├── data/
│   ├── sample_datasets/
│   └── sample_papers/
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧪 Sample Datasets

Download and place in `data/sample_datasets/`:

| Dataset | Link | Task |
|---|---|---|
| Titanic | [kaggle.com/c/titanic](https://www.kaggle.com/c/titanic) | Classification |
| House Prices | [kaggle.com/c/house-prices](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) | Regression |
| Mall Customers | [kaggle.com/datasets/vjchoudhary7](https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python) | Clustering |

---

## ✅ Running Tests

```bash
python3 tests/test_parser.py
python3 tests/test_profiler.py
python3 tests/test_preprocessor.py
python3 tests/test_trainer.py
```

All 4 test suites should pass with no errors.

---
## 📸 Screenshots

### Home Page
![Home](assets/Main_dashboard.png)

### Upload Papers
![Upload Papers](assets/Upload_papers.png)

### ML Experiment Results
![ML Experiment](assets/experiment_result.png)

### Experiment History
![Experiment History](assets/ML_experiment_history.png)

### Analytics Dashboard
![Analytics](assets/Analytics_dashboard.png)

### Reports
![Reports](assets/Reports.png)


## 📌 API Documentation

Once the backend is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔖 Versioning

| Version | Description |
|---|---|
| v1.0.0 | Initial release  |

---

## 👤 Author

Charanpreet Singh
B.Tech CSE — CGC University Mohali