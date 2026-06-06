import streamlit as st

st.set_page_config(
    page_title="AI Research Scientist Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# minimal custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    [data-testid="metric-container"] {
        background: #f8f9ff;
        border: 1px solid #e0e4ff;
        border-radius: 8px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🔬 AI Research Scientist Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Literature Analysis & ML Experimentation Platform</div>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### What this platform does
    - 📄 Parses research PDFs and extracts structured knowledge
    - 🔍 Semantic search across all uploaded papers
    - 🕸️ Knowledge graph of papers, algorithms, datasets
    - 🧪 Automated ML experiments on your datasets
    - 📊 Interactive analytics and model comparison
    - 📝 Auto-generated PDF research reports
    """)
with col2:
    st.markdown("""
    ### How to use it
    1. Go to **Upload Papers** → upload research PDFs
    2. Go to **Knowledge Base** → search and explore
    3. Go to **ML Experiments** → upload a dataset and train models
    4. Go to **Analytics** → view trends and comparisons
    5. Go to **Reports** → generate and download PDF report
    """)

st.info("👈 Use the sidebar to navigate between pages.")