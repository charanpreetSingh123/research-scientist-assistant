import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

API_URL = "http://localhost:8000/api"

st.title("📊 Analytics Dashboard")
st.markdown("---")

# ── Overview metrics ─────────────────────────────────────────
try:
    response = requests.get(f"{API_URL}/analytics/overview")
    if response.status_code == 200:
        overview = response.json()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📄 Papers Uploaded", overview["total_papers"])
        col2.metric("🧪 Experiments Run", overview["total_experiments"])
        col3.metric("✅ Completed", overview["completed_experiments"])
        col4.metric("❌ Failed", overview["failed_experiments"])
except Exception as e:
    st.error(f"Cannot connect to API: {e}")

st.markdown("---")

col_left, col_right = st.columns(2)

# ── Model performance chart ──────────────────────────────────
with col_left:
    st.subheader("🏆 Model Performance (Avg Score)")
    try:
        response = requests.get(f"{API_URL}/analytics/model-performance")
        if response.status_code == 200:
            data = response.json()
            avg_scores = data.get("model_average_scores", {})

            if avg_scores:
                df = pd.DataFrame(avg_scores.items(), columns=["Model", "Avg Score"])
                df = df.sort_values("Avg Score", ascending=True)
                fig = px.bar(
                    df, x="Avg Score", y="Model",
                    orientation="h",
                    color="Avg Score",
                    color_continuous_scale="Blues",
                    title="Average Score per Model"
                )
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Run some experiments to see model performance here.")
    except Exception as e:
        st.error(f"Error: {e}")

# ── Research trends ──────────────────────────────────────────
with col_right:
    st.subheader("📈 Research Trends")
    try:
        response = requests.get(f"{API_URL}/analytics/research-trends")
        if response.status_code == 200:
            trends = response.json()
            top_algos = trends.get("top_algorithms", {})

            if top_algos:
                df = pd.DataFrame(top_algos.items(), columns=["Algorithm", "Count"])
                fig = px.pie(
                    df, names="Algorithm", values="Count",
                    title="Algorithm Usage in Papers",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Upload research papers to see trends here.")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

# ── Top metrics and datasets ─────────────────────────────────
st.subheader("📋 Research Metrics & Datasets")
col1, col2 = st.columns(2)

try:
    response = requests.get(f"{API_URL}/analytics/research-trends")
    if response.status_code == 200:
        trends = response.json()

        with col1:
            top_metrics = trends.get("top_metrics", {})
            if top_metrics:
                df = pd.DataFrame(top_metrics.items(), columns=["Metric", "Count"])
                fig = px.bar(df, x="Count", y="Metric", orientation="h",
                             color="Count", color_continuous_scale="Greens",
                             title="Most Used Evaluation Metrics")
                fig.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No metric data yet.")

        with col2:
            top_datasets = trends.get("top_datasets", {})
            if top_datasets:
                df = pd.DataFrame(top_datasets.items(), columns=["Dataset", "Count"])
                fig = px.bar(df, x="Count", y="Dataset", orientation="h",
                             color="Count", color_continuous_scale="Oranges",
                             title="Most Referenced Datasets")
                fig.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No dataset data yet.")
except Exception as e:
    st.error(f"Error: {e}")