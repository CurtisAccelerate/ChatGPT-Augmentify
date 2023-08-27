import nbformat as nbf
from nbclient import NotebookClient
import io
import sys
import platform
import os
import shutil
from nbconvert.preprocessors import ExecutePreprocessor
from contextlib import redirect_stdout, redirect_stderr, ExitStack

# Define paths for the work directory and files
WORK_DIR = "Work"
TEMPLATE_FILE = os.path.join(WORK_DIR, "template.py")
TARGET_PATH = os.path.join(WORK_DIR, "work.py")

# If the target Python file doesn't exist, copy the template
if not os.path.exists(TARGET_PATH):
    shutil.copyfile(TEMPLATE_FILE, TARGET_PATH)

# History of code and results
code_history = []

# Define global state for executed code
exec_globals = {}

def load_and_execute_file(file_path):
    global exec_globals
    with open(file_path, 'r') as f:
        code = f.read()
    exec(code, exec_globals)

# Load the 'work.py' file
load_and_execute_file(TARGET_PATH)

def execute_code(code):
    global exec_globals

    # Append the code to work.py
    with open(TARGET_PATH, 'a', encoding='utf-8') as f:
        f.write("\n# User Code\n" + code + "\n")

    # Execute the code and capture the result using the simplified function
    result = execute_code_simplified(code)

    # Store the result in history
    entry = {"code": code, "result": result}
    code_history.append(entry)

    # Mirror work.py to a Jupyter notebook format
    with open(TARGET_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    nb = nbf.v4.new_notebook()
    for line in content.split("\n"):
        cell = nbf.v4.new_code_cell(source=line)
        nb.cells.append(cell)

    with open(os.path.join(WORK_DIR, "augmented_work_01.ipynb"), 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

    return {"result": result, "id": len(code_history) - 1}

# Your simplified execute code function
def execute_code_simplified(code):
    global exec_globals

    # Execute the code for side effects using exec
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        try:
            exec(code, exec_globals)
                                    
            printed_output = output_buffer.getvalue().strip()

            # Evaluate the last line of the code to capture its result (if any)
            last_line = code.strip().split('\n')[-1]
            result_value = eval(last_line, exec_globals)

            # If there's printed output, prioritize that
            if printed_output:
                result = printed_output
            # Otherwise, return the result of the last statement
            elif result_value is not None:
                result = str(result_value)
            else:
                result = "None"
                
        except Exception as e:
            result = str(e).strip()

    return result

# Additional utility functions from the old version

def server_status():
    """
    Returns the status of the server.
    """
    VERSION = "1.0.0"
    return {"status": "Server is running", "version": str(VERSION), "message": "Welcome to the Python execution server!"}

def hello_world():
    """
    Returns a basic hello world message.
    """
    return "Hello, world!"

def get_history():
    """
    Returns the execution history.
    """
    return {"history": code_history}

def restart_kernel():
    """
    Restarts the kernel and clears the notebook.
    """
    global current_notebook
    current_notebook = nbf.v4.new_notebook()
    return {"status": "Kernel restarted and notebook cleared"}

def get_post(id):
    """
    Retrieves a specific post from the history.
    """
    if 0 <= id < len(code_history):
        return code_history[id]
    else:
        return {"error": "ID not found"}, 404
