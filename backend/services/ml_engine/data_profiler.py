import pandas as pd
import numpy as np


def profile_dataset(df: pd.DataFrame) -> dict:
    # basic shape info
    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "missing_percentage": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
    }

    # numeric stats
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        profile["numeric_stats"] = df[numeric_cols].describe().round(4).to_dict()
        profile["numeric_columns"] = numeric_cols

    # categorical stats
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    profile["categorical_columns"] = cat_cols
    if cat_cols:
        profile["categorical_stats"] = {
            col: {
                "unique_values": int(df[col].nunique()),
                "top_values": df[col].value_counts().head(5).to_dict()
            }
            for col in cat_cols
        }

    # correlation matrix for numeric cols
    if len(numeric_cols) > 1:
        profile["correlation"] = df[numeric_cols].corr().round(3).to_dict()

    return profile


def detect_problem_type(df: pd.DataFrame, target_col: str) -> str:
    if target_col not in df.columns:
        return "clustering"

    target = df[target_col]
    n_unique = target.nunique()
    dtype = target.dtype

    # if dtype is numeric and has many unique values = regression
    if dtype in ["float64", "float32", "int64", "int32"] and n_unique > 20:
        return "regression"
    # if few unique values or object type = classification
    elif dtype == "object" or n_unique <= 20:
        return "classification"
    else:
        return "regression"


def check_class_imbalance(df: pd.DataFrame, target_col: str) -> dict:
    if target_col not in df.columns:
        return {}

    counts = df[target_col].value_counts()
    total = len(df)
    ratio = counts.min() / counts.max()

    return {
        "class_counts": counts.to_dict(),
        "imbalance_ratio": round(ratio, 3),
        "is_imbalanced": ratio < 0.3
    }