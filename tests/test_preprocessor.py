import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from backend.services.ml_engine.preprocessor import (
    clean_dataset,
    encode_features,
    scale_features,
)


def make_dirty_df():
    return pd.DataFrame({
        "age": [25, None, 35, 40, 25],
        "city": ["delhi", "mumbai", None, "delhi", "mumbai"],
        "salary": [50000, 60000, 70000, 80000, 50000],
        "target": [0, 1, 1, 0, 0]
    })


def test_clean_removes_duplicates():
    df = make_dirty_df()
    cleaned = clean_dataset(df, "target")
    assert cleaned.duplicated().sum() == 0
    print("✅ test_clean_removes_duplicates passed")


def test_clean_fills_missing_numeric():
    df = make_dirty_df()
    cleaned = clean_dataset(df, "target")
    assert cleaned["age"].isnull().sum() == 0
    print("✅ test_clean_fills_missing_numeric passed")


def test_clean_fills_missing_categorical():
    df = make_dirty_df()
    cleaned = clean_dataset(df, "target")
    assert cleaned["city"].isnull().sum() == 0
    print("✅ test_clean_fills_missing_categorical passed")


def test_encode_features():
    df = pd.DataFrame({
        "city": ["delhi", "mumbai", "delhi"],
        "target": [0, 1, 0]
    })
    encoded, encoders = encode_features(df, "target")
    assert encoded["city"].dtype in [np.int32, np.int64, int]
    assert "city" in encoders
    print("✅ test_encode_features passed")


def test_scale_features():
    df = pd.DataFrame({
        "age": [20.0, 30.0, 40.0, 50.0],
        "salary": [30000.0, 50000.0, 70000.0, 90000.0]
    })
    scaled, scaler = scale_features(df, method="standard")
    # after standard scaling mean should be near 0
    assert abs(scaled["age"].mean()) < 0.01
    print("✅ test_scale_features passed")


def test_minmax_scale():
    df = pd.DataFrame({
        "age": [0.0, 50.0, 100.0],
    })
    scaled, scaler = scale_features(df, method="minmax")
    assert scaled["age"].min() >= 0.0
    assert scaled["age"].max() <= 1.0
    print("✅ test_minmax_scale passed")


if __name__ == "__main__":
    print("running preprocessor tests...\n")
    test_clean_removes_duplicates()
    test_clean_fills_missing_numeric()
    test_clean_fills_missing_categorical()
    test_encode_features()
    test_scale_features()
    test_minmax_scale()
    print("\nall preprocessor tests passed ✅")