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
    with open('info.md', 'r', encoding="utf-8") as f:
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
                project_name = st.text_input("Project Name", value="ACME Corp Web Application VAPT")
                client_name = st.text_input("Client Name", value="ACME Corporation")
                assessment_date = st.date_input("Assessment Date")
                assessor_name = st.text_input("Assessor Name", value="John Smith")

            with st.expander("2. Findings", expanded=False):
                high_level_findings = st.text_area(
                    "High-Level Findings",
                    value=(
                        "- Multiple input validation vulnerabilities identified.\n"
                        "- Weak password policy enforcement.\n"
                        "- Outdated third-party dependencies with known vulnerabilities."
                    ),
                )
                detailed_findings = st.text_area(
                    "Detailed Findings",
                    value=(
                        "1. **SQL Injection** on login page allowing unauthorized access.\n"
                        "   - Exploit: SQL payload bypassed authentication.\n"
                        "   - Impact: Access to sensitive user data.\n\n"
                        "2. **Cross-Site Scripting (XSS)** in search functionality.\n"
                        "   - Exploit: JavaScript injection into browser context.\n"
                        "   - Impact: Potential session hijacking.\n\n"
                        "3. **Unpatched Apache Server** (CVE-2023-4567).\n"
                        "   - Impact: Exploitable remote code execution vulnerability."
                    ),
                )

            with st.expander("3. Risk Analysis", expanded=False):
                risk_description = st.text_area(
                    "Risk Description",
                    value=(
                        "Exploitation of identified vulnerabilities could lead to:\n"
                        "- Data breaches.\n"
                        "- Financial loss due to reputation damage.\n"
                        "- Non-compliance with regulatory requirements."
                    ),
                )
                business_impact = st.text_area(
                    "Business Impact",
                    value=(
                        "- Compromise of customer data leading to loss of trust.\n"
                        "- Potential fines under GDPR for data exposure.\n"
                        "- Risk of operational downtime due to exploitation."
                    ),
                )

            with st.expander("4. Recommendations", expanded=False):
                mitigation_strategies = st.text_area(
                    "Mitigation Strategies",
                    value=(
                        "- Implement input validation and parameterized queries.\n"
                        "- Apply patches to outdated software and dependencies.\n"
                        "- Enforce strong password policies and multifactor authentication."
                    ),
                )
                additional_notes = st.text_area(
                    "Additional Notes",
                    value="Ensure regular vulnerability scans and patch management.",
                )

            submitted = st.form_submit_button("Generate VAPT Report")

    elif tabs == "🔐 Pentesting":
        with st.form("pentest_form"):
            with st.expander("1. General Information", expanded=True):
                project_name = st.text_input("Project Name", value="ACME External Pentest")
                client_name = st.text_input("Client Name", value="ACME Corporation")
                assessment_date = st.date_input("Assessment Date")
                assessor_name = st.text_input("Assessor Name", value="Alice Johnson")

            with st.expander("2. Findings", expanded=False):
                high_level_findings = st.text_area(
                    "High-Level Findings",
                    value=(
                        "- Open SSH port with weak credentials.\n"
                        "- No rate limiting on login endpoints.\n"
                        "- Default admin credentials still active on management portal."
                    ),
                )
                detailed_findings = st.text_area(
                    "Detailed Findings",
                    value=(
                        "1. **Weak SSH Password**\n"
                        "   - Exploit: Brute-forced SSH access.\n"
                        "   - Impact: Full server compromise.\n\n"
                        "2. **Default Credentials on Admin Panel**\n"
                        "   - Exploit: Admin:admin login successful.\n"
                        "   - Impact: Unauthorized configuration changes."
                    ),
                )

            with st.expander("3. Exploitation Details", expanded=False):
                tools_used = st.text_area(
                    "Tools Used",
                    value="Nmap, Hydra, Metasploit, Burp Suite.",
                )
                steps_taken = st.text_area(
                    "Steps Taken",
                    value=(
                        "1. Identified open ports and services using Nmap.\n"
                        "2. Brute-forced SSH login with Hydra.\n"
                        "3. Exploited admin panel default credentials using manual testing."
                    ),
                )

            with st.expander("4. Recommendations", expanded=False):
                mitigation_strategies = st.text_area(
                    "Mitigation Strategies",
                    value=(
                        "- Disable default credentials and enforce password complexity.\n"
                        "- Apply rate limiting and lockout mechanisms on authentication endpoints.\n"
                        "- Monitor and audit access logs for anomalies."
                    ),
                )
                additional_notes = st.text_area(
                    "Additional Notes",
                    value="Consider implementing a SIEM for centralized monitoring.",
                )

            submitted = st.form_submit_button("Generate Pentest Report")

    elif tabs == "⚠️ Incident Response Plan":
        with st.form("incident_response_form"):
            with st.expander("1. Incident Details", expanded=True):
                incident_name = st.text_input("Incident Name", value="Ransomware Attack on Finance Systems")
                incident_date = st.date_input("Incident Date")
                incident_description = st.text_area(
                    "Incident Description",
                    value=(
                        "A ransomware attack encrypted sensitive financial data, rendering it inaccessible. "
                        "The attack vector was traced to a phishing email targeting employees."
                    ),
                )

            with st.expander("2. Actions Taken", expanded=False):
                actions_taken = st.text_area(
                    "Actions Taken",
                    value=(
                        "1. Isolated affected systems from the network.\n"
                        "2. Restored data from backups.\n"
                        "3. Notified employees and conducted post-incident forensics."
                    ),
                )

            with st.expander("3. Lessons Learned", expanded=False):
                lessons_learned = st.text_area(
                    "Lessons Learned",
                    value=(
                        "- Improve phishing awareness training.\n"
                        "- Enforce least privilege access.\n"
                        "- Implement endpoint detection and response tools."
                    ),
                )

            with st.expander("4. Recommendations", expanded=False):
                future_prevention = st.text_area(
                    "Future Prevention Strategies",
                    value="Deploy advanced email filtering and improve incident response SOPs.",
                )

            submitted = st.form_submit_button("Generate Incident Response Plan")

    elif tabs == "✅ Compliance":
        with st.form("compliance_form"):
            with st.expander("1. General Information", expanded=True):
                project_name = st.text_input("Project Name", value="ISO 27001 Compliance Assessment")
                client_name = st.text_input("Client Name", value="XYZ Inc.")
                assessment_date = st.date_input("Assessment Date")
                compliance_type = st.text_input("Compliance Type", value="ISO 27001")

            with st.expander("2. Compliance Findings", expanded=False):
                compliance_findings = st.text_area(
                    "Compliance Findings",
                    value=(
                        "- Lack of a formal Information Security Policy.\n"
                        "- Absence of periodic risk assessments.\n"
                        "- Unencrypted storage of sensitive customer data."
                    ),
                )

            with st.expander("3. Recommendations", expanded=False):
                compliance_recommendations = st.text_area(
                    "Recommendations",
                    value=(
                        "- Establish and document an Information Security Policy.\n"
                        "- Conduct risk assessments biannually.\n"
                        "- Implement data encryption for sensitive data storage."
                    ),
                )

            submitted = st.form_submit_button("Generate Compliance Report")

    elif tabs == "📊 Risk Assessment":
        with st.form("risk_assessment_form"):
            with st.expander("1. General Information", expanded=True):
                project_name = st.text_input("Project Name", value="Corporate Network Risk Assessment")
                client_name = st.text_input("Client Name", value="TechWorld LLC")
                assessment_date = st.date_input("Assessment Date")

            with st.expander("2. Risk Details", expanded=False):
                risks_identified = st.text_area(
                    "Risks Identified",
                    value=(
                        "- Unpatched critical vulnerabilities in network devices.\n"
                        "- Lack of multifactor authentication for VPN access.\n"
                        "- Overly permissive file-sharing permissions."
                    ),
                )
                risk_severity = st.text_area(
                    "Risk Severity",
                    value=(
                        "1. High: Unpatched vulnerabilities in firewalls could lead to remote exploitation.\n"
                        "2. Medium: VPN access without MFA increases risk of credential theft exploitation.\n"
                        "3. Low: Overly permissive permissions increase internal data leakage risks."
                    ),
                )

            with st.expander("3. Mitigation Plan", expanded=False):
                risk_mitigation_plan = st.text_area(
                    "Risk Mitigation Plan",
                    value=(
                        "- Deploy patches for all critical vulnerabilities immediately.\n"
                        "- Enforce MFA for all remote access points.\n"
                        "- Review and restrict file-sharing permissions."
                    ),
                )

            submitted = st.form_submit_button("Generate Risk Assessment Report")



    # Handle report generation
    if submitted:
        with st.spinner("Generating your report... ⏳"):
            time.sleep(2)
            st.progress(100)
        try:
            # Initialize data to prevent undefined variable issues
            data = {}

            if tabs == "🛡️ VAPT":
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
            elif tabs == "🔐 Pentesting":
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
            elif tabs == "⚠️ Incident Response Plan":
                data = {
                    "incident_name": incident_name,
                    "incident_date": str(incident_date),
                    "incident_description": incident_description,
                    "actions_taken": actions_taken,
                    "lessons_learned": lessons_learned,
                    "future_prevention": future_prevention,
                }
            elif tabs == "✅ Compliance":
                data = {
                    "project_name": project_name,
                    "client_name": client_name,
                    "assessment_date": str(assessment_date),
                    "compliance_type": compliance_type,
                    "compliance_findings": compliance_findings,
                    "compliance_recommendations": compliance_recommendations,
                }
            elif tabs == "📊 Risk Assessment":
                data = {
                    "project_name": project_name,
                    "client_name": client_name,
                    "assessment_date": str(assessment_date),
                    "risks_identified": risks_identified,
                    "risk_severity": risk_severity,
                    "risk_mitigation_plan": risk_mitigation_plan,
                }

            # Ensure data is valid before generating the report
            if not data:
                raise ValueError("No data collected for the selected tab. Please complete the form.")

            # Clean the tabs variable to remove emojis and unnecessary characters
            clean_tab_key = ''.join(char for char in tabs if char.isalnum() or char.isspace()).strip()

            # Generate the report
            report_content = generate_report(clean_tab_key, data)

            # Generate HTML report using cleaned tab key
            template_file = f"backend/templates/{clean_tab_key.lower().replace(' ', '_')}_template.html"
            html_content = generate_html_report(data, template_file)

            # Display the report in Markdown format
            st.markdown("### Generated Report (Preview):")

            # Prepare the Markdown content for all data fields
            st.markdown = f"""
            ## {tabs} Report for {data.get('project_name', data.get('incident_name', 'Unnamed Project'))}

            **Client Name:** {data.get('client_name', 'N/A')}  
            **Assessment Date:** {data.get('assessment_date', 'N/A')}  
            **Assessor Name:** {data.get('assessor_name', 'N/A')}  

            ---

            ### High-Level Findings:
            {data.get('high_level_findings', 'No high-level findings provided.')}

            ---

            ### Detailed Findings:
            {data.get('detailed_findings', 'No detailed findings provided.')}

            ---

            ### Risk Analysis:
            - **Risk Description:** {data.get('risk_description', 'No risk description provided.')}  
            - **Business Impact:** {data.get('business_impact', 'No business impact provided.')}

            ---

            ### Mitigation Strategies:
            {data.get('mitigation_strategies', 'No mitigation strategies provided.')}

            ---

            ### Additional Notes:
            {data.get('additional_notes', 'No additional notes provided.')}

            ---

            ### Tools and Steps (For Pentesting):
            - **Tools Used:** {data.get('tools_used', 'N/A')}  
            - **Steps Taken:** {data.get('steps_taken', 'N/A')}

            ---

            ### Incident Details (For Incident Response):
            - **Incident Name:** {data.get('incident_name', 'N/A')}  
            - **Incident Date:** {data.get('incident_date', 'N/A')}  
            - **Incident Description:** {data.get('incident_description', 'N/A')}  
            - **Actions Taken:** {data.get('actions_taken', 'N/A')}  
            - **Lessons Learned:** {data.get('lessons_learned', 'N/A')}  
            - **Future Prevention:** {data.get('future_prevention', 'N/A')}

            ---

            ### Compliance Details (For Compliance Reports):
            - **Compliance Type:** {data.get('compliance_type', 'N/A')}  
            - **Compliance Findings:** {data.get('compliance_findings', 'N/A')}  
            - **Compliance Recommendations:** {data.get('compliance_recommendations', 'N/A')}

            ---

            ### Risk Assessment (For Risk Assessment Reports):
            - **Risks Identified:** {data.get('risks_identified', 'N/A')}  
            - **Risk Severity:** {data.get('risk_severity', 'N/A')}  
            - **Risk Mitigation Plan:** {data.get('risk_mitigation_plan', 'N/A')}

            ---

            ### Summary of Findings:
            - **Tools and Technologies Used:** {data.get('tools_used', 'N/A')}
            - **Actions Taken and Next Steps:** {data.get('steps_taken', 'N/A')}
            - **Future Recommendations:** {data.get('mitigation_strategies', 'N/A')}

            ---

            **Note:** The report has been generated based on the provided data. Please verify and cross-check with your actual findings and observations.
            """


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