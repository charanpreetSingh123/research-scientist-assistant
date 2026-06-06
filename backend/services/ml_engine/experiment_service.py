import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.schemas import Experiment
from backend.services.ml_engine.data_profiler import profile_dataset, detect_problem_type
from backend.services.ml_engine.preprocessor import prepare_data
from backend.services.ml_engine.trainer import train_all_models, get_best_model
from backend.services.ml_engine.explainer import get_shap_values


def save_uploaded_dataset(file_content: bytes, filename: str) -> str:
    dataset_dir = Path(settings.UPLOAD_DIR) / "datasets"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    file_path = dataset_dir / filename
    with open(file_path, "wb") as f:
        f.write(file_content)
    return str(file_path)


def load_dataset(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)
    else:
        raise ValueError("only CSV and Excel files supported")


def run_experiment(
    file_path: str,
    target_col: str,
    experiment_name: str,
    db: Session
) -> dict:

    print(f"starting experiment: {experiment_name}")

    # load and profile
    df = load_dataset(file_path)
    profile = profile_dataset(df)
    problem_type = detect_problem_type(df, target_col)

    print(f"problem type detected: {problem_type}")

    # save experiment record as running
    experiment = Experiment(
        name=experiment_name,
        dataset_name=Path(file_path).name,
        problem_type=problem_type,
        status="running",
        owner_id=None,
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    try:
        # preprocess
        X, y, scaler, encoders, selected_features = prepare_data(df, target_col, problem_type)

        # train all models
        results, trained_models = train_all_models(X, y, problem_type)

        # get best model
        best_model_name, best_score = get_best_model(results, problem_type)

        # get SHAP explanation for best model
        shap_summary = {}
        if best_model_name and best_model_name in trained_models:
            shap_summary = get_shap_values(
                trained_models[best_model_name], X, best_model_name
            )

        # update experiment record
        experiment.models_trained = list(results.keys())
        experiment.best_model = best_model_name
        experiment.best_score = float(best_score) if best_score else 0.0
        experiment.metrics = results
        experiment.feature_importance = shap_summary
        experiment.status = "complete"

        db.commit()
        db.refresh(experiment)

        return {
            "experiment_id": experiment.id,
            "experiment_name": experiment_name,
            "problem_type": problem_type,
            "best_model": best_model_name,
            "best_score": best_score,
            "all_results": results,
            "feature_importance": shap_summary,
            "dataset_profile": profile,
            "selected_features": selected_features,
        }

    except Exception as e:
        experiment.status = "failed"
        db.commit()
        raise e


def get_all_experiments(db: Session) -> list:
    return db.query(Experiment).order_by(Experiment.created_at.desc()).all()


def get_experiment_by_id(exp_id: str, db: Session) -> Experiment:
    return db.query(Experiment).filter(Experiment.id == exp_id).first()