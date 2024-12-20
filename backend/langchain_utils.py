from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st


# Configure API Key
gemini_key = st.secrets["api_keys"]["gemini_api_key"]


# Initialize GEMINI LLM for reasoning tasks
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    api_key=gemini_key,
    temperature=0.7,
    max_tokens=3000,  # Allow for detailed responses
)

# Define tools for the agent
tools = [
    Tool(
        name="Analyze Findings",
        func=lambda x: analyze_findings(x),
        description=(
            "Analyze cybersecurity findings to identify vulnerabilities, risks, and threats. "
            "Provide a categorized analysis with potential impacts and related CVEs where applicable."
        )
    ),
    Tool(
        name="Evaluate Risks",
        func=lambda x: evaluate_risks(x),
        description=(
            "Evaluate risks based on identified vulnerabilities. "
            "Include severity, likelihood of exploitation, and potential business impacts."
        )
    ),
    Tool(
        name="Generate Recommendations",
        func=lambda x: generate_recommendations(x),
        description=(
            "Generate actionable recommendations to mitigate identified risks. "
            "Include preventive measures, detection strategies, and response plans."
        )
    )
]

# Initialize the agent with tools
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=ConversationBufferMemory(),
    verbose=True
)

# Reasoning Task: Using the agent to reason through findings
def agent_reasoning_task(data: dict) -> str:
    agent_input = f"Task: Analyze and process the following findings.\nInput: {data}"
    response = agent.run(agent_input)
    return response

# Helper functions for agent tasks
def analyze_findings(data):
    return f"Analyzing findings: {data}"

def evaluate_risks(data):
    return f"Evaluating risks: {data}"

def generate_recommendations(data):
    return f"Generating recommendations for: {data}"

# Chain-of-Thought (CoT) prompt generator
def generate_cot_prompt(report_type: str, data: dict) -> str:
    report_prompts = {
        "VAPT": """
        Generate a comprehensive Vulnerability Assessment and Penetration Testing (VAPT) report. 
        The structure should include:
        1. **Executive Summary**: 
            - Overview of the engagement's scope, objectives, and methodology.
            - High-level findings summary with impact on the business.
        2. **Technical Findings**: 
            - Detailed descriptions of vulnerabilities identified.
            - Include screenshots, CVEs, and proof-of-concept exploits where relevant.
        3. **Risk Analysis**: 
            - Evaluate risks considering severity, exploitability, and potential business impacts.
            - Provide a likelihood-impact matrix for prioritization.
        4. **Recommendations**: 
            - Detailed actionable steps for mitigation.
            - Short-term, mid-term, and long-term recommendations.
        """,
        "Pentesting": """
        Generate a detailed Penetration Testing report. 
        The structure should include:
        1. **Introduction**: 
            - Scope, methodology, and tools used during the test.
        2. **Findings**: 
            - Categorized vulnerabilities with detailed descriptions.
            - Include screenshots, evidence, and possible exploitation scenarios.
        3. **Exploitation Details**: 
            - Techniques used, tools leveraged, and success rates of attempts.
        4. **Recommendations**: 
            - Steps to remediate each vulnerability with priority levels.
        """,
        "Incident Response Plan": """
        Generate an Incident Response Plan. 
        The structure should include:
        1. **Introduction**: 
            - Objectives, scope, and purpose of the plan.
        2. **Incident Classification**: 
            - Categorize incidents based on severity levels (e.g., low, medium, high).
        3. **Workflow**: 
            - Outline detection, containment, eradication, and recovery steps.
        4. **Roles and Responsibilities**: 
            - Define roles for team members with a RACI matrix (Responsible, Accountable, Consulted, Informed).
        """,
        "Compliance": """
        Generate a Compliance Report. 
        The structure should include:
        1. **Introduction**: 
            - Scope and objectives of the assessment.
            - Frameworks considered (e.g., ISO 27001, GDPR, HIPAA).
        2. **Findings**: 
            - Detailed sections for compliance gaps and achieved milestones.
        3. **Recommendations**: 
            - Steps to address gaps and ensure ongoing compliance.
        """,
        "Risk Assessment": """
        Generate a Risk Assessment Report. 
        The structure should include:
        1. **Risk Identification**: 
            - Detailed listing of risks including vulnerabilities, threats, and weaknesses.
        2. **Risk Evaluation**: 
            - Severity analysis using a qualitative or quantitative approach.
            - Include a risk heat map for visualization.
        3. **Mitigation Plan**: 
            - Steps to reduce risks with resource allocation.
            - Residual risk overview after implementation.
        """
    }

    return report_prompts.get(report_type, "Unknown report type")

# Tree-of-Thought (ToT) Method
def generate_tree_of_thought(data: dict, steps: list) -> list:
    responses = []
    for step in steps:
        prompt = f"Step: {step}\nInput Data: {data}\n"
        response = llm.predict(prompt)
        responses.append(response)
    return responses

# Recursive Action Planning (RAP)
def recursive_refinement(prompt: str, max_iterations: int = 3) -> str:
    current_prompt = prompt
    for _ in range(max_iterations):
        try:
            response = llm.predict(current_prompt)
            current_prompt = f"Refine the following output:\n{response}"
        except Exception as e:
            break
    return current_prompt

# Unified Report Generation Function
def generate_report(report_type: str, data: dict) -> dict:
    # Generate CoT prompt
    cot_prompt = generate_cot_prompt(report_type, data)

    # Define steps for Tree-of-Thought (ToT)
    steps = {
        "VAPT": ["Summarize vulnerabilities.", "Analyze risks.", "Propose remediation.", "Draft report."],
        "Pentesting": ["Define scope.", "Detail findings.", "Propose fixes.", "Finalize report."],
        "Incident Response Plan": ["Classify incidents.", "Describe workflow.", "Outline roles.", "Draft plan."],
        "Compliance": ["Analyze framework.", "List findings.", "Propose compliance steps.", "Summarize."],
        "Risk Assessment": ["Identify risks.", "Evaluate severity.", "Suggest mitigations.", "Summarize residual risks."]
    }

    # Agent reasoning task
    agent_response = agent_reasoning_task(data)

    # Generate Tree-of-Thought (ToT) responses
    tot_responses = generate_tree_of_thought(data, steps[report_type])

    # Generate refined response
    final_response = recursive_refinement(cot_prompt)

    # Construct report
    report = {
        "Executive Summary": tot_responses[0],
        "Technical Findings": tot_responses[1],
        "Risk Analysis": tot_responses[2],
        "Recommendations": tot_responses[1],
        "Final Report": final_response,
        "Agent Reasoning Response": agent_response
    }

    return report
