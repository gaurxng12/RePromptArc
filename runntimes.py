from new_score import evaluate_code_quality
from api_requests_code import call_model_code, extract_python_code
from api_requests_prompt import call_model_prompt
from memory_utils import ( run_memory_profiler , save_generated_code , parse_memory_dat , 
                        summarize_memory_usage)
from readability import understand_requirements, generate_optimized_prompt
from code_evaluation import evaluate_code_quality, compute_complexity, check_redundancy, check_syntax, visualize_comparison, analyze_code_structure

def final_prompt(ini_prompt,ini_code,ini_summary,avg_mem,codequal):
    selected_model = None
    #iteration1
    print("Iterationnnn 11")
    prompt1 = generate_optimized_prompt(
                prev_prompt=ini_prompt,
                code=ini_code,
                evaluation_results=ini_summary,
                code_qual=codequal,
                model_name=None
            )
    code1 = extract_python_code(call_model_code(prompt1, selected_model))
    eval1 = evaluate_code_quality(code1)
    quality1=evaluate_code_quality(code1)
    complexity1=compute_complexity(code1)
    redundancy1=check_redundancy(code1)
    codequal1={
            "quality": quality1,
            "complexity": complexity1,
            "redundancy": redundancy1,
    }
    try:
        py_file = "llm_generated_code.py"
        dat_file = "llm_generated_dat.dat"
        dat_file = "llm_generated_dat.dat"
        print("Try running memory profiler")
        run_memory_profiler("llm_generated_script.py", dat_file, 20)
        print("Profiler running successfullyS")
        cmdline, mem, ts = parse_memory_dat(dat_file)
        summary1 = summarize_memory_usage(mem, ts)
        print("Memory 1 ")
        print(summary1["Average Memory Used"])
        if summary1["Average Memory Used"] < avg_mem:
            return prompt1,code1,summary1,mem,ts
    except Exception as e:
                    st.error(f"Memory profiling failed: {e}")

    #iteration2
    print("Iterationnnn 22")
    prompt2 = generate_optimized_prompt(
        prev_prompt=prompt1,
        code=code1,
        evaluation_results=summary1,
        code_qual=codequal1,
        model_name=None
    )
    code2 = extract_python_code(call_model_code(prompt2, selected_model))
    eval2 = evaluate_code_quality(code2)
    quality2=evaluate_code_quality(code2)
    complexity2=compute_complexity(code2)
    redundancy2=check_redundancy(code2)
    codequal2={
        "quality": quality2,
        "complexity": complexity2,
        "redundancy": redundancy2,
    }
    try:
        py_file = "llm_generated_code.py"
        dat_file = "llm_generated_dat.dat"
        dat_file = "llm_generated_dat.dat"
        print("Try running memory profiler")
        run_memory_profiler("llm_generated_script.py", dat_file, 20)
        print("Profiler running successfullyS")
        cmdline, mem, ts = parse_memory_dat(dat_file)
        summary2 = summarize_memory_usage(mem, ts)
        print("Memory 2 ")
        print(summary2["Average Memory Used"])
        if summary2["Average Memory Used"] < avg_mem:
            return prompt2,code2,summary2,mem,ts
    except Exception as e:
                    st.error(f"Memory profiling failed: {e}")


    #iteration3
    print("Iterationnnn 33")
    prompt3 = generate_optimized_prompt(
        prev_prompt=prompt2,
        code=code2,
        evaluation_results=summary2,
        code_qual=codequal2,
        model_name=None
    )
    code3 = extract_python_code(call_model_code(prompt3, selected_model))
    eval3 = evaluate_code_quality(code3)
    try:
        py_file = "llm_generated_code.py"
        dat_file = "llm_generated_dat.dat"
        dat_file = "llm_generated_dat.dat"
        print("Try running memory profiler")
        run_memory_profiler("llm_generated_script.py", dat_file, 20)
        print("Profiler running successfullyS")
        cmdline, mem, ts = parse_memory_dat(dat_file)
        summary3 = summarize_memory_usage(mem, ts)
        print("Memory 3 ")
        print(summary3["Average Memory Used"])
    except Exception as e:
                    st.error(f"Memory profiling failed: {e}")
    return prompt3,code3,summary3,mem,ts