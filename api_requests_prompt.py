import re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Your OpenRouter API Key
API_KEY = Open Router API Key

# OpenRouter model you want to use
MODEL = "Open Router Model

def call_model_prompt(prompt, model_name=None):
    """
    Calls the OpenRouter API to generate a response.
    `model_name` is optional now—defaults to preset MODEL.
    """
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
