import streamlit as st
import requests
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.ui_helpers import load_css, page_header, section_header, tags_row, divider, success_banner, error_banner

load_css()
API_URL = "http://localhost:8000/api"

page_header("Upload Papers", "Parse research PDFs and extract structured knowledge", "📄")

tabs = st.tabs(["⬆️  Upload", "📚  All Papers", "🔎  Gap Analysis"])

# ── Tab 1: Upload ─────────────────────────────────────────
with tabs[0]:
    section_header("Upload Research PDFs", "Supports single or multiple papers at once")

    uploaded_files = st.file_uploader(
        "Drop PDF files here or click to browse",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{API_URL}/papers/upload", files=files)

                    if response.status_code == 200:
                        data = response.json()
                        success_banner(f"{data['title']} uploaded successfully")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Algorithms detected**")
                            tags_row(data.get("algorithms_found") or ["None found"], "blue")
                        with col2:
                            st.markdown("**Datasets detected**")
                            tags_row(data.get("datasets_found") or ["None found"], "green")
                    else:
                        error_banner(response.json().get("detail", "Upload failed"))
                except Exception as e:
                    error_banner(f"Cannot connect to API: {e}")

# ── Tab 2: All Papers ─────────────────────────────────────
with tabs[1]:
    try:
        response = requests.get(f"{API_URL}/papers/")
        if response.status_code == 200:
            papers = response.json()

            if not papers:
                st.markdown("""
                <div style="text-align:center; padding:40px; color:#64748b;">
                    <div style="font-size:3rem; margin-bottom:12px;">📭</div>
                    <div style="font-size:1rem; font-weight:600;">No papers yet</div>
                    <div style="font-size:0.85rem; margin-top:4px;">Upload PDFs in the Upload tab</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="margin-bottom:1rem;">
                    <span style="font-size:0.85rem; color:#64748b;">
                        Showing <strong style="color:#4C9BE8;">{len(papers)}</strong> papers
                    </span>
                </div>
                """, unsafe_allow_html=True)

                for paper in papers:
                    with st.expander(f"📖  {paper['title']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Authors**")
                            st.markdown(f"<span style='color:#94a3b8'>{', '.join(paper.get('authors') or ['Unknown'])}</span>", unsafe_allow_html=True)
                            st.markdown(f"**Keywords**")
                            tags_row(paper.get("keywords") or ["None"], "amber")
                        with col2:
                            st.markdown("**Algorithms**")
                            tags_row(paper.get("algorithms_used") or ["None found"], "blue")
                            st.markdown("**Datasets**")
                            tags_row(paper.get("datasets_used") or ["None found"], "green")

                        if st.button("🗑️ Delete paper", key=f"del_{paper['id']}"):
                            del_resp = requests.delete(f"{API_URL}/papers/{paper['id']}")
                            if del_resp.status_code == 200:
                                st.rerun()
    except Exception as e:
        error_banner(f"Cannot connect to API: {e}")

# ── Tab 3: Gap Analysis ───────────────────────────────────
with tabs[2]:
    section_header("Research Gap Detection", "Analyze all papers to find underexplored areas")

    if st.button("🔍 Run Gap Analysis", type="primary"):
        with st.spinner("Analyzing all papers..."):
            try:
                response = requests.get(f"{API_URL}/papers/gaps")
                if response.status_code == 200:
                    gaps = response.json()

                    if "message" in gaps:
                        st.info(gaps["message"])
                    else:
                        st.markdown(f"""
                        <div style="font-size:0.9rem; color:#64748b; margin-bottom:1rem;">
                            Analyzed <strong style="color:#e2e8f0;">{gaps['total_papers']}</strong> papers
                        </div>
                        """, unsafe_allow_html=True)

                        for insight in gaps.get("gap_insights", []):
                            st.markdown(f"""
                            <div style="
                                background: rgba(76,155,232,0.08);
                                border-left: 4px solid #4C9BE8;
                                border-radius: 8px;
                                padding: 14px 18px;
                                margin-bottom: 10px;
                                color: #94a3b8;
                                font-size: 0.9rem;
                                line-height: 1.6;
                            ">💡 {insight}</div>
                            """, unsafe_allow_html=True)

                        col1, col2 = st.columns(2)
                        with col1:
                            if gaps.get("algorithm_frequency"):
                                section_header("Algorithm Frequency")
                                df = pd.DataFrame(gaps["algorithm_frequency"].items(), columns=["Algorithm", "Count"])
                                st.dataframe(df.sort_values("Count", ascending=False), use_container_width=True)
                        with col2:
                            if gaps.get("metric_frequency"):
                                section_header("Metric Frequency")
                                df = pd.DataFrame(gaps["metric_frequency"].items(), columns=["Metric", "Count"])
                                st.dataframe(df.sort_values("Count", ascending=False), use_container_width=True)
            except Exception as e:
                error_banner(f"Error: {e}")