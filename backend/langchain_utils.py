from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize GEMINI LLM for reasoning tasks
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    api_key="AIzaSyDnfECGAlP3640PdfaP6ez9xF5oM6aP15I",
    temperature=0.7,
    max_tokens=2000,
)

# Define tools for agent
tools = [
    Tool(
        name="Analyze Findings",
        func=lambda x: analyze_findings(x),
        description="Analyze the cybersecurity findings to identify vulnerabilities, risks, and threats."
    ),
    Tool(
        name="Evaluate Risks",
        func=lambda x: evaluate_risks(x),
        description="Evaluate the risks based on the findings, considering exploitability, impact, and likelihood."
    ),
    Tool(
        name="Generate Recommendations",
        func=lambda x: generate_recommendations(x),
        description="Generate actionable recommendations based on the analysis and risk evaluation."
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
    agent_input = f"Task: Analyze and process the following findings.\nInput: {data['findings']}"
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
        Generate a Vulnerability Assessment and Penetration Testing (VAPT) report using the following structure:
        1. **Executive Summary**: High-level overview of vulnerabilities discovered.
        2. **Technical Findings**: Detailed analysis of vulnerabilities.
        3. **Risk Analysis**: Evaluate impact, exploitability, and likelihood.
        4. **Recommendations**: Actionable remediation steps.
        """,
        "Pentesting": """
        Generate a detailed Penetration Testing report using the following structure:
        1. **Introduction**: Scope of the test.
        2. **Methodology**: Approach and tools used.
        3. **Findings**: Detailed analysis.
        4. **Recommendations**: Remediation actions.
        """,
        "Incident Response Plan": """
        Generate an Incident Response Plan using the following structure:
        1. **Introduction**: Objectives and scope.
        2. **Incident Classification**: Severity levels.
        3. **Workflow**: Steps for identification, containment, and recovery.
        4. **Roles**: Responsibilities of team members.
        """,
        "Compliance": """
        Generate a Compliance Report using the following structure:
        1. **Introduction**: Scope of assessment.
        2. **Findings**: Compliance and non-compliance areas.
        3. **Recommendations**: Steps to ensure compliance.
        """,
        "Risk Assessment": """
        Generate a Risk Assessment report using the following structure:
        1. **Risk Identification**: Vulnerabilities and threats.
        2. **Risk Evaluation**: Severity and likelihood analysis.
        3. **Mitigation Plan**: Steps to reduce risks.
        """
    }

    return report_prompts.get(report_type, "Unknown report type")

# Tree-of-Thought (ToT) Method
def generate_tree_of_thought(data: dict, steps: list) -> list:
    responses = []
    for step in steps:
        prompt = f"Step: {step}\nInput Data: {data['findings']}\n"
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
        except Exception:
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
        "Recommendations": tot_responses[3],
        "Final Report": final_response,
        "Agent Reasoning Response": agent_response
    }

    return report
