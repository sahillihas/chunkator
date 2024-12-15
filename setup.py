# setup.py
from setuptools import setup, find_packages

setup(
    name="sentence-split",
    version="0.0.1",
    description="A library for splitting text into sentences",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sahil Sahil",
    author_email="sahil.lihas@ymail.com",
    url="https://github.com/sahillihas/sentence-split",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)