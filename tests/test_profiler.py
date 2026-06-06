import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from backend.services.ml_engine.data_profiler import (
    profile_dataset,
    detect_problem_type,
    check_class_imbalance,
)


def make_sample_df():
    return pd.DataFrame({
        "age": [25, 30, 35, 40, None, 28, 33],
        "salary": [50000, 60000, 75000, 90000, 55000, 62000, 71000],
        "department": ["eng", "hr", "eng", "finance", "hr", "eng", "finance"],
        "target": [0, 1, 1, 0, 1, 0, 1]
    })


def test_profile_shape():
    df = make_sample_df()
    profile = profile_dataset(df)
    assert profile["rows"] == 7
    assert profile["columns"] == 4
    print("✅ test_profile_shape passed")


def test_profile_missing_values():
    df = make_sample_df()
    profile = profile_dataset(df)
    assert profile["missing_values"]["age"] == 1
    print("✅ test_profile_missing_values passed")


def test_profile_numeric_columns():
    df = make_sample_df()
    profile = profile_dataset(df)
    assert "age" in profile["numeric_columns"]
    assert "salary" in profile["numeric_columns"]
    print("✅ test_profile_numeric_columns passed")


def test_detect_classification():
    df = make_sample_df()
    result = detect_problem_type(df, "target")
    assert result == "classification"
    print("✅ test_detect_classification passed")


def test_detect_regression():
    # needs enough unique values to trigger regression detection
    df = pd.DataFrame({
        "age": list(range(50)),
        "salary": [float(i * 1000) for i in range(50)],
        "target": [float(i * 2.5) for i in range(50)]  # 50 unique float values
    })
    result = detect_problem_type(df, "target")
    assert result == "regression"
    print("✅ test_detect_regression passed")


def test_detect_clustering_no_target():
    df = make_sample_df()
    result = detect_problem_type(df, "nonexistent_col")
    assert result == "clustering"
    print("✅ test_detect_clustering_no_target passed")


def test_class_imbalance():
    df = pd.DataFrame({
        "target": [0]*90 + [1]*10
    })
    result = check_class_imbalance(df, "target")
    assert result["is_imbalanced"] == True
    print("✅ test_class_imbalance passed")


def test_balanced_classes():
    df = pd.DataFrame({
        "target": [0]*50 + [1]*50
    })
    result = check_class_imbalance(df, "target")
    assert result["is_imbalanced"] == False
    print("✅ test_balanced_classes passed")


if __name__ == "__main__":
    print("running profiler tests...\n")
    test_profile_shape()
    test_profile_missing_values()
    test_profile_numeric_columns()
    test_detect_classification()
    test_detect_regression()
    test_detect_clustering_no_target()
    test_class_imbalance()
    test_balanced_classes()
    print("\nall profiler tests passed ✅")