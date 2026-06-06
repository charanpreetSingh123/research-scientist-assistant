from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path

from backend.models.database import get_db
from backend.services.ml_engine.experiment_service import get_experiment_by_id
from backend.services.report_generator.pdf_report import generate_experiment_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate/{experiment_id}")
def generate_report(experiment_id: str, db: Session = Depends(get_db)):
    exp = get_experiment_by_id(experiment_id, db)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    experiment_data = {
        "experiment_name": exp.name,
        "dataset_name": exp.dataset_name,
        "problem_type": exp.problem_type,
        "best_model": exp.best_model,
        "best_score": exp.best_score or 0,
        "all_results": exp.metrics or {},
        "feature_importance": exp.feature_importance or {},
        "dataset_profile": {},
    }

    report_path = generate_experiment_report(
        experiment_data,
        output_filename=f"report_{experiment_id[:8]}.pdf"
    )

    # save path back to experiment
    exp.report_path = report_path
    db.commit()

    return {
        "message": "Report generated successfully",
        "report_path": report_path,
        "experiment_id": experiment_id
    }


@router.get("/download/{experiment_id}")
def download_report(experiment_id: str, db: Session = Depends(get_db)):
    exp = get_experiment_by_id(experiment_id, db)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    if not exp.report_path or not Path(exp.report_path).exists():
        raise HTTPException(status_code=404, detail="Report not generated yet")

    return FileResponse(
        path=exp.report_path,
        media_type="application/pdf",
        filename=f"report_{exp.name[:20]}.pdf"
    )