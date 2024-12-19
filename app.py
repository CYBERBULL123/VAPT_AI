import streamlit as st
from backend.langchain_utils import generate_report
from backend.report import generate_html_report
import time

# Set up the page configuration
st.set_page_config(
    page_title="🛡️ Cybersecurity Report Generator",
    page_icon="🛡️",
    layout="wide"
)

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("frontend/assests/style.css")

# Function to render README content
def render_readme():
    with open('README.md', 'r') as f:
        readme_content = f.read()
    st.markdown(readme_content, unsafe_allow_html=True)
    # Wait for user input to proceed
    if st.button('Start Cybersecurity Report Generator'):
        # Set session state to true to indicate the button was clicked
        st.session_state.started = True
        # Rerun the app to load the main program
        st.rerun()

# Function to render the main app with better UX and advanced layout
def render_main_app():
    st.title("🛡️ **Advanced Cybersecurity Report Generator**")
    st.divider()

    # Using tabs with proper emojis
    tabs = st.radio(
        "",
        ("🛡️ VAPT", "🔐 Pentesting", "⚠️ Incident Response Plan", "✅ Compliance", "📊 Risk Assessment"),
        index=0,
        horizontal=True
    )
    
    st.divider()

    # Report forms based on selected tab
    if tabs == "🛡️ VAPT":
        with st.form("vapt_form"):
            with st.expander("1. General Information", expanded=True):
                project_name = st.text_input("Project Name", placeholder="Enter project name")
                client_name = st.text_input("Client Name", placeholder="Enter client name")
                assessment_date = st.date_input("Assessment Date")
                assessor_name = st.text_input("Assessor Name", placeholder="Enter assessor name")

            with st.expander("2. Findings", expanded=False):
                high_level_findings = st.text_area("High-Level Findings", placeholder="Enter high-level findings")
                detailed_findings = st.text_area("Detailed Findings", placeholder="Enter detailed findings")

            with st.expander("3. Risk Analysis", expanded=False):
                risk_description = st.text_area("Risk Description", placeholder="Enter risk description")
                business_impact = st.text_area("Business Impact", placeholder="Enter business impact")

            with st.expander("4. Recommendations", expanded=False):
                mitigation_strategies = st.text_area("Mitigation Strategies", placeholder="Enter mitigation strategies")
                additional_notes = st.text_area("Additional Notes", placeholder="Enter additional notes")

            submitted = st.form_submit_button("Generate VAPT Report")

    elif tabs == "🔐 Pentesting":
        with st.form("pentest_form"):
            with st.expander("1. General Information", expanded=True):
                project_name = st.text_input("Project Name", placeholder="Enter project name")
                client_name = st.text_input("Client Name", placeholder="Enter client name")
                assessment_date = st.date_input("Assessment Date")
                assessor_name = st.text_input("Assessor Name", placeholder="Enter assessor name")

            with st.expander("2. Findings", expanded=False):
                high_level_findings = st.text_area("High-Level Findings", placeholder="Enter high-level findings")
                detailed_findings = st.text_area("Detailed Findings", placeholder="Enter detailed findings")

            with st.expander("3. Exploitation Details", expanded=False):
                tools_used = st.text_area("Tools Used", placeholder="List the tools used")
                steps_taken = st.text_area("Steps Taken", placeholder="Describe the exploitation process")

            with st.expander("4. Recommendations", expanded=False):
                mitigation_strategies = st.text_area("Mitigation Strategies", placeholder="Enter mitigation strategies")
                additional_notes = st.text_area("Additional Notes", placeholder="Enter additional notes")

            submitted = st.form_submit_button("Generate Pentest Report")

    elif tabs == "⚠️ Incident Response Plan":
        with st.form("incident_response_form"):
            with st.expander("1. Incident Details", expanded=True):
                incident_name = st.text_input("Incident Name", placeholder="Enter incident name")
                incident_date = st.date_input("Incident Date")
                incident_description = st.text_area("Incident Description", placeholder="Describe the incident")

            with st.expander("2. Actions Taken", expanded=False):
                actions_taken = st.text_area("Actions Taken", placeholder="Describe actions taken to mitigate the incident")

            with st.expander("3. Lessons Learned", expanded=False):
                lessons_learned = st.text_area("Lessons Learned", placeholder="Outline the lessons learned")

            with st.expander("4. Recommendations", expanded=False):
                future_prevention = st.text_area("Future Prevention Strategies", placeholder="Describe strategies to prevent future incidents")

            submitted = st.form_submit_button("Generate Incident Response Plan")

    elif tabs == "✅ Compliance":
        with st.form("compliance_form"):
            with st.expander("1. General Information", expanded=True):
                project_name = st.text_input("Project Name", placeholder="Enter project name")
                client_name = st.text_input("Client Name", placeholder="Enter client name")
                assessment_date = st.date_input("Assessment Date")
                compliance_type = st.text_input("Compliance Type", placeholder="Enter compliance type (e.g., ISO, PCI DSS)")

            with st.expander("2. Compliance Findings", expanded=False):
                compliance_findings = st.text_area("Compliance Findings", placeholder="Enter compliance findings")

            with st.expander("3. Recommendations", expanded=False):
                compliance_recommendations = st.text_area("Recommendations", placeholder="Enter recommendations to meet compliance")

            submitted = st.form_submit_button("Generate Compliance Report")

    elif tabs == "📊 Risk Assessment":
        with st.form("risk_assessment_form"):
            with st.expander("1. General Information", expanded=True):
                project_name = st.text_input("Project Name", placeholder="Enter project name")
                client_name = st.text_input("Client Name", placeholder="Enter client name")
                assessment_date = st.date_input("Assessment Date")

            with st.expander("2. Risk Details", expanded=False):
                risks_identified = st.text_area("Risks Identified", placeholder="List the risks identified")
                risk_severity = st.text_area("Risk Severity", placeholder="Describe the severity of the risks")

            with st.expander("3. Mitigation Plan", expanded=False):
                risk_mitigation_plan = st.text_area("Risk Mitigation Plan", placeholder="Enter the mitigation plan for risks")

            submitted = st.form_submit_button("Generate Risk Assessment Report")

    # Handle report generation
    if submitted:
        with st.spinner("Generating your report... ⏳"):
                time.sleep(2)
                st.progress(100)  
        try:
            if tabs == "VAPT":
                data = {
                    "project_name": project_name,
                    "client_name": client_name,
                    "assessment_date": str(assessment_date),
                    "assessor_name": assessor_name,
                    "findings": f"{high_level_findings}\n\n{detailed_findings}", 
                    "risk_description": risk_description,
                    "business_impact": business_impact,
                    "mitigation_strategies": mitigation_strategies,
                    "additional_notes": additional_notes,
                }
            elif tabs == "Pentesting":
                data = {
                    "project_name": project_name,
                    "client_name": client_name,
                    "assessment_date": str(assessment_date),
                    "assessor_name": assessor_name,
                    "findings": f"{high_level_findings}\n\n{detailed_findings}", 
                    "tools_used": tools_used,
                    "steps_taken": steps_taken,
                    "mitigation_strategies": mitigation_strategies,
                    "additional_notes": additional_notes,
                }
            elif tabs == "Incident Response Plan":
                data = {
                    "incident_name": incident_name,
                    "incident_date": str(incident_date),
                    "incident_description": incident_description,
                    "actions_taken": actions_taken,
                    "lessons_learned": lessons_learned,
                    "future_prevention": future_prevention,
                }
            elif tabs == "Compliance":
                data = {
                    "project_name": project_name,
                    "client_name": client_name,
                    "assessment_date": str(assessment_date),
                    "compliance_type": compliance_type,
                    "compliance_findings": compliance_findings,
                    "compliance_recommendations": compliance_recommendations,
                }
            elif tabs == "Risk Assessment":
                data = {
                    "project_name": project_name,
                    "client_name": client_name,
                    "assessment_date": str(assessment_date),
                    "risks_identified": risks_identified,
                    "risk_severity": risk_severity,
                    "risk_mitigation_plan": risk_mitigation_plan,
                }

            # Generate the report
            report_content = generate_report(tabs, data)

            # Generate HTML report
            template_file = f"backend/templates/{tabs.lower().replace(' ', '_')}_template.html"
            html_content = generate_html_report(data, template_file)

            # Display the report in Markdown format
            st.markdown("### Generated Report (Preview):")
            markdown_content = f"""
            ## {tabs} Report for {data.get('project_name', data.get('incident_name', 'Unnamed Project'))}

            **Client Name:** {data.get('client_name', 'N/A')}  
            **Assessment Date:** {data.get('assessment_date', 'N/A')}  
            **Assessor Name:** {data.get('assessor_name', 'N/A')}  

            ##### High-Level Findings:
            {data.get('high_level_findings', 'No high-level findings provided.')}

            ##### Detailed Findings:
            {data.get('detailed_findings', 'No detailed findings provided.')}

            ##### Risk Analysis:
            **Risk Description:** {data.get('risk_description', 'No risk description provided.')}  
            **Business Impact:** {data.get('business_impact', 'No business impact provided.')}

            ##### Recommendations:
            **Mitigation Strategies:** {data.get('mitigation_strategies', 'No mitigation strategies provided.')}  
            **Additional Notes:** {data.get('additional_notes', 'No additional notes provided.')}

            ##### Tools and Steps (For Pentesting):
            **Tools Used:** {data.get('tools_used', 'N/A')}  
            **Steps Taken:** {data.get('steps_taken', 'N/A')}

            ##### Incident Details (For Incident Response):
            **Incident Name:** {data.get('incident_name', 'N/A')}  
            **Incident Date:** {data.get('incident_date', 'N/A')}  
            **Incident Description:** {data.get('incident_description', 'N/A')}  
            **Actions Taken:** {data.get('actions_taken', 'N/A')}  
            **Lessons Learned:** {data.get('lessons_learned', 'N/A')}  
            **Future Prevention:** {data.get('future_prevention', 'N/A')}
            """
            st.markdown(markdown_content)

            # Download option
            st.download_button(
                label="📥 Download Report HTML",
                data=html_content,
                file_name=f"{data.get('project_name', data.get('incident_name', 'report'))}_report.html",
                mime="text/html"
            )

            st.success(f"{tabs} Report for '{data.get('project_name', data.get('incident_name', 'Unnamed Project'))}' generated successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Main Streamlit app logic
def main():
    # Initialize session state if not already set
    if 'started' not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started:
        # Display the README first
        render_readme()
    else:
        # Render the main app if the button was clicked
        render_main_app()

if __name__ == "__main__":
    main()