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
│   ├── sample_datasets/           # put Titanic, House Prices CSVs here
│   └── sample_papers/             # put arxiv PDFs here
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md

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

## 📌 API Documentation

Once the backend is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔖 Versioning

| Version | Description |
|---|---|
| v1.0.0 | Initial release — all 12 modules complete |

---

## 👤 Author

**Charanpreet Singh**
B.Tech CSE — CGC University Mohali
