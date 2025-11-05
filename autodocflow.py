import os
import ast
import requests
import json
import logging
from jinja2 import Environment, FileSystemLoader # Assuming 'templates' folder is available

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- Configuration ---
# BEST PRACTICE: Do NOT leave a hardcoded key here. 
# The application should fail if the key is not provided via the environment variable.
# For now, we keep the user's fallback for rapid testing, but show a warning.
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDtQNveM1iAAcmMFLShatpT2OIzmwuVfSU')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

if GEMINI_API_KEY == 'AIzaSyDtQNveM1iAAcmMFLShatpT2OIzmwuVfSU':
    logging.warning("Using a default or hardcoded API key. Ensure GEMINI_API_KEY is set in your environment for production use.")

# --- Code Parsing Functions ---

# Parse Python code for functions, classes, and Flask routes
def parse_python_code(src_dir):
    """Parses Python files in a directory to extract functions, classes, and Flask routes."""
    docs = []
    # Note: Using ast.get_source_segment requires the full source code string to be passed
    # and is only available in Python 3.8+.
    for fname in os.listdir(src_dir):
        if fname.endswith('.py'):
            fpath = os.path.join(src_dir, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    source_code = f.read()
            except IOError as e:
                logging.error(f"Could not read file {fpath}: {e}")
                continue
                
            try:
                tree = ast.parse(source_code)
            except SyntaxError as e:
                logging.error(f"Syntax error in {fpath}: {e}")
                continue

            for node in ast.walk(tree):
                # Handle Function Definitions
                if isinstance(node, ast.FunctionDef):
                    route_path = None
                    for deco in node.decorator_list:
                        if isinstance(deco, ast.Call) and getattr(getattr(deco, 'func', None), 'attr', '') == 'route':
                            route_path = deco.args[0].s if deco.args and isinstance(deco.args[0], ast.Constant) else None
                    
                    func_doc = ast.get_docstring(node)
                    # Extract the source code segment for the function/method
                    func_code = ast.get_source_segment(source_code, node)

                    docs.append({
                        'name': node.name,
                        'path': route_path,
                        'doc': func_doc,
                        'code': func_code,
                        'type': 'flask_route' if route_path else 'function',
                        'file': fname
                    })
                # Handle Class Definitions
                elif isinstance(node, ast.ClassDef):
                    class_doc = ast.get_docstring(node)
                    class_code = ast.get_source_segment(source_code, node)
                    docs.append({
                        'name': node.name,
                        'doc': class_doc,
                        'code': class_code,
                        'type': 'class',
                        'file': fname
                    })
    return docs

# --- Gemini AI Integration (UPDATED) ---

def gemini_summarize_code(code):
    """
    Summarizes a block of Python code using the Gemini API.
    Uses the correct URL parameter authentication and request/response structure.
    """
    
    # 1. Construct the final URL with the API key as a query parameter
    full_url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
    # 2. Define headers (Authorization header is removed, only Content-Type is needed)
    headers = {
        'Content-Type': 'application/json'
    }
    
    prompt = (
        "Explain this Python code in plain English, focusing on its purpose, "
        "inputs, and outputs. Keep the explanation concise and under 100 words:\n\n"
        f"CODE:\n{code}"
    )
    
    # 3. Use the correct POST body structure (contents/parts)
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        # 4. Use generationConfig for model parameters
        "generationConfig": {
            "temperature": 0.3,
            # maxOutputTokens is the standard name for max tokens parameter
            "maxOutputTokens": 150, 
        }
    }
    
    try:
        logging.info("Sending request to Gemini API...")
        response = requests.post(full_url, headers=headers, data=json.dumps(data), timeout=60)
        
        # Raise HTTPError for bad status codes (4xx or 5xx)
        response.raise_for_status() 

        result = response.json()
        
        # 5. Correctly navigate the response structure to extract the text
        if 'candidates' in result and result['candidates'][0]['content']['parts']:
            summary = result['candidates'][0]['content']['parts'][0]['text']
            logging.info("Summary successfully extracted.")
            return summary
        else:
            logging.error(f"Gemini API returned an unexpected response structure: {result}")
            return "Summary unavailable due to unexpected API response."
            
    except requests.exceptions.HTTPError as e:
        logging.error(f"Gemini API HTTP Error ({response.status_code}): {response.text}")
        return f"Summary unavailable due to API HTTP Error ({response.status_code})."
    except requests.exceptions.Timeout:
        logging.error("Gemini API request timed out.")
        return "Summary unavailable (API Timeout)."
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during the API request: {e}")
        return "Summary unavailable due to network/request error."
    except Exception as e:
        logging.error(f"An unexpected error occurred during summarization: {e}")
        return "Summary unavailable due to an unexpected error."

# --- Document Rendering Functions ---

# Render HTML docs using Jinja2 templates
def render_docs(docs, output_dir):
    """Renders documentation data into an HTML file using a Jinja2 template."""
    try:
        # Assuming templates are in a 'templates' folder relative to the script
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('api_doc_template.html')
        output = template.render(docs=docs)
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, 'api_docs.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
        logging.info(f"HTML documentation generated at {filepath}")
    except Exception as e:
        logging.error(f"Error rendering HTML documentation: {e}")


# Generate plain English docs with Gemini summaries
def generate_plain_english_doc(docs, output_dir):
    """Generates a plain text document with extracted information and Gemini summaries."""
    lines = []
    lines.append("API Documentation (Plain English)\n" + "="*40 + "\n")
    for doc in docs:
        lines.append(f"Name: {doc['name']}")
        if doc.get('path'):
            lines.append(f"Path: {doc['path']}")
        lines.append(f"Type: {doc['type']}")
        lines.append(f"Defined in: {doc['file']}")
        
        doc_content = ""
        if doc['doc']:
            lines.append("Docstring:")
            doc_content = doc['doc']
        elif doc.get('code'):
            lines.append("Code Explanation (AI Generated):")
            doc_content = gemini_summarize_code(doc['code'])
        else:
            doc_content = "No documentation or code available for analysis."
        
        # Indent the content for readability
        lines.extend([f"  > {line.strip()}" for line in doc_content.split('\n') if line.strip()])
        lines.append("\n" + "-"*40 + "\n") # Separator
        
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'api_docs.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    logging.info(f"Plain English documentation generated at {filepath}")

# --- Main Execution ---

if __name__ == "__main__":
    # Define source and output directories
    # NOTE: You must ensure './src/python' exists and contains your Python code
    # and a 'templates' folder exists with 'api_doc_template.html'.
    py_src = './src/python'
    out_dir = './out'

    # Check for required directories before proceeding
    if not os.path.exists(py_src):
        logging.error(f"Source directory '{py_src}' not found. Please create it and add Python files.")
    elif not os.path.exists('templates'):
        logging.error("Template directory 'templates' not found. Cannot render HTML.")
    else:
        docs = parse_python_code(py_src)
        if not docs:
            logging.warning("No functions, classes, or routes were found to document.")
        else:
            render_docs(docs, out_dir)
            generate_plain_english_doc(docs, out_dir)
            logging.info("Documentation generation process completed successfully.")
