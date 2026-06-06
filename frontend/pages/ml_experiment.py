import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.ui_helpers import load_css, page_header, section_header, divider, success_banner, error_banner, plotly_dark_layout

load_css()
API_URL = "http://localhost:8000/api"

page_header("ML Experiments", "Auto-profile datasets, train models, explain results", "🧪")

tabs = st.tabs(["📊  Profile Dataset", "🚀  Run Experiment", "📈  History"])

# ── Tab 1: Profile ────────────────────────────────────────
with tabs[0]:
    section_header("Dataset Profiler", "Get a full statistical breakdown before training")
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"], label_visibility="collapsed")

    if uploaded:
        with st.spinner("Profiling..."):
            try:
                files = {"file": (uploaded.name, uploaded.getvalue())}
                response = requests.post(f"{API_URL}/experiments/profile", files=files)

                if response.status_code == 200:
                    data = response.json()
                    profile = data["profile"]

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Rows", f"{profile['rows']:,}")
                    c2.metric("Columns", profile["columns"])
                    c3.metric("Duplicates", profile["duplicate_rows"])
                    c4.metric("Missing Values", sum(profile["missing_values"].values()))

                    divider()

                    col1, col2 = st.columns(2)
                    with col1:
                        section_header("Column Types")
                        dtype_df = pd.DataFrame(profile["dtypes"].items(), columns=["Column", "Type"])
                        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

                    with col2:
                        if profile.get("correlation"):
                            section_header("Correlation Heatmap")
                            corr_df = pd.DataFrame(profile["correlation"])
                            fig = px.imshow(
                                corr_df,
                                color_continuous_scale=[[0, "#1a1d2e"], [0.5, "#4C9BE8"], [1, "#00d4aa"]],
                            )
                            fig = plotly_dark_layout(fig, height=300)
                            st.plotly_chart(fig, use_container_width=True)

                    if profile.get("numeric_stats"):
                        section_header("Numeric Statistics")
                        st.dataframe(pd.DataFrame(profile["numeric_stats"]).round(3), use_container_width=True)

                    success_banner("Profile complete — go to Run Experiment tab to train models")
                else:
                    error_banner(response.json().get("detail", "Profiling failed"))
            except Exception as e:
                error_banner(f"Error: {e}")

# ── Tab 2: Run Experiment ─────────────────────────────────
with tabs[1]:
    section_header("Train & Evaluate Models", "Automated multi-model training with SHAP explainability")

    uploaded_exp = st.file_uploader("Upload dataset", type=["csv", "xlsx"], key="exp_upload", label_visibility="collapsed")

    if uploaded_exp:
        df_preview = pd.read_csv(io.BytesIO(uploaded_exp.getvalue())) if uploaded_exp.name.endswith(".csv") else pd.read_excel(io.BytesIO(uploaded_exp.getvalue()))

        st.markdown(f"""
        <div style="background:#1a1d2e; border:1px solid #2d3154; border-radius:10px;
                    padding:12px 16px; margin-bottom:1rem; font-size:0.85rem; color:#94a3b8;">
            📁 <strong style="color:#e2e8f0;">{uploaded_exp.name}</strong>
            &nbsp;·&nbsp; {df_preview.shape[0]:,} rows
            &nbsp;·&nbsp; {df_preview.shape[1]} columns
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            target_col = st.selectbox("Target column", df_preview.columns.tolist())
        with col2:
            exp_name = st.text_input("Experiment name", value=f"Exp — {uploaded_exp.name}")

        if st.button("🚀 Run Experiment", type="primary"):
            with st.spinner("Training models... this may take a minute"):
                try:
                    files = {"file": (uploaded_exp.name, uploaded_exp.getvalue())}
                    data = {"target_column": target_col, "experiment_name": exp_name}
                    response = requests.post(f"{API_URL}/experiments/run", files=files, data=data)

                    if response.status_code == 200:
                        result = response.json()

                        success_banner(f"Best model: {result['best_model']} — score: {round(result['best_score'], 4)}")

                        st.markdown(f"""
                        <div style="font-size:0.85rem; color:#64748b; margin-bottom:1rem;">
                            Problem type detected:
                            <span style="color:#4C9BE8; font-weight:600;">{result['problem_type']}</span>
                        </div>
                        """, unsafe_allow_html=True)

                        col1, col2 = st.columns(2)

                        with col1:
                            section_header("Model Comparison")
                            all_results = result["all_results"]
                            model_names, scores = [], []

                            for model, metrics in all_results.items():
                                if "error" not in metrics:
                                    model_names.append(model)
                                    if result["problem_type"] == "classification":
                                        scores.append(metrics.get("f1_score", 0))
                                    elif result["problem_type"] == "regression":
                                        scores.append(metrics.get("r2_score", 0))
                                    else:
                                        scores.append(metrics.get("silhouette_score", 0))

                            colors = ["#00d4aa" if m == result["best_model"] else "#4C9BE8" for m in model_names]
                            fig = go.Figure(go.Bar(
                                x=scores, y=model_names,
                                orientation="h",
                                marker_color=colors,
                                marker_line_width=0,
                            ))
                            fig = plotly_dark_layout(fig, "Score by Model", height=320)
                            st.plotly_chart(fig, use_container_width=True)

                        with col2:
                            if result.get("feature_importance"):
                                section_header("Feature Importance (SHAP)")
                                fi = result["feature_importance"]
                                fi_df = pd.DataFrame(fi.items(), columns=["Feature", "Importance"]).sort_values("Importance")
                                fig2 = go.Figure(go.Bar(
                                    x=fi_df["Importance"], y=fi_df["Feature"],
                                    orientation="h",
                                    marker_color="#a855f7",
                                    marker_line_width=0,
                                ))
                                fig2 = plotly_dark_layout(fig2, "SHAP Values", height=320)
                                st.plotly_chart(fig2, use_container_width=True)

                        divider()
                        section_header("Detailed Results")
                        rows = []
                        for model, metrics in all_results.items():
                            if "error" not in metrics:
                                row = {"Model": model}
                                row.update(metrics)
                                if model == result["best_model"]:
                                    row["Model"] = f"⭐ {model}"
                                rows.append(row)
                        if rows:
                            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
                    else:
                        error_banner(response.json().get("detail", "Experiment failed"))
                except Exception as e:
                    error_banner(f"Error: {e}")

# ── Tab 3: History ────────────────────────────────────────
with tabs[2]:
    section_header("Experiment History", "All past runs")
    try:
        response = requests.get(f"{API_URL}/experiments/")
        if response.status_code == 200:
            experiments = response.json()
            if not experiments:
                st.markdown("""
                <div style="text-align:center; padding:40px; color:#64748b;">
                    <div style="font-size:3rem;">🧪</div>
                    <div style="font-weight:600; margin-top:8px;">No experiments yet</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for exp in experiments:
                    status_color = "#00d4aa" if exp["status"] == "complete" else "#ef4444" if exp["status"] == "failed" else "#f59e0b"
                    status_icon = "✅" if exp["status"] == "complete" else "❌" if exp["status"] == "failed" else "⏳"
                    with st.expander(f"{status_icon}  {exp['name']}"):
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Problem Type", exp["problem_type"] or "N/A")
                        c2.metric("Best Model", exp["best_model"] or "N/A")
                        c3.metric("Score", round(exp["best_score"] or 0, 4))
    except Exception as e:
        error_banner(f"Cannot connect to API: {e}")