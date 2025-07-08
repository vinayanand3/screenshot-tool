#!/usr/bin/env python3
"""
Setup script for Advanced Screen Capture Tool
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="advanced-screenshot-tool",
    version="1.0.0",
    author="Screenshot Tool Developer",
    author_email="your.email@example.com",
    description="A powerful, feature-rich screen capture tool with annotation capabilities",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/screenshot-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Capture",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "screenshot-tool=main:run_capture_tool",
        ],
    },
    keywords="screenshot, screen capture, annotation, image, tool, gui, tkinter",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/screenshot-tool/issues",
        "Source": "https://github.com/yourusername/screenshot-tool",
        "Documentation": "https://github.com/yourusername/screenshot-tool#readme",
    },
) 