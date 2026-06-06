# text_parser.py — parses raw text into structured research paper fields
import re
from typing import Optional


#  ML/AI algorithms to look for
KNOWN_ALGORITHMS = [
    "logistic regression", "random forest", "xgboost", "svm", "support vector",
    "neural network", "deep learning", "cnn", "lstm", "transformer", "bert",
    "gpt", "decision tree", "naive bayes", "knn", "k-nearest", "gradient boosting",
    "adaboost", "linear regression", "ridge", "lasso", "kmeans", "k-means",
    "dbscan", "pca", "autoencoder", "resnet", "vgg", "attention mechanism",
    "random forest regressor", "lightgbm", "catboost"
]

# Common datasets to look for
KNOWN_DATASETS = [
    "imagenet", "cifar", "mnist", "coco", "pascal voc", "glue", "squad",
    "imdb", "amazon", "yelp", "twitter", "wikipedia", "pubmed", "arxiv",
    "ucl", "kaggle", "iris", "titanic", "boston housing", "movielens"
]

# Common evaluation metrics
KNOWN_METRICS = [
    "accuracy", "precision", "recall", "f1", "f1-score", "auc", "roc",
    "mse", "rmse", "mae", "r2", "bleu", "rouge", "perplexity", "loss",
    "map", "ndcg", "mrr", "specificity", "sensitivity", "iou"
]


def extract_title(text: str, pdf_metadata_title: str = "") -> str:
    """Extract paper title — use PDF metadata first, then first line."""
    if pdf_metadata_title and len(pdf_metadata_title) > 5:
        return pdf_metadata_title.strip()

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    # Title is usually in the first 5 lines and longer than 20 chars
    for line in lines[:5]:
        if len(line) > 20 and not line.lower().startswith(("abstract", "introduction")):
            return line
    return lines[0] if lines else "Unknown Title"


def extract_authors(text: str, pdf_metadata_author: str = "") -> list:
    """Extract author names."""
    if pdf_metadata_author and len(pdf_metadata_author) > 2:
        authors = [a.strip() for a in pdf_metadata_author.split(",")]
        return [a for a in authors if a]

    authors = []
    lines = text.split("\n")[:20]  # Authors usually in first 20 lines

    for line in lines:
        # Look for lines with multiple capitalized words (author pattern)
        if re.match(r'^([A-Z][a-z]+ [A-Z][a-z]+)(,\s*[A-Z][a-z]+ [A-Z][a-z]+)*', line):
            parts = re.split(r',|\band\b', line)
            for part in parts:
                part = part.strip()
                if 3 < len(part) < 50:
                    authors.append(part)
    return authors[:10]  # max 10 authors


def extract_abstract(text: str) -> str:
    """Extract abstract section."""
    # Look for Abstract header
    pattern = r'(?i)abstract[:\s\-]*\n?(.*?)(?=\n\s*(?:introduction|keywords|1\.|index terms))'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        abstract = match.group(1).strip()
        return abstract[:2000]  # cap at 2000 chars

    # Fallback: first substantial paragraph
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 150]
    return paragraphs[0][:2000] if paragraphs else ""


def extract_keywords(text: str) -> list:
    """Extract keywords from paper."""
    pattern = r'(?i)(?:keywords|index terms)[:\s\-]*([^\n]+(?:\n(?!\n)[^\n]+)*)'
    match = re.search(pattern, text)
    if match:
        kw_text = match.group(1)
        keywords = re.split(r'[,;·•]', kw_text)
        return [kw.strip() for kw in keywords if 2 < len(kw.strip()) < 50][:15]
    return []


def extract_section(text: str, section_names: list) -> str:
    """Generic section extractor given a list of possible section headers."""
    for name in section_names:
        pattern = rf'(?i)(?:^|\n)\s*(?:\d+\.?\s+)?{name}[:\s\-]*\n(.*?)(?=\n\s*(?:\d+\.?\s+)?(?:conclusion|result|experiment|method|reference|discussion|related|future|limitation))'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()[:3000]
    return ""


def extract_algorithms(text: str) -> list:
    """Find known algorithms mentioned in the paper."""
    text_lower = text.lower()
    found = []
    for algo in KNOWN_ALGORITHMS:
        if algo in text_lower:
            # Capitalize nicely
            found.append(algo.title())
    return list(set(found))


def extract_datasets(text: str) -> list:
    """Find known datasets mentioned in the paper."""
    text_lower = text.lower()
    found = []
    for dataset in KNOWN_DATASETS:
        if dataset in text_lower:
            found.append(dataset.title())
    return list(set(found))


def extract_metrics(text: str) -> list:
    """Find evaluation metrics mentioned in the paper."""
    text_lower = text.lower()
    found = []
    for metric in KNOWN_METRICS:
        if metric in text_lower:
            found.append(metric.upper())
    return list(set(found))


def parse_paper(raw_text: str, metadata: dict) -> dict:
    """
    Master function — takes raw text and metadata,
    returns fully structured paper dictionary.
    """
    title = extract_title(raw_text, metadata.get("title", ""))
    authors = extract_authors(raw_text, metadata.get("author", ""))
    abstract = extract_abstract(raw_text)
    keywords = extract_keywords(raw_text)

    problem_statement = extract_section(raw_text, ["problem statement", "problem formulation", "motivation"])
    methodology = extract_section(raw_text, ["methodology", "method", "approach", "proposed method", "our approach"])
    results = extract_section(raw_text, ["results", "experiments", "evaluation", "performance"])
    limitations = extract_section(raw_text, ["limitation", "limitations", "weakness"])
    future_work = extract_section(raw_text, ["future work", "future research", "conclusion and future"])

    algorithms = extract_algorithms(raw_text)
    datasets = extract_datasets(raw_text)
    metrics = extract_metrics(raw_text)

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "keywords": keywords,
        "problem_statement": problem_statement,
        "methodology": methodology,
        "datasets_used": datasets,
        "algorithms_used": algorithms,
        "evaluation_metrics": metrics,
        "results": results,
        "limitations": limitations,
        "future_work": future_work,
    }