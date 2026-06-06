import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io

API_URL = "http://localhost:8000/api"

st.title("🧪 ML Experimentation Engine")
st.markdown("---")

tabs = st.tabs(["📊 Profile Dataset", "🚀 Run Experiment", "📈 Experiment History"])

# ── Tab 1: Profile ───────────────────────────────────────────
with tabs[0]:
    st.subheader("Dataset Profiler")
    uploaded = st.file_uploader("Upload CSV or Excel dataset", type=["csv", "xlsx"])

    if uploaded:
        with st.spinner("Profiling dataset..."):
            try:
                files = {"file": (uploaded.name, uploaded.getvalue())}
                response = requests.post(f"{API_URL}/experiments/profile", files=files)

                if response.status_code == 200:
                    data = response.json()
                    profile = data["profile"]

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Rows", profile["rows"])
                    col2.metric("Columns", profile["columns"])
                    col3.metric("Duplicates", profile["duplicate_rows"])
                    missing_total = sum(profile["missing_values"].values())
                    col4.metric("Missing Values", missing_total)

                    st.markdown("**Column Types**")
                    dtype_df = pd.DataFrame(
                        profile["dtypes"].items(),
                        columns=["Column", "Type"]
                    )
                    st.dataframe(dtype_df, use_container_width=True)

                    if profile.get("numeric_stats"):
                        st.markdown("**Numeric Statistics**")
                        stats_df = pd.DataFrame(profile["numeric_stats"])
                        st.dataframe(stats_df.round(3), use_container_width=True)

                    if profile.get("correlation"):
                        st.markdown("**Correlation Matrix**")
                        corr_df = pd.DataFrame(profile["correlation"])
                        fig = px.imshow(
                            corr_df,
                            color_continuous_scale="RdBu",
                            title="Feature Correlation"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    # store columns in session for experiment tab
                    st.session_state["dataset_columns"] = data["columns"]
                    st.session_state["uploaded_dataset"] = uploaded
                    st.success("Done! Go to 'Run Experiment' tab to train models.")
                else:
                    st.error(response.json().get("detail", "Profiling failed"))
            except Exception as e:
                st.error(f"Error: {e}")

# ── Tab 2: Run Experiment ────────────────────────────────────
with tabs[1]:
    st.subheader("Train & Evaluate Models")

    uploaded_exp = st.file_uploader("Upload dataset", type=["csv", "xlsx"], key="exp_upload")

    if uploaded_exp:
        # preview columns
        df_preview = pd.read_csv(io.BytesIO(uploaded_exp.getvalue())) if uploaded_exp.name.endswith(".csv") else pd.read_excel(io.BytesIO(uploaded_exp.getvalue()))
        columns = df_preview.columns.tolist()

        col1, col2 = st.columns(2)
        with col1:
            target_col = st.selectbox("Select target column", columns)
        with col2:
            exp_name = st.text_input("Experiment name", value=f"Experiment on {uploaded_exp.name}")

        st.info(f"Dataset shape: {df_preview.shape[0]} rows × {df_preview.shape[1]} columns")

        if st.button("🚀 Run Experiment", type="primary"):
            with st.spinner("Training models... this may take a minute"):
                try:
                    files = {"file": (uploaded_exp.name, uploaded_exp.getvalue())}
                    data = {"target_column": target_col, "experiment_name": exp_name}
                    response = requests.post(f"{API_URL}/experiments/run", files=files, data=data)

                    if response.status_code == 200:
                        result = response.json()

                        st.success(f"✅ Best model: **{result['best_model']}** — score: {result['best_score']}")
                        st.markdown(f"**Problem type detected:** {result['problem_type']}")

                        # model comparison chart
                        st.markdown("### Model Comparison")
                        all_results = result["all_results"]
                        model_names = []
                        scores = []

                        for model, metrics in all_results.items():
                            if "error" not in metrics:
                                model_names.append(model)
                                if result["problem_type"] == "classification":
                                    scores.append(metrics.get("f1_score", 0))
                                elif result["problem_type"] == "regression":
                                    scores.append(metrics.get("r2_score", 0))
                                else:
                                    scores.append(metrics.get("silhouette_score", 0))

                        fig = go.Figure(go.Bar(
                            x=scores,
                            y=model_names,
                            orientation="h",
                            marker_color=["#4C9BE8" if m != result["best_model"] else "#E8834C" for m in model_names]
                        ))
                        fig.update_layout(
                            title="Model Scores (orange = best)",
                            xaxis_title="Score",
                            height=300
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        # feature importance
                        if result.get("feature_importance"):
                            st.markdown("### Feature Importance (SHAP)")
                            fi = result["feature_importance"]
                            fi_df = pd.DataFrame(fi.items(), columns=["Feature", "Importance"]).sort_values("Importance", ascending=True)
                            fig2 = go.Figure(go.Bar(
                                x=fi_df["Importance"],
                                y=fi_df["Feature"],
                                orientation="h",
                                marker_color="#4CE87A"
                            ))
                            fig2.update_layout(height=400, title="Feature Importance")
                            st.plotly_chart(fig2, use_container_width=True)

                        # full metrics table
                        st.markdown("### Detailed Results")
                        metrics_rows = []
                        for model, metrics in all_results.items():
                            if "error" not in metrics:
                                row = {"Model": model}
                                row.update(metrics)
                                metrics_rows.append(row)
                        if metrics_rows:
                            st.dataframe(pd.DataFrame(metrics_rows), use_container_width=True)

                    else:
                        st.error(response.json().get("detail", "Experiment failed"))
                except Exception as e:
                    st.error(f"Error: {e}")

# ── Tab 3: History ───────────────────────────────────────────
with tabs[2]:
    st.subheader("Past Experiments")

    try:
        response = requests.get(f"{API_URL}/experiments/")
        if response.status_code == 200:
            experiments = response.json()

            if not experiments:
                st.info("No experiments yet. Run one in the previous tab.")
            else:
                for exp in experiments:
                    status_icon = "✅" if exp["status"] == "complete" else "❌" if exp["status"] == "failed" else "⏳"
                    with st.expander(f"{status_icon} {exp['name']} — {exp['dataset']}"):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Problem Type", exp["problem_type"] or "N/A")
                        col2.metric("Best Model", exp["best_model"] or "N/A")
                        col3.metric("Best Score", round(exp["best_score"] or 0, 4))
    except Exception as e:
        st.error(f"Cannot connect to API: {e}")