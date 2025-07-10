import subprocess
import numpy as np
from sklearn.linear_model import LinearRegression

def save_generated_code(code_str, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code_str)


import subprocess

def run_memory_profiler(script_path, dat_output_path, max_execution_time):
    py_file = "llm_generated_script.py"
    bash_exe = "C:\\Program Files\\Git\\bin\\bash.exe"
    shell_script = "run_code.sh"

    with open("temp_script.py", "r", encoding="utf-8") as file:
        generated_code = file.read()

    generated_code = "import time\n" + generated_code + "\n" + "time.sleep(25)"

    with open(py_file, "w", encoding="utf-8") as f:
        f.write(generated_code)

    print(f"Running: {bash_exe} {shell_script} {py_file} {dat_output_path} {max_execution_time}")
    print("Types:", type(py_file), type(dat_output_path), type(max_execution_time))

    try:
        process = subprocess.run(
            [bash_exe, shell_script, py_file, dat_output_path, str(max_execution_time)],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        print("✅ Script executed successfully:")
        return dat_output_path

    except subprocess.CalledProcessError as e:
        print("❌ Script failed!")
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)

def parse_memory_dat(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    cmdline = ""
    memory = []
    timestamps = []

    for line in lines:
        if line.startswith("CMDLINE"):
            cmdline = line.strip().replace("CMDLINE ", "")
        elif line.startswith("MEM"):
            parts = line.strip().split()
            memory.append(float(parts[1]))
            timestamps.append(float(parts[2]))

    return cmdline, np.array(memory), np.array(timestamps)

def summarize_memory_usage(memory, timestamps):
    mem_diff = np.diff(memory)
    spike_indices = np.where(mem_diff > np.mean(mem_diff) + 2 * np.std(mem_diff))[0]

    summary = {
        "Minimum Memory": float(np.min(memory)),
        "Maximum Memory": float(np.max(memory)),
        "Average Memory Used": float(np.mean(memory)),
        "Memory Increase": float(memory[-1] - memory[0]),
        "Max-Spike in Memory": float(np.max(mem_diff)) if len(mem_diff) > 0 else 0,
        "Spike TimeStamps": timestamps[spike_indices].tolist() if len(spike_indices) else [],
    }

    # Memory usage trend
    X = timestamps.reshape(-1, 1)
    y = memory
    model = LinearRegression().fit(X, y)
    summary["slope"] = float(model.coef_[0])

    return summary

def generate_prompt(generated_code_after , cmdline, summary):
    return f"""
You are a code optimization assistant.

Memory profiling was run on a Python script :
{generated_code_after}
with the following command:
{cmdline}

Here is a memory usage summary:
- Min Memory: {summary['min_mem']:.2f} MB
- Max Memory: {summary['max_mem']:.2f} MB
- Average Memory: {summary['avg_mem']:.2f} MB
- Total Increase: {summary['mem_increase']:.2f} MB
- Memory Growth Rate: {summary['slope']:.4f} MB/sec
- Max Single Spike: {summary['max_spike_value']:.2f} MB
- Spike Timestamps: {summary['spike_timestamps']}

Tasks:
1. Identify if memory behavior is normal or inefficient.
2. Suggest any potential causes.
3. Recommend optimizations to reduce the memory usage and decrease the Code Complexity
""".strip()

# with open("temp_script.py", "r", encoding="utf-8") as file:
#     generated_code = file.read()
# generated_code = "import time " + "\n" + generated_code + "\n" + "time.sleep(25)"

# py_file = "llm_generated_script.py"
# dat_file = "llm_generated_script.dat"

# with open(py_file, "w", encoding="utf-8") as f:
#     f.write(generated_code)

# save_generated_code(generated_code, f"{py_file}")

# run_memory_profiler(py_file, dat_file, 30)

# # 3. Summarize memory
# cmdline, mem, ts = parse_memory_dat(f"{dat_file}")
# summary = summarize_memory_usage(mem, ts)
