import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from readability import understand_requirements, generate_pseudocode, pseudocode_to_code, optimize_code, generate_optimized_prompt
from api_requests_code import call_model_code, extract_python_code
from api_requests_prompt import call_model_prompt
from code_evaluation import evaluate_code_quality, compute_complexity, check_redundancy, check_syntax, visualize_comparison, analyze_code_structure
from get_model_name import get_ollama_models
from memory_utils import ( run_memory_profiler , save_generated_code , parse_memory_dat , 
                        summarize_memory_usage)
from runntimes import final_prompt
import os

st.set_page_config(page_title="RePromptArc", page_icon="📜", layout="centered")
st.title("RePromptArc - AI-Powered Code Assistant")
st.markdown("### Generate, Understand, and Optimize Code with AI")

st.sidebar.image(r"C:\Users\uzair\Desktop\BE Project\Final\Logo.png", width=300)
st.sidebar.title("Navigation")
st.sidebar.info("Use this tool to generate, analyze, and improve code snippets effortlessly.")
st.markdown("### 🔍 Enter Your Coding Problem")

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

if "latest_code" not in st.session_state:
    st.session_state.latest_code = ""

if "latest_eval" not in st.session_state:
    st.session_state.latest_eval = {}

if "optimization_cycle" not in st.session_state:
    st.session_state.optimization_cycle = 0

if "continue_optimizing" not in st.session_state:
    st.session_state.continue_optimizing = False

if "initial_generated" not in st.session_state:
    st.session_state.initial_generated = False


selected_model=None
user_prompt = st.text_area("Describe your coding problem in detail:")
if st.button(" -> Generate Solution"):
    if user_prompt.strip():
        st.session_state.prompt_history = [user_prompt]
        with st.spinner("⚙️ Generating Initial Code..."):
            generated_code = extract_python_code(call_model_code(user_prompt, selected_model))
            code_quality_before = evaluate_code_quality(generated_code)
            code_complexity_before = compute_complexity(generated_code)
            check_syntaxs_before = check_syntax(generated_code)
            check_redundancys_before = check_redundancy(generated_code)
            totfunction1, totclass1 = analyze_code_structure(generated_code)

            st.session_state.latest_code = generated_code
            st.session_state.latest_eval = {
                "quality": code_quality_before,
                "complexity": code_complexity_before,
                "syntax": check_syntaxs_before,
                "redundancy": check_redundancys_before,
            }

            codequal = {
                "quality": code_quality_before,
                "complexity": code_complexity_before,
                "redundancy": check_redundancys_before,
            }

            st.subheader("📝 Initial Code Response")
            st.code(generated_code, language="python")
            st.write("\n=== Evaluation Results ===")
            st.write(f"📊 Total Functions: {totfunction1}")
            st.write(f"📊 Total Classes: {totclass1}")
            st.write(f"✅ Syntax Valid: {check_syntaxs_before}")
            st.write(f"📊 Code Quality (0-10): {code_quality_before:.2f}")
            st.write(f"🚀 Code Complexity: {code_complexity_before}")
            st.write(f"🔄 Redundancy Score (0-1): {check_redundancys_before}")
            try:
                    py_file = "llm_generated_code.py"
                    dat_file = "llm_generated_dat.dat"
                    dat_file = "llm_generated_dat.dat"
                    print("Try running memory profiler")
                    run_memory_profiler("llm_generated_script.py", dat_file, 20)
                    print("Profiler running successfullyS")
                    cmdline, mem, ts = parse_memory_dat(dat_file)
                    summary = summarize_memory_usage(mem, ts)

                    st.subheader("📈 Memory Usage Summary")
                    for key, value in summary.items():
                        st.markdown(f"**{key.replace('_', ' ').title()}**: {value}")

                    st.session_state.latest_eval = {
                        "Minimum Memory": summary["Minimum Memory"],
                        "Maximum Memory": summary["Maximum Memory"],
                        "Average Memory Used": summary["Average Memory Used"],
                        "Memory Increase": summary["Memory Increase"],
                        "Max-Spike in Memory": summary["Max-Spike in Memory"],
                        "Spike TimeStamps": summary["Spike TimeStamps"],
                    }
                    avg_mem = summary["Average Memory Used"]
                    zoom_seconds = 0.1
                    ts = ts - ts[0]
                    mem = np.array(mem)

                    early_mask = ts <= zoom_seconds
                    ts_early = ts[early_mask]
                    mem_early = mem[early_mask]

                    peak_idx = np.argmax(mem_early)
                    peak_time = ts_early[peak_idx]
                    peak_value = mem_early[peak_idx]

                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(ts_early, mem_early, label="Raw Memory", color="blue", linewidth=1)
                    ax.plot(peak_time, peak_value, "ro", label=f"Peak: {peak_value:.2f} MB")

                    ax.set_title(f"Early Memory Spike (First {zoom_seconds} sec)")
                    ax.set_xlabel("Time (s)")
                    ax.set_ylabel("Memory (MB)")
                    ax.legend()
                    ax.grid(True)
                    st.pyplot(fig)

                    os.remove(r"C:\Users\uzair\Desktop\BE Project\Final\llm_generated_script.py")
                    os.remove(r"C:\Users\uzair\Desktop\BE Project\Final\llm_generated_dat.dat")


            except Exception as e:
                    st.error(f"Memory profiling failed: {e}")
                    

        
        # User choice to optimize or continue
        with st.spinner("🧠 Generating an improved prompt..."):
            new_prompt,new_code,summary1,mem,ts = final_prompt(user_prompt, generated_code, summary,avg_mem,codequal) 
        
        st.subheader("🧾 Suggested Improved Prompt")
        edited_prompt = st.text_area("", value=new_prompt, key=f"edit_prompt_{st.session_state.optimization_cycle}")
        optimize_choice = st.radio("✨ Do you want to optimize the code with this prompt?", ("Yes", "No"))

        if optimize_choice == "Yes":
            st.session_state.prompt_history.append(edited_prompt)
            st.session_state.optimization_cycle += 1  # move early
            with st.spinner("🔧 Generating optimized code..."):
                requirements = understand_requirements(edited_prompt, selected_model)
                pseudocode = generate_pseudocode(requirements, selected_model)
                psuedo = pseudocode_to_code(pseudocode, selected_model)
                optimized_code = optimize_code(psuedo, selected_model)
                generated_code_after = extract_python_code(optimized_code)
                code_quality_after = evaluate_code_quality(generated_code_after)
                code_complexity_after = compute_complexity(generated_code_after)
                check_syntaxs_after = check_syntax(generated_code_after)
                check_redundancys_after = check_redundancy(generated_code_after)
                totfunction2, totclass2 = analyze_code_structure(generated_code_after)

                st.subheader("✨ Optimized Code")
                st.code(generated_code_after, language="python")
                st.write("\n=== Evaluation Results ===")
                st.write(f"📊 Total Functions: {totfunction2}")
                st.write(f"📊 Total Classes: {totclass2}")
                st.write(f"✅ Syntax Valid: {check_syntaxs_after}")
                st.write(f"📊 Code Quality (0-10): {code_quality_after:.2f}")
                st.write(f"🚀 Code Complexity: {code_complexity_after}")
                st.write(f"🔄 Redundancy Score (0-1): {check_redundancys_after}")


                st.subheader("📈 Memory Usage Summary")
                for key, value in summary1.items():
                    st.markdown(f"**{key.replace('_', ' ').title()}**: {value}")

                zoom_seconds = 0.1
                ts = ts - ts[0]
                mem = np.array(mem)

                early_mask = ts <= zoom_seconds
                ts_early = ts[early_mask]
                mem_early = mem[early_mask]

                peak_idx = np.argmax(mem_early)
                peak_time = ts_early[peak_idx]
                peak_value = mem_early[peak_idx]

                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(ts_early, mem_early, label="Raw Memory", color="blue", linewidth=1)
                ax.plot(peak_time, peak_value, "ro", label=f"Peak: {peak_value:.2f} MB")

                ax.set_title(f"Early Memory Spike (First {zoom_seconds} sec)")
                ax.set_xlabel("Time (s)")
                ax.set_ylabel("Memory (MB)")
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

                os.remove(r"C:\Users\uzair\Desktop\BE Project\Final\llm_generated_script.py")
                os.remove(r"C:\Users\uzair\Desktop\BE Project\Final\llm_generated_dat.dat")


            comparison = {
                "syntax_valid": (check_syntaxs_before, check_syntaxs_after),
                "quality_score": (code_quality_before, code_quality_after),
                "complexity_score": (code_complexity_before, code_complexity_after),
                "redundancy_score": (check_redundancys_before, check_redundancys_after),
            }

            st.write("📊 Comparison of Initial vs Optimized Code")
            fig = visualize_comparison(comparison)
            st.pyplot(fig)
            def plot_summary_comparison_matplotlib(summary, summary1):
                keys_to_plot = [k for k in summary.keys() 
                if isinstance(summary[k], (int, float)) and k != "Slope"]
                labels = [key.replace("_", " ").title() for key in keys_to_plot]
                initial_values = [summary[k] for k in keys_to_plot]
                optimized_values = [summary1[k] for k in keys_to_plot]

                x = np.arange(len(labels))  # label positions
                width = 0.35  # bar width

                fig, ax = plt.subplots(figsize=(10, 5))
                bars1 = ax.bar(x - width/2, initial_values, width, label='Initial Code', color='skyblue')
                bars2 = ax.bar(x + width/2, optimized_values, width, label='Optimized Code', color='lightgreen')

                ax.set_ylabel('Memory (MB)')
                ax.set_title('📊 Memory Comparison: Initial vs Optimized Code')
                ax.set_xticks(x)
                ax.set_xticklabels(labels, rotation=30, ha='right')
                ax.legend()
                ax.grid(True, axis='y', linestyle='--', alpha=0.7)

                # Annotate bars with values
                for bar in bars1 + bars2:
                    height = bar.get_height()
                    ax.annotate(f'{height:.2f}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=8)

                st.pyplot(fig)
            plot_summary_comparison_matplotlib(summary, summary1)
            st.write("✅ Optimization complete.")
            st.session_state.optimization_cycle += 1
