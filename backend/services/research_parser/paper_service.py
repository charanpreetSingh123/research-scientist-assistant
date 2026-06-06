import os
from pathlib import Path
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.schemas import ResearchPaper
from backend.services.research_parser.pdf_extractor import extract_text, get_pdf_metadata
from backend.services.research_parser.text_parser import parse_paper


def save_uploaded_pdf(file_content: bytes, filename: str) -> str:
    upload_dir = Path(settings.UPLOAD_DIR) / "papers"
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / filename
    with open(file_path, "wb") as f:
        f.write(file_content)
    return str(file_path)


def process_paper(file_path: str, db: Session, owner_id: str = None) -> ResearchPaper:
    print(f"processing: {file_path}")

    raw_text = extract_text(file_path)
    if not raw_text:
        raise ValueError("could not extract text from PDF")

    metadata = get_pdf_metadata(file_path)
    parsed = parse_paper(raw_text, metadata)

    paper = ResearchPaper(
        title=parsed["title"],
        authors=parsed["authors"],
        abstract=parsed["abstract"],
        keywords=parsed["keywords"],
        problem_statement=parsed["problem_statement"],
        methodology=parsed["methodology"],
        datasets_used=parsed["datasets_used"],
        algorithms_used=parsed["algorithms_used"],
        evaluation_metrics=parsed["evaluation_metrics"],
        results=parsed["results"],
        limitations=parsed["limitations"],
        future_work=parsed["future_work"],
        file_path=file_path,
        owner_id=None,  # no auth for now
    )

    db.add(paper)
    db.commit()
    db.refresh(paper)

    # add to vector store for semantic search
    try:
        from backend.services.vector_store.embeddings import add_paper_to_vectorstore
        add_paper_to_vectorstore(
            paper.id,
            paper.title,
            paper.abstract or "",
            paper.keywords or []
        )
    except Exception as e:
        print(f"vector store indexing failed (non-critical): {e}")

    print(f"saved: {paper.title} — {paper.id}")
    return paper


def get_all_papers(db: Session) -> list:
    return db.query(ResearchPaper).all()


def get_paper_by_id(paper_id: str, db: Session) -> ResearchPaper:
    return db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()


def delete_paper(paper_id: str, db: Session) -> bool:
    paper = get_paper_by_id(paper_id, db)
    if not paper:
        return False
    if paper.file_path and Path(paper.file_path).exists():
        os.remove(paper.file_path)
    db.delete(paper)
    db.commit()
    return True


def get_research_gap_analysis(db: Session) -> dict:
    papers = get_all_papers(db)

    if not papers:
        return {"message": "No papers uploaded yet"}

    algo_count = {}
    dataset_count = {}
    metric_count = {}

    for paper in papers:
        for algo in (paper.algorithms_used or []):
            algo_count[algo] = algo_count.get(algo, 0) + 1
        for dataset in (paper.datasets_used or []):
            dataset_count[dataset] = dataset_count.get(dataset, 0) + 1
        for metric in (paper.evaluation_metrics or []):
            metric_count[metric] = metric_count.get(metric, 0) + 1

    sorted_algos = sorted(algo_count.items(), key=lambda x: x[1], reverse=True)
    sorted_datasets = sorted(dataset_count.items(), key=lambda x: x[1], reverse=True)
    sorted_metrics = sorted(metric_count.items(), key=lambda x: x[1], reverse=True)

    total_papers = len(papers)
    rarely_used_algos = [a for a, c in sorted_algos if c == 1]
    dominant_algos = [a for a, c in sorted_algos if c >= total_papers * 0.5]

    gap_insights = []

    if dominant_algos:
        gap_insights.append(
            f"Most papers focus on: {', '.join(dominant_algos[:3])}. "
            f"Limited work exists exploring alternative approaches."
        )
    if rarely_used_algos:
        gap_insights.append(
            f"Underexplored algorithms: {', '.join(rarely_used_algos[:3])}. "
            f"These appear in only 1 paper."
        )
    if sorted_algos and "Transformer" not in [a for a, _ in sorted_algos]:
        gap_insights.append(
            "Transformer-based architectures appear underrepresented in this research area."
        )

    return {
        "total_papers": total_papers,
        "algorithm_frequency": dict(sorted_algos),
        "dataset_frequency": dict(sorted_datasets),
        "metric_frequency": dict(sorted_metrics),
        "gap_insights": gap_insights,
        "dominant_algorithms": dominant_algos,
        "rarely_used_algorithms": rarely_used_algos,
    }