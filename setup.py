from setuptools import setup, find_packages

setup(
    name="OxSecure Intelligence",
    version="1.0.0",  # Update version as needed
    author="Aditya",
    author_email="your_email@example.com",  # Replace with your email
    description="Automated Vulnerability Assessment and Penetration Testing (VAPT) Report Generation with Generative AI and Machine Learning",
    long_description=open('README.md').read(),  # Assuming you have a README.md file with the project description
    long_description_content_type="text/markdown",
    url="https://github.com/CYBERBULL123/VAPT_AI",  # Replace with your GitHub URL
    packages=find_packages(),  # Automatically find all packages in your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # You can change this based on your preferred license
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-google-genai",
        "jinja2"
        "plotly"
        "requests",  # Add all the necessary dependencies here
    ],
    python_requires='>=3.6',
)
