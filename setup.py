from setuptools import setup, find_packages

setup(
    name="readme-generator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool to generate professional README.md files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/readme-generator",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "rich",
        "questionary",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "readme-gen=readme_generator.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)