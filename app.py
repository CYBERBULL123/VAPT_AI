import streamlit as st
from backend.langchain_utils import generate_report , generate_analytics
from backend.report import generate_html_report
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Set up the page configuration
st.set_page_config(
    page_title="Cybersecurity Report Generator",
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
    if st.button('😳 Start the App'):
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
        "Choose Report",
        ("🛡️ VAPT", "🔐 Pentesting", "⚠️ Incident Response Plan", "✅ Compliance", "📊 Risk Assessment", "📈 Analytics"),
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

    elif tabs == "📈 Analytics":
        # Setting up the dark theme for the plots
        plt.style.use('dark_background')

        st.header("🔍 Comprehensive Analytics Dashboard")
        st.write("Explore findings, severity, risk scores, and exploitation likelihood with detailed visualizations.")

        # Load or process your actual findings data
        analytics_data = generate_analytics(data={})
        df = pd.DataFrame(analytics_data['structured_data'])

        # Display the findings in a table
        st.subheader("🔎 Findings Overview")
        st.dataframe(df)
        st.download_button(
            label="📥 Download Findings Data as CSV",
            data=df.to_csv(index=False),
            file_name="findings_data.csv",
            mime="text/csv"
        )
        st.divider()

        # Add tabs for Plotly and Seaborn visualizations
        plot_tab, seaborn_tab = st.tabs(["📊 Plotly Charts", "🎨 Seaborn Charts"])

        with plot_tab:
            st.subheader("📊 Interactive Plotly Visualizations")

            # 1. Heatmap: Severity vs Exploitation Likelihood
            st.write("🔴 **Heatmap: Severity vs Exploitation Likelihood**")
            st.caption("Outcome: This heatmap visualizes how exploitation likelihood varies across different severity levels and findings. It highlights the concentration of high exploitation likelihood within specific severities.")
            pivot_df = df.pivot(index="Finding", columns="Severity", values="Exploitation Likelihood")
            heatmap_fig = px.imshow(
                pivot_df,
                color_continuous_scale='viridis',
                labels=dict(x="Severity", y="Finding", color="Exploitation Likelihood"),
                title="Severity vs Exploitation Likelihood"
            )
            heatmap_fig.update_layout(width=700, height=500)
            st.plotly_chart(heatmap_fig, use_container_width=True)

            # 2. Bar Chart: Risk Scores by Severity
            st.write("📊 **Bar Chart: Risk Scores by Severity**")
            st.caption("Outcome: This bar chart shows the aggregated risk scores for each severity level. It provides a clear comparison of which severity level contributes the most to overall risk.")
            bar_fig = px.bar(
                df.groupby('Severity')['Risk Score'].sum().reset_index(),
                x='Severity',
                y='Risk Score',
                color='Severity',
                title="Risk Scores by Severity"
            )
            st.plotly_chart(bar_fig, use_container_width=True)

            # 3. Pie Chart: Findings by Severity
            st.write("📝 **Pie Chart: Findings by Severity**")
            st.caption("Outcome: This pie chart displays the proportion of findings classified under each severity level. It helps to identify which severities are most frequent.")
            severity_count = df['Severity'].value_counts()
            pie_fig = px.pie(
                names=severity_count.index,
                values=severity_count.values,
                title="Distribution of Findings by Severity",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(pie_fig, use_container_width=True)

            # 4. Scatter Plot: Risk vs Exploitation Likelihood
            st.write("📉 **Scatter Plot: Risk vs Exploitation Likelihood**")
            st.caption("Outcome: This scatter plot illustrates the relationship between risk scores and exploitation likelihood. It reveals clusters or trends, such as high-risk scores correlating with high likelihoods.")
            scatter_fig = px.scatter(
                df,
                x="Risk Score",
                y="Exploitation Likelihood",
                color="Severity",
                symbol="Severity",
                size="Risk Score",
                title="Risk vs Exploitation Likelihood"
            )
            st.plotly_chart(scatter_fig, use_container_width=True)

            # 5. Line Chart: Exploitation Likelihood over Findings
            st.write("📈 **Line Chart: Exploitation Likelihood over Findings**")
            st.caption("Outcome: This line chart tracks how exploitation likelihood changes across findings, offering insights into patterns or outliers in the data.")
            line_fig = px.line(
                df,
                x="Finding",
                y="Exploitation Likelihood",
                title="Exploitation Likelihood over Findings",
                markers=True
            )
            line_fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(line_fig, use_container_width=True)

            # 6. Histogram: Distribution of Risk Scores
            st.write("📊 **Histogram: Distribution of Risk Scores**")
            st.caption("Outcome: This histogram reveals the distribution of risk scores across findings, helping to identify whether risks are evenly spread or concentrated in certain ranges.")
            hist_fig = px.histogram(
                df,
                x="Risk Score",
                nbins=10,
                title="Histogram of Risk Scores",
                marginal="box"
            )
            st.plotly_chart(hist_fig, use_container_width=True)


        with seaborn_tab:
            st.subheader("🎨 Seaborn Visualizations")

            # 1. Heatmap: Severity vs Exploitation Likelihood
            st.write("🔴 **Heatmap: Severity vs Exploitation Likelihood**")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(pivot_df, annot=True, cmap='coolwarm', fmt='.1f', linewidths=0.5, ax=ax)
            ax.set_title("Severity vs Exploitation Likelihood", fontsize=14)
            st.pyplot(fig)

            # 2. Bar Plot: Risk Scores by Severity
            st.write("📊 **Bar Plot: Risk Scores by Severity**")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.barplot(
                x=df.groupby('Severity')['Risk Score'].sum().index,
                y=df.groupby('Severity')['Risk Score'].sum().values,
                palette="viridis",
                ax=ax
            )
            ax.set_title("Risk Scores by Severity", fontsize=14)
            ax.set_ylabel("Risk Score")
            ax.set_xlabel("Severity")
            st.pyplot(fig)

            # 3. Pie Chart: Findings by Severity
            st.write("📝 **Pie Chart: Findings by Severity**")
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(severity_count, labels=severity_count.index, autopct='%1.1f%%', startangle=90, colors=['#ff6347', '#ffa500', '#4caf50'])
            ax.axis('equal')  # Equal aspect ratio ensures a circular pie chart
            ax.set_title("Distribution of Findings by Severity", fontsize=14)
            st.pyplot(fig)

            # 4. Scatterplot: Risk vs Exploitation Likelihood
            st.write("📉 **Scatterplot: Risk vs Exploitation Likelihood**")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.scatterplot(data=df, x="Risk Score", y="Exploitation Likelihood", hue="Severity", style="Severity", s=100, palette="viridis", ax=ax)
            ax.set_title("Risk vs Exploitation Likelihood", fontsize=14)
            ax.set_xlabel("Risk Score")
            ax.set_ylabel("Exploitation Likelihood")
            st.pyplot(fig)

            # 5. Line Plot: Exploitation Likelihood over Findings
            st.write("📈 **Line Plot: Exploitation Likelihood over Findings**")
            fig, ax = plt.subplots(figsize=(16, 10))
            sns.lineplot(data=df, x="Finding", y="Exploitation Likelihood", marker='o', color='cyan', ax=ax)
            ax.set_title("Exploitation Likelihood over Findings", fontsize=14)
            ax.set_xticklabels(df['Finding'], rotation=45, ha='right')
            st.pyplot(fig)

            # Histogram: Distribution of Risk Scores
            st.write("**Histogram: Distribution of Risk Scores**")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.histplot(df['Risk Score'], bins=10, kde=True, color="skyblue", ax=ax)
            ax.set_title("Histogram of Risk Scores", fontsize=14)
            st.pyplot(fig)
            st.divider()

            # 6. Violin Plot: Severity vs Exploitation Likelihood
            st.write("🎻 **Violin Plot: Severity vs Exploitation Likelihood**")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.violinplot(data=df, x="Severity", y="Exploitation Likelihood", palette="dark", ax=ax)
            ax.set_title("Severity vs Exploitation Likelihood", fontsize=14)
            ax.set_xlabel("Severity")
            ax.set_ylabel("Exploitation Likelihood")
            st.pyplot(fig)

            # 7. Box Plot: Severity vs Risk Score
            st.write("📦 **Box Plot: Severity vs Risk Score**")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.boxplot(data=df, x="Severity", y="Risk Score", palette="muted", ax=ax)
            ax.set_title("Severity vs Risk Score", fontsize=14)
            ax.set_xlabel("Severity")
            ax.set_ylabel("Risk Score")
            st.pyplot(fig)
            st.divider()
        st.markdown("""
            ### 📊 Insights and Impacts of Visualizations

            | **Visualization**                             | **Key Insights**                                                                                | **Potential Impacts**                                                                                 |
            |-----------------------------------------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
            | 🔴 **Heatmap: Severity vs Exploitation Likelihood** | **Critical Zones:** High-severity vulnerabilities align with the highest exploitation likelihood. **Hidden Risks:** Medium-severity findings can pose overlooked dangers. | 🚨 **Action Needed:** Attackers prioritize high-likelihood vulnerabilities for exploitation. <br> 🛠️ **Mitigation:** Patch high-severity issues immediately. |
            | 📊 **Bar Chart: Risk Scores by Severity**     | **Risk Leaders:** High-severity issues dominate total risk scores. <br> Medium-severity also contributes significantly.         | 🎯 **Focus Areas:** Attackers exploit high-risk contributors first. 📈 **Resource Allocation:** Prioritize mitigation strategies for top risk scores. |
            | 📝 **Pie Chart: Findings by Severity**        | **Threat Breakdown:** High-severity findings are fewer but far more critical. <br> **Majority Share:** Medium/low-severity dominate in count. | 🔍 **Focus Shift:** High-severity issues are attacker favorites. 🚧 **Preventative Measures:** Address medium/low-severity to block lateral movements. |
            | 📉 **Scatter Plot: Risk vs Exploitation Likelihood** | **Critical Clusters:** High-risk, high-likelihood findings form key target zones. <br> **Subtle Threats:** Low-likelihood risks can evolve. | 🚩 **Primary Target:** Attackers exploit clustered vulnerabilities for maximum damage. 🛡️ **Strategic Defense:** Minimize critical clusters proactively. |
            | 📈 **Line Chart: Exploitation Likelihood Over Findings** | **Trending Risks:** Consistently high-likelihood findings highlight recurring vulnerabilities. <br> Fluctuating risks need constant monitoring. | 📅 **Audit Timelines:** Track trends to avoid recurring risks. 🌟 **Proactive Defense:** Predict and address upcoming attack trends effectively. |
            | 🟦 **Histogram: Distribution of Risk Scores** | **Risk Patterns:** Majority of findings fall within moderate risk ranges (e.g., 60–80). <br> Outliers (>90) are urgent concerns. | 🔥 **Priority Fixes:** Attackers target high-risk outliers for significant impacts. 🚀 **Quick Wins:** Addressing outliers reduces the attack surface. |

            ---

            ### 🔑 Key Takeaways for Action
            - 🛡️ **High-Severity Focus:** Address high-severity vulnerabilities immediately to neutralize critical threats.
            - 🔄 **Medium-Risk Monitoring:** Medium-risk findings often act as stepping stones for attackers; ensure consistent management.
            - 📊 **Trend Awareness:** Use exploitation likelihood trends to anticipate and mitigate future vulnerabilities.
            - 🚀 **Resource Optimization:** Align resources to address critical clusters and reduce high-risk outliers effectively.

            ---

            ✨ **Remember:** Insightful visualizations are not just data—they're a blueprint for defense!

        """)
        return




    if submitted:
        try:
            # Initialize data to prevent undefined variable issues
            data = {}

            # Collect data based on the selected tab
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

            with st.spinner("Generating your report... ⏳"):
                # Generate the report
                report_content = generate_report(clean_tab_key, data)
                time.sleep(2)  # Simulate time for LLM processing

            # Store the report in the session state
            if "reports" not in st.session_state:
                st.session_state.reports = {}
            
            # Use clean_tab_key as a unique identifier for the report
            st.session_state.reports[clean_tab_key] = report_content

            # Generate HTML report
            template_file = f"backend/templates/{clean_tab_key.lower().replace(' ', '_')}_template.html"
            html_content = generate_html_report(data, template_file)

            # Display download button
            st.download_button(
                label="📥 Download Report HTML",
                data=html_content,
                file_name=f"{data.get('project_name', data.get('incident_name', 'report'))}_report.html",
                mime="text/html"
            )

            st.success(f"{tabs} Report for '{data.get('project_name', data.get('incident_name', 'Unnamed Project'))}' generated successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            print(e)

    # Display all saved reports in expanders
    if "reports" in st.session_state:
        st.markdown("## Generated Reports")
        for report_key, report_content in st.session_state.reports.items():
            with st.expander(f"{report_key} Report"):
                for section, content in report_content.items():
                    st.markdown(f"### **{section}:**")
                    st.markdown(content if content else "_No data provided._")



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