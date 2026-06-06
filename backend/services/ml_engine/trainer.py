import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score,
    silhouette_score
)
from xgboost import XGBClassifier, XGBRegressor
import joblib
import time


def get_classification_models() -> dict:
    return {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=100, random_state=42, eval_metric="logloss", verbosity=0),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "SVM": SVC(probability=True, random_state=42),
    }


def get_regression_models() -> dict:
    return {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost Regressor": XGBRegressor(n_estimators=100, random_state=42, verbosity=0),
    }


def get_clustering_models(n_clusters: int = 3) -> dict:
    return {
        "KMeans": KMeans(n_clusters=n_clusters, random_state=42, n_init=10),
        "Agglomerative": AgglomerativeClustering(n_clusters=n_clusters),
        "DBSCAN": DBSCAN(eps=0.5, min_samples=5),
    }


def evaluate_classification(model, X_train, X_test, y_train, y_test) -> dict:
    start = time.time()
    model.fit(X_train, y_train)
    train_time = round(time.time() - start, 3)

    y_pred = model.predict(X_test)

    return {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred, average="weighted", zero_division=0), 4),
        "recall": round(recall_score(y_test, y_pred, average="weighted", zero_division=0), 4),
        "f1_score": round(f1_score(y_test, y_pred, average="weighted", zero_division=0), 4),
        "train_time_seconds": train_time,
    }


def evaluate_regression(model, X_train, X_test, y_train, y_test) -> dict:
    start = time.time()
    model.fit(X_train, y_train)
    train_time = round(time.time() - start, 3)

    y_pred = model.predict(X_test)

    return {
        "r2_score": round(r2_score(y_test, y_pred), 4),
        "mse": round(mean_squared_error(y_test, y_pred), 4),
        "rmse": round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
        "mae": round(mean_absolute_error(y_test, y_pred), 4),
        "train_time_seconds": train_time,
    }


def evaluate_clustering(model, X) -> dict:
    start = time.time()
    labels = model.fit_predict(X)
    train_time = round(time.time() - start, 3)

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    score = 0.0
    if n_clusters > 1:
        try:
            score = round(silhouette_score(X, labels), 4)
        except Exception:
            score = 0.0

    return {
        "n_clusters_found": n_clusters,
        "silhouette_score": score,
        "train_time_seconds": train_time,
    }


def train_all_models(X, y, problem_type: str) -> dict:
    results = {}
    trained_models = {}

    if problem_type == "classification":
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() > 1 else None
        )
        models = get_classification_models()
        for name, model in models.items():
            print(f"training {name}...")
            try:
                metrics = evaluate_classification(model, X_train, X_test, y_train, y_test)
                results[name] = metrics
                trained_models[name] = model
            except Exception as e:
                print(f"{name} failed: {e}")
                results[name] = {"error": str(e)}

    elif problem_type == "regression":
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        models = get_regression_models()
        for name, model in models.items():
            print(f"training {name}...")
            try:
                metrics = evaluate_regression(model, X_train, X_test, y_train, y_test)
                results[name] = metrics
                trained_models[name] = model
            except Exception as e:
                print(f"{name} failed: {e}")
                results[name] = {"error": str(e)}

    elif problem_type == "clustering":
        models = get_clustering_models()
        for name, model in models.items():
            print(f"training {name}...")
            try:
                metrics = evaluate_clustering(model, X)
                results[name] = metrics
                trained_models[name] = model
            except Exception as e:
                print(f"{name} failed: {e}")
                results[name] = {"error": str(e)}

    return results, trained_models


def get_best_model(results: dict, problem_type: str) -> str:
    # pick best model based on primary metric
    best_name = None
    best_score = -999

    for name, metrics in results.items():
        if "error" in metrics:
            continue

        if problem_type == "classification":
            score = metrics.get("f1_score", 0)
        elif problem_type == "regression":
            score = metrics.get("r2_score", -999)
        else:
            score = metrics.get("silhouette_score", 0)

        if score > best_score:
            best_score = score
            best_name = name

    return best_name, best_score