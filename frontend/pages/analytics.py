import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.ui_helpers import load_css, page_header, section_header, divider, error_banner, plotly_dark_layout

load_css()
API_URL = "http://localhost:8000/api"

page_header("Analytics Dashboard", "Research trends, model performance, experiment insights", "📊")

# ── Overview metrics ──────────────────────────────────────
try:
    response = requests.get(f"{API_URL}/analytics/overview")
    if response.status_code == 200:
        ov = response.json()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📄 Papers", ov["total_papers"])
        c2.metric("🧪 Experiments", ov["total_experiments"])
        c3.metric("✅ Completed", ov["completed_experiments"])
        c4.metric("❌ Failed", ov["failed_experiments"])
except Exception as e:
    error_banner(f"Cannot connect to API: {e}")

divider()

col_left, col_right = st.columns(2)

# ── Model performance ─────────────────────────────────────
with col_left:
    section_header("Model Performance", "Average score across all experiments")
    try:
        response = requests.get(f"{API_URL}/analytics/model-performance")
        if response.status_code == 200:
            data = response.json()
            avg_scores = data.get("model_average_scores", {})
            if avg_scores:
                df = pd.DataFrame(avg_scores.items(), columns=["Model", "Score"]).sort_values("Score")
                fig = go.Figure(go.Bar(
                    x=df["Score"], y=df["Model"],
                    orientation="h",
                    marker=dict(
                        color=df["Score"],
                        colorscale=[[0, "#1e3a5f"], [1, "#4C9BE8"]],
                        line_width=0,
                    )
                ))
                fig = plotly_dark_layout(fig, height=350)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("<div style='text-align:center;padding:40px;color:#64748b;'>Run experiments to see model performance</div>", unsafe_allow_html=True)
    except Exception as e:
        error_banner(f"Error: {e}")

# ── Research trends ───────────────────────────────────────
with col_right:
    section_header("Algorithm Usage in Papers", "From uploaded research literature")
    try:
        response = requests.get(f"{API_URL}/analytics/research-trends")
        if response.status_code == 200:
            trends = response.json()
            top_algos = trends.get("top_algorithms", {})
            if top_algos:
                df = pd.DataFrame(top_algos.items(), columns=["Algorithm", "Count"])
                fig = go.Figure(go.Pie(
                    labels=df["Algorithm"],
                    values=df["Count"],
                    hole=0.55,
                    marker=dict(
                        colors=["#4C9BE8", "#00d4aa", "#f59e0b", "#a855f7",
                                "#ef4444", "#06b6d4", "#84cc16", "#f97316"],
                        line=dict(color="#0f1117", width=2)
                    ),
                    textfont=dict(color="#94a3b8"),
                ))
                fig = plotly_dark_layout(fig, height=350)
                fig.update_layout(
                    legend=dict(font=dict(color="#94a3b8")),
                    annotations=[dict(
                        text="Algos",
                        x=0.5, y=0.5,
                        font=dict(size=13, color="#64748b"),
                        showarrow=False
                    )]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("<div style='text-align:center;padding:40px;color:#64748b;'>Upload papers to see trends</div>", unsafe_allow_html=True)
    except Exception as e:
        error_banner(f"Error: {e}")

divider()

col1, col2 = st.columns(2)

try:
    response = requests.get(f"{API_URL}/analytics/research-trends")
    if response.status_code == 200:
        trends = response.json()

        with col1:
            section_header("Top Evaluation Metrics")
            top_metrics = trends.get("top_metrics", {})
            if top_metrics:
                df = pd.DataFrame(top_metrics.items(), columns=["Metric", "Count"]).sort_values("Count")
                fig = go.Figure(go.Bar(
                    x=df["Count"], y=df["Metric"],
                    orientation="h",
                    marker=dict(color="#00d4aa", line_width=0)
                ))
                fig = plotly_dark_layout(fig, height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("<div style='color:#64748b;font-size:0.85rem;'>No metric data yet</div>", unsafe_allow_html=True)

        with col2:
            section_header("Referenced Datasets")
            top_datasets = trends.get("top_datasets", {})
            if top_datasets:
                df = pd.DataFrame(top_datasets.items(), columns=["Dataset", "Count"]).sort_values("Count")
                fig = go.Figure(go.Bar(
                    x=df["Count"], y=df["Dataset"],
                    orientation="h",
                    marker=dict(color="#f59e0b", line_width=0)
                ))
                fig = plotly_dark_layout(fig, height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("<div style='color:#64748b;font-size:0.85rem;'>No dataset data yet</div>", unsafe_allow_html=True)
except Exception as e:
    error_banner(f"Error: {e}")