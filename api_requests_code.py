import re 
import requests
import re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Your OpenRouter API Key
API_KEY = Open Router API Key

# OpenRouter model you want to use
MODEL = Open Router Model

def call_model_code(prompt, model_name):
    """
    Calls the OpenRouter API to generate a response.
    `model_name` is optional now—defaults to preset MODEL.
    """
    model_name = None
    MODEL = "mistralai/mistral-small-3.1-24b-instruct:free"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourapp.com",
        "X-Title": "RePromptArc"
    }

    payload = {
        "model": model_name or MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            verify=False  # ONLY for testing behind corp VPN
        )
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def extract_python_code(text):
    """Extracts only the Python code from the generated response."""
    code_block = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    return code_block.group(1) if code_block else text

# URL = "http://localhost:12345/api/generate"

# def call_model(prompt,model_name):
#     """
#     Calls the Ollama API to generate a response based on the given prompt.
#     """
#     temperature=0.7
#     max_tokens=512
#     payload = {
#         "model": model_name,
#         "prompt": prompt,
#         "temperature": temperature,
#         "max_tokens": max_tokens,
#         "stream": False  
#     }
    
#     try:
#         response = requests.post(URL, json=payload)
#         response.raise_for_status()
#         result = response.json()
#         return result.get("response", "").strip()
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"



# def extract_python_code(text):
#     """Extracts only the Python code from the generated response."""
#     code_block = re.search(r"```python\n(.*?)```", text, re.DOTALL)
#     return code_block.group(1) if code_block else text 


# API_KEY = "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"
# MODEL = "mistralai/mistral-small-3.1-24b-instruct:free"

# def call_model(prompt, model_name=None):
#     """
#     Calls the OpenRouter API to generate a response.
#     `model_name` is optional now—defaults to preset MODEL.
#     """
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://yourapp.com",
#         "X-Title": "RePromptArc"
#     }

#     payload = {
#         "model": model_name or MODEL,
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }

#     try:
#         response = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             json=payload,
#             headers=headers,
#             verify=False  
#         )
#         response.raise_for_status()
#         result = response.json()
#         return result['choices'][0]['message']['content']
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"

# def extract_python_code(text):
#     """Extracts only the Python code from the generated response."""
#     code_block = re.search(r"```python\n(.*?)```", text, re.DOTALL)
#     return code_block.group(1) if code_block else text



