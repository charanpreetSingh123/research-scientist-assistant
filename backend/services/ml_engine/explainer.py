import pandas as pd
import numpy as np
import shap


def get_feature_importance(model, X: pd.DataFrame, model_name: str) -> dict:
    importance = {}

    try:
        # tree-based models have built-in feature importance
        if hasattr(model, "feature_importances_"):
            scores = model.feature_importances_
            importance = dict(zip(X.columns.tolist(), [round(float(s), 4) for s in scores]))
            importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))

        # linear models use coefficients
        elif hasattr(model, "coef_"):
            coefs = np.abs(model.coef_).flatten()
            importance = dict(zip(X.columns.tolist(), [round(float(c), 4) for c in coefs]))
            importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))

    except Exception as e:
        print(f"feature importance failed for {model_name}: {e}")

    return importance


def get_shap_values(model, X: pd.DataFrame, model_name: str, max_samples: int = 100) -> dict:
    # limit samples to keep it fast
    X_sample = X.iloc[:max_samples] if len(X) > max_samples else X

    shap_summary = {}

    try:
        # tree explainer works for RF, XGBoost, GBM
        if any(keyword in model_name.lower() for keyword in ["forest", "xgb", "boost", "tree"]):
            explainer = shap.TreeExplainer(model)
            shap_vals = explainer.shap_values(X_sample)

            # handle multi-class (shap returns list)
            if isinstance(shap_vals, list):
                shap_vals = shap_vals[0]

            mean_shap = np.abs(shap_vals).mean(axis=0)
            shap_summary = dict(zip(
                X.columns.tolist(),
                [round(float(v), 4) for v in mean_shap]
            ))
            shap_summary = dict(sorted(shap_summary.items(), key=lambda x: x[1], reverse=True))

        else:
            # fall back to basic feature importance
            shap_summary = get_feature_importance(model, X_sample, model_name)

    except Exception as e:
        print(f"SHAP failed for {model_name}, using feature importance instead: {e}")
        shap_summary = get_feature_importance(model, X_sample, model_name)

    return shap_summary