import ast
import subprocess
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from io import StringIO
import radon.complexity
import re
import numpy as np
import matplotlib.pyplot as plt

def evaluate_code_quality(llm_code):
    with open("temp_script.py", "w") as f:
        f.truncate(0)

    with open("temp_script.py", "w") as f:
        f.write(llm_code)
    output = StringIO()
    reporter = TextReporter(output)
    Run([r"C:\Users\uzair\Desktop\BE Project\Final\temp_script.py"], reporter=reporter, exit=False)

    output.seek(0)
    report = output.read()
    for line in report.splitlines():
        if "Your code has been rated at" in line:
            try:
                return float(line.split()[6].split("/")[0])  
            except:
                return 0.0  

    return 0.0  

def compute_complexity(code):
    try:
        results = radon.complexity.cc_visit(code)
        return sum(block.complexity for block in results)
    except Exception:
        return -1  

def check_redundancy(code):
    lines = code.strip().split("\n")
    unique_lines = set(lines)
    redundancy_score = 1 - (len(unique_lines) / len(lines))
    return round(redundancy_score, 2) if len(lines) > 1 else 0

def check_syntax(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def analyze_code_structure(source_code):
    tree = ast.parse(source_code)
    class_count = 0
    method_count = 0
    top_level_function_count = 0
    class_details = []
    top_level_functions = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            # This is a top-level function (not inside a class)
            function_name = node.name
            lines = (node.end_lineno - node.lineno + 1
                     if hasattr(node, 'end_lineno') else "?")
            top_level_functions.append((function_name, lines))
            top_level_function_count += 1

        elif isinstance(node, ast.ClassDef):
            class_count += 1
            class_name = node.name
            methods = []

            for body_item in node.body:
                if isinstance(body_item, ast.FunctionDef):
                    method_name = body_item.name
                    lines = (body_item.end_lineno - body_item.lineno + 1
                             if hasattr(body_item, 'end_lineno') else "?")
                    methods.append((method_name, lines))
                    method_count += 1

            class_details.append((class_name, methods))

    total_function_count = top_level_function_count + method_count

    print(f"Total Classes: {class_count}")
    print(f"Total Functions: {total_function_count}")
    print(f"Top-level Functions: {top_level_function_count}")
    
    for name, lines in top_level_functions:
        print(f"  Function: {name} ({lines} lines)")

    for class_name, methods in class_details:
        print(f"\nClass: {class_name}")
        print(f"  Number of methods: {len(methods)}")
        for method_name, lines in methods:
            print(f"    Method: {method_name} ({lines} lines)")

    return total_function_count, class_count 


ERROR_WEIGHTS = {
    'E101': 0.5,   # mixed spaces and tabs
    'E111': 0.5,   # indentation not multiple of four
    'E231': 0.2,   # missing whitespace after ','
    'E265': 0.5,   # block comment should start with '# '
    'E302': 0.2,   # expected 2 blank lines, found 1
    'E303': 1,   # too many blank lines
    'E305': 0.5,   # expected 2 blank lines after function definition
    'E501': 1.5,   # line too long
    'W291': 0.75,   # trailing whitespace
    'W292': 0.5,   # no newline at end of file
    'W293': 0.2,   # blank line contains whitespace

    # pyflakes (F)
    'F401': 2,   # module imported but unused
    'F841': 1,   # local variable assigned but never used

    # mccabe (C)
    'C901': 3,   # function is too complex

    # pydocstyle (D)
    'D100': 0.5,   # missing docstring in public module
    'D101': 0.5,   # missing docstring in class
    'D102': 0.5,   # missing docstring in method

    # pep8-naming (N)
    'N802': 0.5,   
    'N803': 0.5,   
    'N806': 0.5,   
}


def run_flake8(file_path):
    result = subprocess.run(['flake8', file_path], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split('\n') if result.stdout.strip() else []



def extract_error_code(line):
    match = re.search(r' ([A-Z]\d{3}) ', line)
    return match.group(1) if match else None


def calculate_weighted_score(flake8_lines, weights):
    total_weight = 0
    error_counts = {}

    for line in flake8_lines:
        code = extract_error_code(line)
        if code:
            weight = weights.get(code, 1)
            total_weight += weight
            error_counts[code] = error_counts.get(code, 0) + 1

    return total_weight, error_counts


def weighted_mean(error_breakdown, weights):
    total_issues = sum(error_breakdown.values())
    if total_issues == 0:
        return 0
    weighted_sum = sum(weights.get(code, 1) * count for code, count in error_breakdown.items())
    return weighted_sum / total_issues


def evaluate_code_quality_2(file_path):
    flake8_output = run_flake8(file_path)
    total_score, error_breakdown = calculate_weighted_score(flake8_output, ERROR_WEIGHTS)
    total_score = 10 - total_score
    print(f"Total Weighted Lint Score out of 10 : {total_score}")


code_file = r'C:\Users\uzair\Desktop\BE Project\Final\temp_script.py' 
if __name__ == "__main__":
    with open(r"C:\Users\uzair\Desktop\BE Project\Final\temp_script.py", "r") as f:
        llm_code = f.read()

    evaluate_code_quality_2(code_file)
    print(f"Code Quality : {evaluate_code_quality(llm_code)}")
    analyze_code_structure(llm_code)
    print(f"Computing Complexity : {compute_complexity(llm_code)} \n ")
    print(f"Checking Redundancy :{check_redundancy(llm_code)}\n")
    print(f"Syntax Validation :{check_syntax(llm_code)} \n")

def visualize_comparison(comparison_results):
    metrics = ["Quality Score", "Complexity", "Redundancy Score"]
    values_code1 = [
        comparison_results["quality_score"][0],
        comparison_results["complexity_score"][0],
        comparison_results["redundancy_score"][0]
    ]
    values_code2 = [
        comparison_results["quality_score"][1],
        comparison_results["complexity_score"][1],
        comparison_results["redundancy_score"][1]
    ]

    x = np.arange(len(metrics))
    width = 0.35 

    fig, ax = plt.subplots(figsize=(8, 5))  # Increase figure size
    bars1 = ax.bar(x - width/2, values_code1, width, label="Code Before Optimization", color="blue")
    bars2 = ax.bar(x + width/2, values_code2, width, label="Code After Optimization", color="green")

    ax.set_xlabel("Evaluation Metrics")
    ax.set_ylabel("Score")
    ax.set_title("Code Comparison: Before vs. After Optimization")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    
    # Move the legend outside the plot
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

    # Annotate bars with values
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', 
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()  # Adjust layout to prevent overlap

    return fig

