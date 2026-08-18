import os
import sys
import runpy

script_to_trace_path = "XipppyServerLSTM.py"

def targeted_trace(frame, event, arg):
    if event == "call":
        file_path = frame.f_code.co_filename

        # Use the variable you defined instead of a hardcoded "my_script.py"
        is_main_script = script_to_trace_path in file_path  
        is_custom_pkg = os.path.join("site-packages", "feedbackdecode") in file_path

        if is_main_script or is_custom_pkg:
            func_name = frame.f_code.co_name
            line_no = frame.f_lineno
            print(f"[TRACE] Call to {func_name}() on line {line_no} in {file_path}")

    return targeted_trace

# Activate tracing
sys.settrace(targeted_trace)

try:
    # runpy executes the script in the CURRENT process, so the trace applies
    runpy.run_path(script_to_trace_path, run_name="__main__")
finally:
    # Always turn off the trace when done to prevent performance degradation
    sys.settrace(None)
