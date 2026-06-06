from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.database import get_db
from backend.models.schemas import ResearchPaper, Experiment

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    total_papers = db.query(ResearchPaper).count()
    total_experiments = db.query(Experiment).count()
    completed = db.query(Experiment).filter(Experiment.status == "complete").count()
    failed = db.query(Experiment).filter(Experiment.status == "failed").count()

    return {
        "total_papers": total_papers,
        "total_experiments": total_experiments,
        "completed_experiments": completed,
        "failed_experiments": failed,
    }


@router.get("/model-performance")
def model_performance(db: Session = Depends(get_db)):
    # collect all model scores across all experiments
    experiments = db.query(Experiment).filter(
        Experiment.status == "complete",
        Experiment.metrics != None
    ).all()

    model_scores = {}

    for exp in experiments:
        if not exp.metrics:
            continue
        for model_name, metrics in exp.metrics.items():
            if "error" in metrics:
                continue

            if exp.problem_type == "classification":
                score = metrics.get("f1_score", 0)
            elif exp.problem_type == "regression":
                score = metrics.get("r2_score", 0)
            else:
                score = metrics.get("silhouette_score", 0)

            if model_name not in model_scores:
                model_scores[model_name] = []
            model_scores[model_name].append(round(score, 4))

    # average score per model
    avg_scores = {
        model: round(sum(scores) / len(scores), 4)
        for model, scores in model_scores.items()
    }

    return {
        "model_average_scores": avg_scores,
        "model_run_counts": {m: len(s) for m, s in model_scores.items()}
    }


@router.get("/research-trends")
def research_trends(db: Session = Depends(get_db)):
    papers = db.query(ResearchPaper).all()

    algo_count = {}
    metric_count = {}
    dataset_count = {}

    for paper in papers:
        for algo in (paper.algorithms_used or []):
            algo_count[algo] = algo_count.get(algo, 0) + 1
        for metric in (paper.evaluation_metrics or []):
            metric_count[metric] = metric_count.get(metric, 0) + 1
        for ds in (paper.datasets_used or []):
            dataset_count[ds] = dataset_count.get(ds, 0) + 1

    return {
        "top_algorithms": dict(sorted(algo_count.items(), key=lambda x: x[1], reverse=True)[:10]),
        "top_metrics": dict(sorted(metric_count.items(), key=lambda x: x[1], reverse=True)[:10]),
        "top_datasets": dict(sorted(dataset_count.items(), key=lambda x: x[1], reverse=True)[:10]),
    }