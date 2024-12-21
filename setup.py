from setuptools import setup, find_packages

setup(
    name="OxSecure Intelligence",
    version="1.0.0",  # Update version as needed
    author="Aditya",
    author_email="opaadi98@gmail.com", 
    description="Automated Vulnerability Assessment and Penetration Testing (VAPT) Report Generation with Generative AI and Machine Learning",
    long_description=open('README.md').read(), 
    long_description_content_type="text/markdown",
    url="https://github.com/CYBERBULL123/VAPT_AI", 
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-google-genai",
        "jinja2"
        "plotly"
        "requests",  
    ],
    python_requires='>=3.6',
)
