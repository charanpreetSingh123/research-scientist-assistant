import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils.ui_helpers import load_css

st.set_page_config(
    page_title="AI Research Scientist Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# sidebar branding
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem 0; border-bottom: 1px solid #2d3154; margin-bottom: 1rem;">
        <div style="font-size:1.3rem; font-weight:800; color:#e2e8f0; letter-spacing:-0.02em;">
            🔬 ResearchAI
        </div>
        <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">
            v1.0.0 · All systems running
        </div>
    </div>
    <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase;
                letter-spacing:0.1em; font-weight:600; margin-bottom:8px;">
        Navigation
    </div>
    """, unsafe_allow_html=True)

# hero section
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1a1d2e 0%, #1e2235 50%, #1a2540 100%);
    border: 1px solid #2d3154;
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute; top: -40px; right: -40px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(76,155,232,0.08) 0%, transparent 70%);
        border-radius: 50%;
    "></div>
    <div style="
        position: absolute; bottom: -30px; left: 30%;
        width: 150px; height: 150px;
        background: radial-gradient(circle, rgba(0,212,170,0.06) 0%, transparent 70%);
        border-radius: 50%;
    "></div>
    <div style="font-size:0.8rem; color:#4C9BE8; font-weight:600;
                text-transform:uppercase; letter-spacing:0.1em; margin-bottom:12px;">
        AI-Powered Platform
    </div>
    <div style="font-size:2.4rem; font-weight:800; color:#e2e8f0;
                letter-spacing:-0.03em; line-height:1.2; margin-bottom:12px;">
        Research Scientist Assistant
    </div>
    <div style="font-size:1rem; color:#64748b; max-width:600px; line-height:1.7;">
        Automated literature analysis, knowledge extraction, and ML experimentation.
        From raw research papers to actionable insights — in one platform.
    </div>
    <div style="margin-top:24px; display:flex; gap:12px; flex-wrap:wrap;">
        <span style="background:rgba(76,155,232,0.15); color:#4C9BE8;
                     border:1px solid rgba(76,155,232,0.3); border-radius:20px;
                     padding:4px 14px; font-size:0.8rem; font-weight:500;">
            🧠 NLP Pipeline
        </span>
        <span style="background:rgba(0,212,170,0.15); color:#00d4aa;
                     border:1px solid rgba(0,212,170,0.3); border-radius:20px;
                     padding:4px 14px; font-size:0.8rem; font-weight:500;">
            ⚡ Auto ML
        </span>
        <span style="background:rgba(245,158,11,0.15); color:#f59e0b;
                     border:1px solid rgba(245,158,11,0.3); border-radius:20px;
                     padding:4px 14px; font-size:0.8rem; font-weight:500;">
            📊 Knowledge Graph
        </span>
        <span style="background:rgba(168,85,247,0.15); color:#a855f7;
                     border:1px solid rgba(168,85,247,0.3); border-radius:20px;
                     padding:4px 14px; font-size:0.8rem; font-weight:500;">
            📝 PDF Reports
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# feature cards
col1, col2, col3, col4 = st.columns(4)

features = [
    ("📄", "Paper Ingestion", "Upload PDFs, auto-extract algorithms, datasets, metrics", "#4C9BE8"),
    ("🔍", "Semantic Search", "Vector search across all papers using embeddings", "#00d4aa"),
    ("🧪", "ML Engine", "Train 6+ models automatically, compare and explain", "#f59e0b"),
    ("📊", "Analytics", "Interactive dashboards, trends, knowledge graph", "#a855f7"),
]

for col, (icon, title, desc, color) in zip([col1, col2, col3, col4], features):
    with col:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1a1d2e, #1e2235);
            border: 1px solid #2d3154;
            border-top: 3px solid {color};
            border-radius: 12px;
            padding: 20px;
            height: 140px;
            transition: all 0.3s ease;
        ">
            <div style="font-size:1.6rem; margin-bottom:8px;">{icon}</div>
            <div style="font-size:0.95rem; font-weight:700;
                        color:#e2e8f0; margin-bottom:6px;">{title}</div>
            <div style="font-size:0.78rem; color:#64748b; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

# quick start guide
st.markdown("""
<div style="
    background: #1a1d2e;
    border: 1px solid #2d3154;
    border-radius: 12px;
    padding: 24px 28px;
">
    <div style="font-size:1rem; font-weight:700; color:#e2e8f0; margin-bottom:16px;">
        🚀 Quick Start Guide
    </div>
    <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:12px;">
""", unsafe_allow_html=True)

steps = [
    ("1", "Upload Papers", "Go to Upload Papers, add research PDFs"),
    ("2", "Search Knowledge", "Use Knowledge Base to search semantically"),
    ("3", "Run Experiment", "Upload a CSV, pick target, train models"),
    ("4", "View Analytics", "Check dashboards and model comparisons"),
    ("5", "Get Report", "Generate and download your PDF report"),
]

cols = st.columns(5)
for col, (num, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div style="
            background: #0f1117;
            border: 1px solid #2d3154;
            border-radius: 10px;
            padding: 16px;
            text-align: center;
        ">
            <div style="
                width: 28px; height: 28px;
                background: linear-gradient(135deg, #4C9BE8, #3b82f6);
                border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.8rem; font-weight: 700; color: white;
                margin: 0 auto 10px auto;
            ">{num}</div>
            <div style="font-size:0.85rem; font-weight:600;
                        color:#e2e8f0; margin-bottom:4px;">{title}</div>
            <div style="font-size:0.75rem; color:#64748b; line-height:1.4;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)