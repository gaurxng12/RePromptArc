# readability.py
from api_requests_prompt import call_model_prompt
from api_requests_code import call_model_code

def understand_requirements(task_description, model_name):
    prompt = f"""
    You are a helpful assistant specializing in programming tasks.
    Task: {task_description}
    
    Explain the requirements clearly and state any assumptions.
    """
    return call_model_prompt(prompt, model_name)

def generate_pseudocode(requirements, model_name):
    prompt = f"""
    Write detailed pseudocode for the given task. Follow these rules:
    1. Use step-by-step numbered instructions.
    2. Use clear and concise language.
    3. Do not include code syntax; use plain language.
    
    Task: {requirements}
    """
    return call_model_prompt(prompt , model_name)

def pseudocode_to_code(pseudocode,model_name):
    language = "python"
    prompt = f"""
    Convert the following pseudocode into {language} code:
    Pseudocode:
    {pseudocode}
    """
    return call_model_code(prompt,model_name)

def optimize_code(code, model_name , language="Python"):
    prompt = f"""
    Optimize the following {language} code for readability, performance, and best practices:
    Code:
    {code}
    """
    return call_model_code(prompt , model_name)

def optimize_for_read(code,model_name):
    prompt = f"""
    Optimize the following python code for readability, performance, and best practices:
    Code:
    {code}
    """
    return call_model_code(prompt , model_name)


def generate_optimized_prompt(prev_prompt, code, evaluation_results, code_qual, model_name):
    prompt = f"""
You are a prompt engineer tasked with improving code via memory profiling data.

Below is the original code being analyzed:

[CODE START]
{code}
[CODE END]

Here is the original prompt that was used to query an LLM:

[INITIAL PROMPT START]
{prev_prompt}
[INITIAL PROMPT END]

And here is the memory profiling summary that resulted from running the above code:

[MEMORY PROFILE DATA]
- Minimum Memory Usage: {evaluation_results.get("Minimum Memory")} MiB
- Maximum Memory Usage: {evaluation_results.get("Maximum Memory")} MiB
- Average Memory Usage: {evaluation_results.get("Average Memory Used")} MiB
- Memory Spike Magnitude: {evaluation_results.get("Max-Spike in Memory")} MiB
- Spike Timestamps: {evaluation_results.get("Spike TimeStamps")}
[END MEMORY PROFILE DATA]

Here is the code quality evaluation summary:

[CODE QUALITY DATA]
- Overall Quality: {code_qual.get("quality")}
- Code Complexity: {code_qual.get("complexity")}
- Redundancy Level: {code_qual.get("redundancy")}
[END CODE QUALITY DATA]

Using all of this information, generate a new, high-quality LLM prompt that:
1. Incorporates the profiling insights intelligently.
2. Clearly defines the optimization goal (e.g., reduce peak memory usage, smooth spikes).
3. Optionally suggests areas of focus based on spike timing or code structure.
4. Remains grounded in preserving the original functional correctness of the code.
5. Aims to increase overall code quality and reduce complexity wherever feasible.

Respond only with the new, improved prompt. Do not explain your reasoning.
"""
    return call_model_prompt(prompt, model_name)

