# **Agentic Report Generator Module (ARGM)** 
- Cyber Report Automation Platform

**OxSecure Intelligence** is a next-gen platform that automates Vulnerability Assessment and Penetration Testing (VAPT) report generation using **Generative AI** and **Machine Learning**. It simplifies the creation of detailed, professional VAPT reports, integrating seamlessly with vulnerability scanners for efficient analysis.

---

### **Key Features**:
- **AI-Driven Reports**: Automatically generate accurate, professional VAPT reports with minimal input.
- **Customizable Templates**: Flexible report formats with HTML templates, converted to PDF.
- **Real-time Collaboration**: Multiple users can contribute and refine reports in real-time.
- **Advanced Reasoning**: Uses **CoT**, **ToT**, and **RAP** for intelligent analysis and continuous report refinement.
- **Visual Insights**: Includes graphs, tables, and charts for clear data representation.

---

### **How It Works**:
1. **Upload Scan Results**: Import data from vulnerability scanners.
2. **Generate Reports**: AI analyzes and generates customized reports.
3. **Download Reports**: Download reports in PDF format.

---

### **Architecture**:
1. **Frontend**:  
   - **Streamlit**: User-friendly web interface for seamless interaction.
   
2. **Backend**:  
   - **Python**: Core logic and processing.
   - **Gemini API**: AI-driven content generation and analysis.
   - **LangChain**: Dynamic, customizable prompts for precise reporting.

3. **AI Reasoning**:  
   - **CoT**: Step-by-step analysis.
   - **ToT**: Linked reasoning across multiple vulnerabilities.
   - **RAP**: Continuous feedback loop for real-time report iteration.

---

### **Developer Setup**:
To contribute or check out the project, you'll need to set up your environment and API keys. Follow these steps:

1. **Clone the Repository**:
   - Clone this repository to your local machine.

2. **Create `secrets.toml` File**:
   - Create a file named `secrets.toml` in the root directory of the project.
   
3. **Add Your Gemini API Key**:
   - Obtain a valid Gemini API key from the [Google Cloud Console](https://console.cloud.google.com/).
   - Add the following to your `secrets.toml` file (replace `your-gemini-api-key` with your actual key):

```toml
[api_keys]
gemini_api_key = "your-gemini-api-key"
```

4. **Use the Mock `sample_secrets.toml` File**:
   - A sample secrets file (`sample_secrets.toml`) is provided in the repository as a template for setting up your secrets file.

5. **Run the Application**:
   - Ensure that your environment is properly configured and the `secrets.toml` file is in place. You can then run the app using Streamlit or through the Python backend.

---

**OxSecure Intelligence** delivers actionable insights and professional VAPT reports with AI-powered efficiency, simplifying the complex world of cybersecurity.

---