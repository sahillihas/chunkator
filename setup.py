# setup.py
from setuptools import setup, find_packages

setup(
    name="chunkator",
    version='0.0.6',
    description="A library for splitting text into sentences",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sahil Sahil",
    author_email="sahil.lihas@ymail.com",
    url="https://github.com/sahillihas/chunkator",
    packages=find_packages(),  # Automatically finds all sub-packages
    include_package_data=True,  # Ensures non-code files are included
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)