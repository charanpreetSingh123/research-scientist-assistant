import streamlit as st
import requests
import plotly.graph_objects as go

API_URL = "http://localhost:8000/api"

st.title("🔍 Knowledge Base & Semantic Search")
st.markdown("---")

# search bar
st.subheader("Semantic Search")
query = st.text_input("Search across all uploaded papers", placeholder="e.g. transformer for image classification")

col1, col2 = st.columns([3, 1])
with col2:
    n_results = st.slider("Results", 1, 10, 5)

if query:
    with st.spinner("Searching..."):
        try:
            response = requests.get(
                f"{API_URL}/knowledge/search",
                params={"query": query, "n_results": n_results}
            )
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                if not results:
                    st.info("No results found. Upload more papers to improve search.")
                else:
                    st.markdown(f"**{len(results)} results found**")
                    for r in results:
                        with st.expander(f"📄 {r['title']} — similarity: {r['similarity_score']}"):
                            st.write(r["excerpt"])
        except Exception as e:
            st.error(f"Search failed: {e}")

st.markdown("---")

# knowledge graph viz
st.subheader("🕸️ Knowledge Graph")

if st.button("Load Knowledge Graph"):
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
                    # color by node type
                    color_map = {
                        "paper": "#4C9BE8",
                        "algorithm": "#E8834C",
                        "dataset": "#4CE87A",
                        "author": "#C44CE8"
                    }

                    # simple spring layout using node index positions
                    import math
                    n = len(nodes)
                    pos = {}
                    for i, node in enumerate(nodes):
                        angle = 2 * math.pi * i / n
                        pos[node["id"]] = (math.cos(angle), math.sin(angle))

                    edge_x, edge_y = [], []
                    for edge in edges:
                        x0, y0 = pos.get(edge["source"], (0, 0))
                        x1, y1 = pos.get(edge["target"], (0, 0))
                        edge_x += [x0, x1, None]
                        edge_y += [y0, y1, None]

                    node_x = [pos[n["id"]][0] for n in nodes]
                    node_y = [pos[n["id"]][1] for n in nodes]
                    node_colors = [color_map.get(n["type"], "#888") for n in nodes]
                    node_labels = [n["label"] for n in nodes]

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=edge_x, y=edge_y,
                        mode="lines",
                        line=dict(width=0.8, color="#888"),
                        hoverinfo="none"
                    ))
                    fig.add_trace(go.Scatter(
                        x=node_x, y=node_y,
                        mode="markers+text",
                        marker=dict(size=12, color=node_colors),
                        text=node_labels,
                        textposition="top center",
                        hoverinfo="text"
                    ))
                    fig.update_layout(
                        showlegend=False,
                        height=500,
                        margin=dict(l=0, r=0, t=0, b=0)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown(f"**{graph_data['total_nodes']} nodes · {graph_data['total_edges']} edges**")
        except Exception as e:
            st.error(f"Failed to load graph: {e}")