# Automated QA Test Case Generator

### Overview

This project is a Python-based automated QA test case generator that leverages the Google Gemini 1.5 Flash API to create structured and detailed test cases from feature specifications. It's designed to streamline the initial test planning phase by generating test cases for a given feature, saving time and ensuring comprehensive coverage.

## Features

    AI-Powered Generation: Uses the Gemini 1.5 Flash API to act as an expert QA engineer and generate test cases.

    Structured Output: Generates test cases in a clean, parsable JSON format with keys for id, title, priority, steps, and expected_result.

    Secure API Key Management: Uses a .env file to securely store your API key, preventing it from being committed to the repository.

    Robust Error Handling: Includes a retry mechanism with exponential backoff for API calls and validates the output to ensure it's valid JSON.

    Git Integration: Uses a .gitignore file to exclude sensitive files (.env) and the virtual environment (venv/) from version control.

## Getting Started

### Prerequisites

    Python 3.8+

    A Google Gemini API Key

### Step-by-Step Installation

    Clone the repository:
    Bash

### git clone
    https://github.com/your-username/qa-test-case-generator.git

    cd qa-test-case-generator

### Create and activate a virtual environment:

On macOS/Linux:

    python3 -m venv venv

    source venv/bin/activate

On Windows:

    python -m venv venv

    venv\Scripts\activate

### Install the required libraries:

    pip install -r requirements.txt

Note: You will first need to create a requirements.txt file by running pip freeze > requirements.txt after installing the google-generativeai and python-dotenv libraries.

## Usage

### Obtain a Gemini API Key:
    Get your API key from the Google AI Studio website.

### Configure your API Key:
Create a file named .env in the project's root directory and add your API key.

    GOOGLE_API_KEY="your_api_key_here"

Remember to replace "your_api_key_here" with your actual key.

### Write your Feature Specification:
    Update the spec.txt file with a clear description of the feature you want to test.

### Run the generator:
Execute the main script from your terminal.

    python main.py

The generated test cases will be printed directly to your console.