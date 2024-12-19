from jinja2 import Template

def generate_html_report(data: dict, template_path: str) -> str:
    with open(template_path, 'r') as file:
        template = Template(file.read())
    return template.render(data)
