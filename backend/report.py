from jinja2 import Template
import json

def generate_html_report(data: dict, template_path: str) -> str:
    with open(template_path, 'r') as file:
        template = Template(file.read())
    try:
        # Handle nested structures that might be JSON strings
        json_fields = ['findings', 'recommendations', 'tools', 'impacts', 
                      'scope_items', 'strategies', 'compliances']
        for field in json_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = json.loads(data[field])
                except:
                    data[field] = []
        
        # Set default values for missing fields
        defaults = {
            'project_name': 'Security Assessment',
            'client_name': 'Client',
            'assessment_date': 'N/A',
            'assessor_name': 'Security Assessor',
            'summary': 'No summary provided',
            'introduction': 'No introduction provided',
            'incident_description': 'No incident description provided',
            'response_actions': 'No response actions provided',
            'risk_analysis': 'No risk analysis provided',
            'risk_description': 'No risk description provided',
            'risk_likelihood': 'N/A',
            'risk_impact': 'N/A',
            'business_impact': 'No business impact provided',
            'mitigation_summary': 'No mitigation summary provided',
            'gaps_identified': 'No gaps identified',
            'compliance_standards': 'No compliance standards specified',
            'additional_notes': 'No additional notes'
        }
        
        # Update data with defaults for missing values
        for key, default in defaults.items():
            if key not in data or not data[key]:
                data[key] = default
        
        return template.render(**data)
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        return f"""
        <html><body>
        <h1>Error Generating Report</h1>
        <p>Error: {str(e)}</p>
        <pre>{json.dumps(data, indent=2)}</pre>
        </body></html>
        """
