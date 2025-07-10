import ast
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from io import StringIO
import radon.complexity
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


def evaluate_code_quality(code):

    with open("temp_script.py", "w") as f:
        f.truncate(0)

    with open("temp_script.py", "w") as f:
        f.write(code)

    output = StringIO()
    reporter = TextReporter(output)
    Run(["temp_script.py"], reporter=reporter, exit=False)

    output.seek(0)
    report = output.read()

    for line in report.splitlines():
        if "Your code has been rated at" in line:
            try:
                print(float(line.split()[6].split("/")[0]) )
                return float(line.split()[6].split("/")[0])  
            except:
                return 0.0  

    return 0.0  



def compute_complexity(code):
    try:
        results = radon.complexity.cc_visit(code)
        print(sum(block.complexity for block in results))
        return sum(block.complexity for block in results)
    except Exception:
        return -1  


def check_redundancy(code):
    lines = code.strip().split("\n")
    unique_lines = set(lines)

    redundancy_score = 1 - (len(unique_lines) / len(lines))
    print(round(redundancy_score, 2))
    return round(redundancy_score, 2) if len(lines) > 1 else 0


def check_syntax(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

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




