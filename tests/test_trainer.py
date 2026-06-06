import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, load_diabetes
from backend.services.ml_engine.trainer import (
    train_all_models,
    get_best_model,
    get_classification_models,
    get_regression_models,
)


def test_classification_models_exist():
    models = get_classification_models()
    assert "Random Forest" in models
    assert "XGBoost" in models
    assert "Logistic Regression" in models
    print("✅ test_classification_models_exist passed")


def test_regression_models_exist():
    models = get_regression_models()
    assert "Linear Regression" in models
    assert "Random Forest Regressor" in models
    print("✅ test_regression_models_exist passed")


def test_train_classification():
    # use iris dataset — simple and fast
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target)

    results, trained_models = train_all_models(X, y, "classification")

    assert len(results) > 0
    assert len(trained_models) > 0

    for model_name, metrics in results.items():
        if "error" not in metrics:
            assert "accuracy" in metrics
            assert 0 <= metrics["accuracy"] <= 1
    print("✅ test_train_classification passed")


def test_train_regression():
    diabetes = load_diabetes()
    X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
    y = pd.Series(diabetes.target)

    results, trained_models = train_all_models(X, y, "regression")

    assert len(results) > 0
    for model_name, metrics in results.items():
        if "error" not in metrics:
            assert "r2_score" in metrics
    print("✅ test_train_regression passed")


def test_get_best_model_classification():
    mock_results = {
        "Model A": {"f1_score": 0.85, "accuracy": 0.86},
        "Model B": {"f1_score": 0.91, "accuracy": 0.92},
        "Model C": {"f1_score": 0.78, "accuracy": 0.79},
    }
    best_name, best_score = get_best_model(mock_results, "classification")
    assert best_name == "Model B"
    assert best_score == 0.91
    print("✅ test_get_best_model_classification passed")


def test_get_best_model_regression():
    mock_results = {
        "Model A": {"r2_score": 0.72},
        "Model B": {"r2_score": 0.88},
        "Model C": {"error": "failed"},
    }
    best_name, best_score = get_best_model(mock_results, "regression")
    assert best_name == "Model B"
    print("✅ test_get_best_model_regression passed")


if __name__ == "__main__":
    print("running trainer tests...\n")
    test_classification_models_exist()
    test_regression_models_exist()
    test_train_classification()
    test_train_regression()
    test_get_best_model_classification()
    test_get_best_model_regression()
    print("\nall trainer tests passed ✅")