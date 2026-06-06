# upload_papers.py — Streamlit page for uploading and viewing research papers
import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000/api"

st.title("📄 Research Paper Upload & Analysis")
st.markdown("---")

# ── Upload Section ──────────────────────────────────────────
st.subheader("Upload Research Papers")

uploaded_files = st.file_uploader(
    "Upload PDF research papers",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f"Processing {uploaded_file.name}..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/papers/upload", files=files)

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ **{data['title']}** uploaded successfully!")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Algorithms Found:**")
                        for algo in (data.get("algorithms_found") or []):
                            st.markdown(f"- {algo}")
                    with col2:
                        st.markdown("**Datasets Found:**")
                        for ds in (data.get("datasets_found") or []):
                            st.markdown(f"- {ds}")
                else:
                    st.error(f"❌ Failed: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Error connecting to API: {e}")

st.markdown("---")

# ── All Papers Section ───────────────────────────────────────
st.subheader("📚 Uploaded Papers")

try:
    response = requests.get(f"{API_URL}/papers/")
    if response.status_code == 200:
        papers = response.json()

        if not papers:
            st.info("No papers uploaded yet. Upload some PDFs above.")
        else:
            st.markdown(f"**Total papers: {len(papers)}**")

            for paper in papers:
                with st.expander(f"📖 {paper['title']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Authors:** {', '.join(paper.get('authors') or ['Unknown'])}")
                        st.markdown(f"**Keywords:** {', '.join(paper.get('keywords') or ['None'])}")
                    with col2:
                        st.markdown(f"**Algorithms:** {', '.join(paper.get('algorithms_used') or ['None found'])}")
                        st.markdown(f"**Datasets:** {', '.join(paper.get('datasets_used') or ['None found'])}")

                    if st.button(f"🗑️ Delete", key=f"del_{paper['id']}"):
                        del_response = requests.delete(f"{API_URL}/papers/{paper['id']}")
                        if del_response.status_code == 200:
                            st.success("Deleted!")
                            st.rerun()
except Exception as e:
    st.error(f"Cannot connect to API. Is the backend running? Error: {e}")

st.markdown("---")

# ── Research Gap Analysis ────────────────────────────────────
st.subheader("🔍 Research Gap Analysis")

if st.button("Analyze Research Gaps"):
    with st.spinner("Analyzing all papers..."):
        try:
            response = requests.get(f"{API_URL}/papers/gaps")
            if response.status_code == 200:
                gaps = response.json()

                if "message" in gaps:
                    st.info(gaps["message"])
                else:
                    st.markdown(f"**Analyzed {gaps['total_papers']} papers**")

                    st.markdown("### 💡 Key Insights")
                    for insight in gaps.get("gap_insights", []):
                        st.info(insight)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Algorithm Frequency**")
                        if gaps.get("algorithm_frequency"):
                            df = pd.DataFrame(
                                gaps["algorithm_frequency"].items(),
                                columns=["Algorithm", "Count"]
                            ).sort_values("Count", ascending=False)
                            st.dataframe(df, use_container_width=True)

                    with col2:
                        st.markdown("**Metric Frequency**")
                        if gaps.get("metric_frequency"):
                            df = pd.DataFrame(
                                gaps["metric_frequency"].items(),
                                columns=["Metric", "Count"]
                            ).sort_values("Count", ascending=False)
                            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")