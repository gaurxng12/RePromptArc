import json 
import os 
import subprocess

def get_ollama_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        if not output:
            return ["No models found"]

        models = [line.split()[0] for line in output.split("\n") if line]  # Extract model names
        return models[1:]

    except subprocess.CalledProcessError as e:
        return [f"Error running command: {e}"]
    except Exception as e:
        return [f"Unexpected error: {str(e)}"]

print(get_ollama_models)