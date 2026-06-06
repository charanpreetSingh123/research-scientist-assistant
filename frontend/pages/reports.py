import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

st.title("📝 Report Generator")
st.markdown("---")

st.subheader("Generate PDF Report from Experiment")

# fetch all experiments
try:
    response = requests.get(f"{API_URL}/experiments/")
    if response.status_code == 200:
        experiments = response.json()
        completed = [e for e in experiments if e["status"] == "complete"]

        if not completed:
            st.info("No completed experiments yet. Run an experiment first from the ML Experiments page.")
        else:
            options = {f"{e['name']} ({e['dataset']})": e["id"] for e in completed}
            selected_label = st.selectbox("Select experiment", list(options.keys()))
            selected_id = options[selected_label]

            selected_exp = next(e for e in completed if e["id"] == selected_id)

            col1, col2, col3 = st.columns(3)
            col1.metric("Problem Type", selected_exp["problem_type"] or "N/A")
            col2.metric("Best Model", selected_exp["best_model"] or "N/A")
            col3.metric("Best Score", round(selected_exp["best_score"] or 0, 4))

            st.markdown("---")

            col_gen, col_dl = st.columns(2)

            with col_gen:
                if st.button("📄 Generate Report", type="primary"):
                    with st.spinner("Generating PDF report..."):
                        try:
                            response = requests.post(f"{API_URL}/reports/generate/{selected_id}")
                            if response.status_code == 200:
                                st.success("✅ Report generated successfully!")
                                st.session_state["report_ready"] = selected_id
                            else:
                                st.error(response.json().get("detail", "Generation failed"))
                        except Exception as e:
                            st.error(f"Error: {e}")

            with col_dl:
                report_ready_id = st.session_state.get("report_ready")
                if report_ready_id == selected_id:
                    try:
                        dl_response = requests.get(
                            f"{API_URL}/reports/download/{selected_id}"
                        )
                        if dl_response.status_code == 200:
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=dl_response.content,
                                file_name=f"report_{selected_exp['name'][:20]}.pdf",
                                mime="application/pdf",
                                type="primary"
                            )
                    except Exception as e:
                        st.error(f"Download error: {e}")

except Exception as e:
    st.error(f"Cannot connect to API: {e}")

st.markdown("---")
st.subheader("📚 All Generated Reports")

try:
    response = requests.get(f"{API_URL}/experiments/")
    if response.status_code == 200:
        experiments = response.json()
        with_reports = [e for e in experiments if e.get("status") == "complete"]

        if not with_reports:
            st.info("No reports yet.")
        else:
            for exp in with_reports:
                with st.expander(f"📄 {exp['name']} — {exp['dataset']}"):
                    col1, col2 = st.columns(2)
                    col1.write(f"**Best Model:** {exp['best_model']}")
                    col2.write(f"**Score:** {round(exp['best_score'] or 0, 4)}")

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
                        if st.button("Generate Report", key=f"gen_{exp['id']}"):
                            requests.post(f"{API_URL}/reports/generate/{exp['id']}")
                            st.rerun()
except Exception as e:
    st.error(f"Error: {e}")