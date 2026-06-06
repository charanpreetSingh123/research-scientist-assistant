import streamlit as st
import requests
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.ui_helpers import load_css, page_header, section_header, divider, success_banner, error_banner

load_css()
API_URL = "http://localhost:8000/api"

page_header("Report Generator", "Auto-generate structured PDF research reports", "📝")

section_header("Generate from Experiment", "Select a completed experiment to build a report")

try:
    response = requests.get(f"{API_URL}/experiments/")
    if response.status_code == 200:
        experiments = response.json()
        completed = [e for e in experiments if e["status"] == "complete"]

        if not completed:
            st.markdown("""
            <div style="text-align:center; padding:60px; color:#64748b;">
                <div style="font-size:3rem;">📭</div>
                <div style="font-size:1rem; font-weight:600; margin-top:12px;">No completed experiments</div>
                <div style="font-size:0.85rem; margin-top:4px;">Run an experiment first from the ML Experiments page</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            options = {f"{e['name']}  ·  {e['dataset']}": e["id"] for e in completed}
            selected_label = st.selectbox("Select experiment", list(options.keys()), label_visibility="collapsed")
            selected_id = options[selected_label]
            selected_exp = next(e for e in completed if e["id"] == selected_id)

            st.markdown(f"""
            <div style="
                background: #1a1d2e;
                border: 1px solid #2d3154;
                border-radius: 12px;
                padding: 20px 24px;
                margin: 1rem 0;
                display: flex;
                gap: 40px;
            ">
                <div>
                    <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase;
                                letter-spacing:0.06em; margin-bottom:4px;">Problem Type</div>
                    <div style="font-size:1.1rem; font-weight:700; color:#4C9BE8;">
                        {selected_exp['problem_type'] or 'N/A'}
                    </div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase;
                                letter-spacing:0.06em; margin-bottom:4px;">Best Model</div>
                    <div style="font-size:1.1rem; font-weight:700; color:#00d4aa;">
                        {selected_exp['best_model'] or 'N/A'}
                    </div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase;
                                letter-spacing:0.06em; margin-bottom:4px;">Best Score</div>
                    <div style="font-size:1.1rem; font-weight:700; color:#f59e0b;">
                        {round(selected_exp['best_score'] or 0, 4)}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("📄 Generate PDF Report", type="primary"):
                    with st.spinner("Building report..."):
                        try:
                            response = requests.post(f"{API_URL}/reports/generate/{selected_id}")
                            if response.status_code == 200:
                                success_banner("Report generated successfully")
                                st.session_state["report_ready"] = selected_id
                            else:
                                error_banner(response.json().get("detail", "Generation failed"))
                        except Exception as e:
                            error_banner(f"Error: {e}")

            with col2:
                if st.session_state.get("report_ready") == selected_id:
                    try:
                        dl_response = requests.get(f"{API_URL}/reports/download/{selected_id}")
                        if dl_response.status_code == 200:
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=dl_response.content,
                                file_name=f"report_{selected_exp['name'][:20]}.pdf",
                                mime="application/pdf",
                                type="primary"
                            )
                    except Exception as e:
                        error_banner(f"Download error: {e}")

        divider()
        section_header("All Reports")

        with_reports = [e for e in experiments if e.get("status") == "complete"]
        if not with_reports:
            st.markdown("<div style='color:#64748b; font-size:0.85rem;'>No reports yet</div>", unsafe_allow_html=True)
        else:
            for exp in with_reports:
                with st.expander(f"📄  {exp['name']}  ·  {exp['dataset']}"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Best Model", exp["best_model"] or "N/A")
                    c2.metric("Score", round(exp["best_score"] or 0, 4))
                    c3.metric("Type", exp["problem_type"] or "N/A")

                    dl_response = requests.get(f"{API_URL}/reports/download/{exp['id']}")
                    if dl_response.status_code == 200:
                        st.download_button(
                            label="⬇️ Download Report",
                            data=dl_response.content,
                            file_name=f"report_{exp['name'][:20]}.pdf",
                            mime="application/pdf",
                            key=f"dl_{exp['id']}"
                        )
                    else:
                        if st.button("Generate", key=f"gen_{exp['id']}"):
                            requests.post(f"{API_URL}/reports/generate/{exp['id']}")
                            st.rerun()

except Exception as e:
    error_banner(f"Cannot connect to API: {e}")