from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.models.database import get_db
from backend.services.ml_engine.experiment_service import (
    save_uploaded_dataset,
    run_experiment,
    get_all_experiments,
    get_experiment_by_id,
    load_dataset,
)
from backend.services.ml_engine.data_profiler import profile_dataset, detect_problem_type

router = APIRouter(prefix="/experiments", tags=["ML Experiments"])


@router.post("/profile")
async def profile_only(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # just profile the dataset without training
    content = await file.read()
    file_path = save_uploaded_dataset(content, file.filename)

    import pandas as pd
    df = pd.read_csv(file_path) if file.filename.endswith(".csv") else pd.read_excel(file_path)
    profile = profile_dataset(df)

    return {
        "filename": file.filename,
        "profile": profile,
        "columns": df.columns.tolist(),
    }


@router.post("/run")
async def run_ml_experiment(
    file: UploadFile = File(...),
    target_column: str = Form(...),
    experiment_name: str = Form(...),
    db: Session = Depends(get_db)
):
    if not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files supported")

    try:
        content = await file.read()
        file_path = save_uploaded_dataset(content, file.filename)
        result = run_experiment(file_path, target_column, experiment_name, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def list_experiments(db: Session = Depends(get_db)):
    experiments = get_all_experiments(db)
    return [
        {
            "id": e.id,
            "name": e.name,
            "dataset": e.dataset_name,
            "problem_type": e.problem_type,
            "best_model": e.best_model,
            "best_score": e.best_score,
            "status": e.status,
            "created_at": e.created_at,
        }
        for e in experiments
    ]


@router.get("/{exp_id}")
def get_experiment(exp_id: str, db: Session = Depends(get_db)):
    exp = get_experiment_by_id(exp_id, db)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp