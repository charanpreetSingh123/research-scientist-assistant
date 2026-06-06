import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif, f_regression
from typing import Tuple


def clean_dataset(df: pd.DataFrame, target_col: str = None) -> pd.DataFrame:
    df = df.copy()

    # drop columns that are entirely empty
    df.dropna(axis=1, how="all", inplace=True)

    # drop duplicate rows
    df.drop_duplicates(inplace=True)

    # fill missing numeric values with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target_col and target_col in numeric_cols:
        numeric_cols.remove(target_col)

    if numeric_cols:
        imputer = SimpleImputer(strategy="median")
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

    # fill missing categorical with mode
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    if target_col and target_col in cat_cols:
        cat_cols.remove(target_col)

    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "unknown")

    return df


def encode_features(df: pd.DataFrame, target_col: str = None) -> Tuple[pd.DataFrame, dict]:
    df = df.copy()
    encoders = {}

    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    return df, encoders


def scale_features(X: pd.DataFrame, method: str = "standard") -> Tuple[pd.DataFrame, object]:
    if method == "minmax":
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()

    X_scaled = pd.DataFrame(
        scaler.fit_transform(X),
        columns=X.columns
    )
    return X_scaled, scaler


def select_features(X: pd.DataFrame, y: pd.Series, problem_type: str, k: int = 10) -> list:
    # pick top k most important features using statistical tests
    k = min(k, X.shape[1])

    score_func = f_classif if problem_type == "classification" else f_regression
    selector = SelectKBest(score_func=score_func, k=k)
    selector.fit(X, y)

    selected = X.columns[selector.get_support()].tolist()
    return selected


def prepare_data(df: pd.DataFrame, target_col: str, problem_type: str):
    # full preprocessing pipeline
    df = clean_dataset(df, target_col)
    df, encoders = encode_features(df, target_col)

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # feature selection — only if we have more than 5 features
    if X.shape[1] > 5:
        selected_features = select_features(X, y, problem_type)
        X = X[selected_features]
    else:
        selected_features = X.columns.tolist()

    X_scaled, scaler = scale_features(X)

    return X_scaled, y, scaler, encoders, selected_features