import streamlit as st
import requests
import plotly.graph_objects as go
import math
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.ui_helpers import load_css, page_header, section_header, divider, error_banner, plotly_dark_layout

load_css()
API_URL = "http://localhost:8000/api"

page_header("Knowledge Base", "Semantic search and knowledge graph visualization", "🔍")

tabs = st.tabs(["🔎  Semantic Search", "🕸️  Knowledge Graph"])

# ── Tab 1: Search ─────────────────────────────────────────
with tabs[0]:
    section_header("Search Across All Papers", "Powered by Sentence-Transformers + ChromaDB")

    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("Search query", placeholder="e.g. transformer for image classification", label_visibility="collapsed")
    with col2:
        n_results = st.slider("Results", 1, 10, 5, label_visibility="collapsed")

    if query:
        with st.spinner("Searching..."):
            try:
                response = requests.get(f"{API_URL}/knowledge/search", params={"query": query, "n_results": n_results})
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])

                    if not results:
                        st.markdown("""
                        <div style="text-align:center; padding:30px; color:#64748b;">
                            <div style="font-size:2rem;">🔭</div>
                            <div style="margin-top:8px;">No results found. Upload more papers.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='color:#64748b; font-size:0.85rem; margin-bottom:1rem;'>Found <strong style='color:#4C9BE8;'>{len(results)}</strong> results</div>", unsafe_allow_html=True)

                        for r in results:
                            score_color = "#00d4aa" if r["similarity_score"] > 0.7 else "#4C9BE8" if r["similarity_score"] > 0.4 else "#64748b"
                            with st.expander(f"📄  {r['title']}"):
                                st.markdown(f"""
                                <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                                    <span style="background:rgba(76,155,232,0.1); color:{score_color};
                                                 border:1px solid {score_color}; border-radius:20px;
                                                 padding:2px 12px; font-size:0.78rem; font-weight:600;">
                                        {r['similarity_score']} similarity
                                    </span>
                                </div>
                                <div style="color:#94a3b8; font-size:0.88rem; line-height:1.7;
                                            background:#0f1117; border-radius:8px; padding:12px;">
                                    {r['excerpt']}...
                                </div>
                                """, unsafe_allow_html=True)
            except Exception as e:
                error_banner(f"Search failed: {e}")

# ── Tab 2: Knowledge Graph ────────────────────────────────
with tabs[1]:
    section_header("Knowledge Graph", "Relationships between papers, algorithms, datasets, authors")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 Load Graph", type="primary"):
            st.session_state["load_graph"] = True
    with col2:
        try:
            stats_resp = requests.get(f"{API_URL}/knowledge/stats")
            if stats_resp.status_code == 200:
                count = stats_resp.json().get("papers_indexed", 0)
                st.metric("Papers Indexed", count)
        except:
            pass

    if st.session_state.get("load_graph"):
        with st.spinner("Building graph..."):
            try:
                response = requests.get(f"{API_URL}/knowledge/graph")
                if response.status_code == 200:
                    graph_data = response.json()
                    nodes = graph_data["nodes"]
                    edges = graph_data["edges"]

                    if not nodes:
                        st.info("No graph data yet. Upload papers first.")
                    else:
                        color_map = {
                            "paper": "#4C9BE8",
                            "algorithm": "#00d4aa",
                            "dataset": "#f59e0b",
                            "author": "#a855f7"
                        }
                        size_map = {
                            "paper": 16,
                            "algorithm": 12,
                            "dataset": 12,
                            "author": 10
                        }

                        n = len(nodes)
                        pos = {}
                        for i, node in enumerate(nodes):
                            angle = 2 * math.pi * i / n
                            radius = 1 + (0.3 if node["type"] != "paper" else 0)
                            pos[node["id"]] = (radius * math.cos(angle), radius * math.sin(angle))

                        edge_x, edge_y = [], []
                        for edge in edges:
                            x0, y0 = pos.get(edge["source"], (0, 0))
                            x1, y1 = pos.get(edge["target"], (0, 0))
                            edge_x += [x0, x1, None]
                            edge_y += [y0, y1, None]

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=edge_x, y=edge_y, mode="lines",
                            line=dict(width=0.8, color="#2d3154"),
                            hoverinfo="none"
                        ))

                        for node_type in ["paper", "algorithm", "dataset", "author"]:
                            type_nodes = [n for n in nodes if n["type"] == node_type]
                            if not type_nodes:
                                continue
                            nx_vals = [pos[n["id"]][0] for n in type_nodes]
                            ny_vals = [pos[n["id"]][1] for n in type_nodes]
                            labels = [n["label"] for n in type_nodes]

                            fig.add_trace(go.Scatter(
                                x=nx_vals, y=ny_vals,
                                mode="markers+text",
                                name=node_type.title(),
                                marker=dict(
                                    size=size_map[node_type],
                                    color=color_map[node_type],
                                    line=dict(width=1.5, color="#0f1117")
                                ),
                                text=labels,
                                textposition="top center",
                                textfont=dict(size=9, color="#94a3b8"),
                                hoverinfo="text"
                            ))

                        fig = plotly_dark_layout(fig, height=550)
                        fig.update_layout(
                            showlegend=True,
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        c1, c2, c3 = st.columns(3)
                        c1.metric("Total Nodes", graph_data["total_nodes"])
                        c2.metric("Total Edges", graph_data["total_edges"])
                        c3.metric("Node Types", len(set(n["type"] for n in nodes)))
            except Exception as e:
                error_banner(f"Failed to load graph: {e}")