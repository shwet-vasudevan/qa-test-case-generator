import os
import time
import json
import google.generativeai as genai
from dotenv import load_dotenv # Import the library

# Load environment variables from .env file
load_dotenv() 

# Load environment variables for API key
api_key = os.environ.get('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set it in your .env file or as an environment variable.")

genai.configure(api_key=api_key)

def load_files(prompt_file, spec_file):
    """Loads content from the prompt and specification files."""
    try:
        with open(prompt_file, 'r') as p_file, open(spec_file, 'r') as s_file:
            prompt_template = p_file.read()
            feature_spec = s_file.read()
        return prompt_template, feature_spec
    except FileNotFoundError as e:
        print(f"Error: A required file was not found. Please ensure '{prompt_file}' and '{spec_file}' exist.")
        raise e

def generate_test_cases(full_prompt, max_retries=3):
    """
    Makes an API call to Gemini with retry logic.
    Returns the JSON output or None if an error occurs.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries} to generate test cases...")
        try:
            response = model.generate_content(full_prompt)
            if response.text:
                return response.text
            else:
                print("Model returned an empty response.")
                return None
        except Exception as e:
            print(f"API call failed: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Max retries reached. Exiting.")
                return None

def parse_and_validate_json(json_string):
    """Parses a JSON string and validates the structure."""
    try:
        data = json.loads(json_string)
        if not isinstance(data, list):
            raise ValueError("Root element is not a JSON array.")

        # Optional: Validate each object's keys
        for item in data:
            required_keys = ["id", "title", "description", "priority", "type", "preconditions", "steps", "expected_result"]
            if not all(key in item for key in required_keys):
                print("Warning: A test case object is missing a required key.")

        return data
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. The model's output was not valid JSON.")
        print(f"JSON Decode Error: {e}")
        return None
    except ValueError as e:
        print(f"Validation Error: {e}")
        return None

def main():
    """Main function to orchestrate the test case generation process."""
    prompt_file = 'prompt_template.txt'
    spec_file = 'spec.txt'

    prompt_template, feature_spec = load_files(prompt_file, spec_file)
    full_prompt = prompt_template.format(spec=feature_spec)

    raw_output = generate_test_cases(full_prompt)
    if not raw_output:
        print("Could not generate a valid response.")
        return

    test_cases = parse_and_validate_json(raw_output)
    if test_cases:
        print("\nSuccessfully generated and parsed test cases! ✨\n")
        # Print the structured test cases in a readable format
        for tc in test_cases:
            print(f"--- Test Case: {tc['title']} ({tc['id']}) ---")
            print(f"Priority: {tc['priority']} | Type: {tc['type']}")
            print(f"Description: {tc['description']}")
            print(f"Preconditions: {tc['preconditions']}")
            print("Steps:")
            for step in tc['steps']:
                print(f"  - {step}")
            print(f"Expected Result: {tc['expected_result']}\n")
    else:
        print("\nFailed to process the model's output.")

if __name__ == "__main__":
    main()