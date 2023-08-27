#!/usr/bin/env python
# coding: utf-8

# # Mecha Corp Beta
# Mecha Corp augments ChatGPT with ability to run code locally. 
# This is the augmentation file which is also a work file. You may start with it as a template.
# 
# **Warning: There is no code containment. Be extremely careful. Run at own risk! Do not use for 
# production. Not responsible for any damages. **
# 
# This file combined local ChatGPT server and tampermonkey script allows ChatGPT to run code. ALl code is stored into this Notebook.  In addition to being able to write client-side code, a special augemented capability structure has been created to enable ChatGPT to efficiently parse pre-packaged / augmented capabilities. 
# 
# This file serves both as an augmented capabilities extension and client-side work code. It is anticipated one use it like a template. There's not a linking mechanism though for chats yet but in future the augmented may be a template and a new notebook created for each chat from the template. 
# 
# ## Why Client Side Code?
# 
# 1. Extend its's capabilities by adding persistent capabilities
# 2. Accesss to any and all Python modules / functions
# 3. Create more efficient work flows. Example, it can create the entire file system for a project vs. copy/paste. 
# 4. Ability to parse local data / large data without having to zip it.
# 5. Capture workflow better and other many other benefits.
# 
# 
# ## High Level Overview:
# 
# ### ChatGPT Client
# Custom TamperMonkey Script
# Custom prompt
#  
# ## ChatGPT Server
# A Python script running in a Flask service
# 
# ## Augmented Capabilities
# This Notebook.
# 
# 
# # Capabilities:
# 1. Augmented engine structure for creating and getting augmented capabilities in a standardized way vs temporary work functions.
# 2. Task manage / to-do lists for state tracking
# 3. Logging capability for large file processing and "memory tracking"
# 4. Preview file capabilities 
# 4. Prompt / Instruction Chains
# 
# 
# ## To Do Add More Capabiltiies
# 1. Add web scraping capability for general research assistant.
# 2. Add document store / stacks for research.
# 3. Create capability to ask an "out of context" AI queries for multi-modal like ChatGPT, Bard, llama code,
# etc for error correction
# 4. Add new capabilities like voice
# 5. Add streaming and recording for automatic creation local markdowns
# 6. Add project creation automation for files system creation


import pickle
import os
import inspect
import datetime
from typing import Optional, Literal, List, Union




# Dictionary to store metadata of the augmented functions
augmented_functions = {}

def augmented_capability(func=None, *, description=None, example=None):
    """
    Decorator to register functions as augmented capabilities.
    """
    if func is None:
        # This means the decorator was used with arguments
        return lambda f: augmented_capability(f, description=description, example=example)

    # Use provided metadata or extract from docstring
    if func.__doc__:
        if not description:
            description = func.__doc__.split("\n")[1].strip()
        if not example and 'Example:' in func.__doc__:
            example_start = func.__doc__.index('Example:') + 8
            example = func.__doc__[example_start:].strip()
    else:
        if not description:
            description = 'Description not provided.'
        if not example:
            example = 'No example provided.'
    
    # Extracting possible values from type hints
    hints = inspect.getfullargspec(func).annotations
    for arg, arg_type in hints.items():
        if hasattr(arg_type, '__origin__') and arg_type.__origin__ is Union:
            # Extracting literal values
            literals = [t.__args__[0] for t in arg_type.__args__ if hasattr(t, '__origin__') and t.__origin__ is Literal]
            if literals:
                description += f" Possible values for '{arg}': {', '.join(map(str, literals))}."
    
    augmented_functions[func.__name__] = {
        'description': description,
        'example': example
    }
    return func


@augmented_capability
def get_all_augmented_capabilities():
    """
    Retrieve metadata of all augmented capabilities.
    
    Example:
    ```
    capabilities = get_all_augmented_capabilities()
    for cap in capabilities:
        print(cap['name'])
        print(cap['signature'])
        print(cap['description'])
        print(cap['example'])
    ```
    """
    capabilities_list = []
    for func_name, meta in augmented_functions.items():
        # Default values in case some metadata is missing
        description = meta.get('description', 'Description not provided.')
        example = meta.get('example', 'No example provided.')
        
        # Fetch the function signature
        func = globals().get(func_name)
        signature = 'Signature not available.'
        if func:
            try:
                signature = str(inspect.signature(func))
            except ValueError:
                pass
        
        capabilities_list.append({
            'name': func_name,
            'signature': signature,
            'description': description,
            'example': example
        })
    return capabilities_list



# Add task and sub task tracking

import pickle
import os

# Define the storage path inside the data folder
STORAGE_PATH = os.path.join(os.getcwd(), 'task_storage.pkl')

# In-memory tasks storage
tasks = []
current_task = None  # To keep track of the current task

# Load tasks from persistent storage
@augmented_capability(description="Load tasks from storage.")
def load_tasks():
    global tasks, current_task
    try:
        with open(STORAGE_PATH, 'rb') as file:
            data = pickle.load(file)
            tasks = data.get('tasks', [])
            current_task = data.get('current_task')
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        tasks = []
        current_task = None

# Save tasks to persistent storage
def save_tasks():
    with open(STORAGE_PATH, 'wb') as file:
        data = {
            'tasks': tasks,
            'current_task': current_task
        }
        pickle.dump(data, file)

@augmented_capability(description="Add a new task to the task list.", example="add_task('My New Task')")
def add_task(title, status="pending", level=1):
    task = {
        'title': title,
        'status': status,
        'level': level
    }
    tasks.append(task)
    save_tasks()
    return f"Task '{title}' added successfully!"

@augmented_capability(description="Mark a task as completed.", example="mark_task_completed('My New Task')")
def mark_task_completed(title):
    for task in tasks:
        if task['title'] == title:
            task['status'] = "completed"
            save_tasks()
            return f"Task '{title}' marked as completed!"
    return f"Task '{title}' not found!"

@augmented_capability(description="Set a task as the current task.", example="set_current_task('My New Task')")
def set_current_task(title):
    global current_task
    for task in tasks:
        if task['title'] == title:
            current_task = title
            save_tasks()
            return f"Task '{title}' set as current!"
    return f"Task '{title}' not found!"

@augmented_capability(description="Display tasks in a hierarchical format.", example="display_tasks()")
def display_tasks():
    task_representation = []
    for task in tasks:
        checkbox = "[x]" if task['status'] == "completed" else "[ ]"
        indentation = "  " * (task['level'] - 1)
        if task['title'] == current_task:
            task_repr = f"{indentation}* {checkbox} {task['title']}"
        else:
            task_repr = f"{indentation}{checkbox} {task['title']}"
        task_representation.append(task_repr)
    return "\n".join(task_representation)

@augmented_capability(description="Retrieve all tasks.", example="get_tasks()")
def get_tasks():
    return tasks

@augmented_capability(description="Update task details.", example="update_task('Old Task', 'New Task', status='completed')")
def update_task(old_title, new_title, status=None):
    for task in tasks:
        if task['title'] == old_title:
            task['title'] = new_title
            if status:
                task['status'] = status
            save_tasks()
            return f"Task '{old_title}' updated to '{new_title}'!"
    return f"Task '{old_title}' not found!"

@augmented_capability(description="Add multiple tasks from a list, including sub-tasks.", example="add_tasks_from_list('[ ] Task 1\\n  [ ] Sub-task 1.1\\n[ ] Task 2')")
def add_tasks_from_list(task_list):
    current_level = 0
    for line in task_list.split("\n"):
        stripped_line = line.strip()
        if not stripped_line:  # Empty lines
            continue
        indentation = len(line) - len(stripped_line)
        level = (indentation // 3) + 1  # Assuming 3 spaces for sub-level indentation
        task_title = stripped_line[3:].strip()  # Exclude '[ ]' and extra spaces
        
        if level > current_level:
            add_task(task_title, status="pending", level=level)
            current_level = level
        elif level == current_level:
            add_task(task_title, status="pending", level=level)
        else:
            add_task(task_title, status="pending", level=level)
            current_level = level
    save_tasks()

    return "Tasks added successfully!"

# Initialization: Load tasks when the system starts
load_tasks()


# Define the storage path for the logger
LOGGER_STORAGE_PATH_TXT = os.path.join(os.getcwd(), 'task_logger.txt')

def write_log_to_txt(task_name, message):
    """
    Write a log entry to the text file.
    """
    with open(LOGGER_STORAGE_PATH_TXT, 'a') as file:
        file.write(f"{task_name}\n")
        file.write(f"{message}\n\n")

@augmented_capability(description="Add a log entry for a task.", example="log_task_txt('Reading File', 'Successfully read chunk 1/10')")
def log_task_txt(task_name, message):
    """
    Log a task message to a text file.
    :param task_name: Name of the task.
    :param message: Message or summary associated with the task.
    """
    write_log_to_txt(task_name, message)
    return f"Log entry added for task '{task_name}' in text file."

@augmented_capability(description="Retrieve the task logger in text format.", example="get_task_logger_txt()")
def get_task_logger_txt():
    """
    Retrieve the log entries from the text file.
    """
    try:
        with open(LOGGER_STORAGE_PATH_TXT, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "No logs found."

# Ensure to initialize the text log file if not present
if not os.path.exists(LOGGER_STORAGE_PATH_TXT):
    with open(LOGGER_STORAGE_PATH_TXT, 'w') as file:
        file.write("Task Logger\n\n")  # Initial header

# On initialization, we'll add a timestamped log entry
log_task_txt("Init", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Add File Preview Capabilites
@augmented_capability(description="Preview a file's contents.", example="preview_file('path/to/file.txt')")
def preview_file(file_path: str, preview_type: Optional[Union[Literal['lines'], Literal['characters']]] = 'lines', n: Optional[int] = 10) -> str:
    """
    Preview a file's contents.
    :param file_path: Path to the file.
    :param preview_type: Type of preview ('lines' or 'characters'). 
    :param n: Number of lines or characters to preview.
    """
    try:
        with open(file_path, 'r') as file:
            if preview_type == 'lines':
                return "".join([file.readline() for _ in range(n)])
            elif preview_type == 'characters':
                return "\n".join([line[:n] for line in file.readlines()[:n]])
    except FileNotFoundError:
        return f"File '{file_path}' not found!"


file_positions = {}  # Store the last read position for each file
file_chunks_info = {}  # Store total chunks information for each file
last_chunk_size = {}  # Store the last chunk size used for each file


@augmented_capability(description="Read a file in chunks.", example="read_file_in_chunks('path/to/large_file.txt', chunk_size=1024, reset=False)")
def read_file_in_chunks(file_path, chunk_size=1024, reset=False):
    """
    Read a file in chunks.
    :param file_path: Path to the file.
    :param chunk_size: Size of each chunk in bytes.
    :param reset: Whether to start reading from the beginning of the file.
    """
    global file_positions, file_chunks_info, last_chunk_size
    
    # Check if chunk size has changed or if the reset flag is True
    if reset or (file_path in last_chunk_size and last_chunk_size[file_path] != chunk_size):
        file_positions[file_path] = 0
        last_chunk_size[file_path] = chunk_size

    # If we've never read this file before, initialize its positions and last chunk size
    if file_path not in file_positions:
        file_positions[file_path] = 0
    if file_path not in last_chunk_size:
        last_chunk_size[file_path] = chunk_size

    # Calculate total chunks if not done before
    if file_path not in file_chunks_info:
        total_size = os.path.getsize(file_path)
        total_chunks = total_size // chunk_size
        total_chunks += 1 if total_size % chunk_size else 0
        file_chunks_info[file_path] = total_chunks

    current_chunk = file_positions[file_path] // chunk_size + 1
    
    try:
        with open(file_path, 'r') as file:
            # Move to the last read position
            file.seek(file_positions[file_path])
            data = file.read(chunk_size)
            
            # Update the position
            file_positions[file_path] = file.tell()
            
            # If we've reached the end of the file
            if not data:
                file_positions[file_path] = 0  # Reset for next read
                return f"Finished reading the file. {current_chunk}/{file_chunks_info[file_path]} chunks read. Starting from the beginning in the next read."
            
            return f"*** {current_chunk}/{file_chunks_info[file_path]} ***\n{data}"
    except FileNotFoundError:
        return f"File '{file_path}' not found!"



prompt_chains_content = """
Name: ConvertCode
Objective: Convert code from one language to another
Prompt: Read the code carefully. Do not attempt to convert line by line but focus on the most salient and important points for reconstruction.
Instructions:
    1. Read the C# file in chunks.
    2. Log each chunk.
    3. Summarize each chunk.
    4. Convert chunk from C# to Python.
    5. Log the Python conversion.
"""
prompt_chains_path = os.path.join(os.getcwd(), 'prompt_chains.txt')

# Write to prompt_chains.txt only if it doesn't exist
if not os.path.exists(prompt_chains_path):
    with open(prompt_chains_path, 'w') as file:
        file.write(prompt_chains_content)

# Update the function to load prompt chains based on the new format
def load_prompt_chains():
    chains = []
    try:
        with open(prompt_chains_path, 'r') as file:
            lines = file.readlines()
            current_chain = None
            in_instructions = False  # A flag to denote if we are within an Instructions block
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("Name:"):
                    if current_chain:  # Append the previous chain before starting a new one
                        chains.append(current_chain)
                    current_chain = {}
                    current_chain["name"] = stripped.split(":")[1].strip()
                    in_instructions = False
                elif stripped.startswith("Objective:"):
                    current_chain["objective"] = stripped.split(":")[1].strip()
                elif stripped.startswith("Prompt:"):
                    current_chain["prompt"] = stripped.split(":")[1].strip()
                elif stripped.startswith("Instructions:"):
                    in_instructions = True
                    current_chain["instructions"] = []
                elif in_instructions and not stripped.startswith("Name:") and stripped:
                    current_chain["instructions"].append(stripped)
                elif not in_instructions and stripped.startswith("Name:"):
                    in_instructions = False  # End of instructions for the previous chain
            if current_chain:  # Append the last chain after the loop
                chains.append(current_chain)
    except (FileNotFoundError, IndexError, KeyError):
        pass  # Handle errors silently and return the chains parsed until the error
    return chains



# Updated list_prompt_chains function to include modes
@augmented_capability(description="List available prompt chains.", example="list_prompt_chains(mode='verbose')")
def list_prompt_chains(mode='brief'):
    chains = load_prompt_chains()
    if mode == 'brief':
        return [{"name": chain["name"], "objective": chain.get("objective", "")} for chain in chains]
    elif mode == 'verbose':
        return chains
    else:
        return "Invalid mode. Use 'brief' or 'verbose'."

# Define a function to get a specific prompt chain by its name
@augmented_capability(description="Retrieve a specific prompt chain by its name.", example="get_prompt_chain('ConvertCode')")
def get_prompt_chain(chain_name):
    chains = load_prompt_chains()
    for chain in chains:
        if chain["name"] == chain_name:
            return chain
    return f"No prompt chain found with the name {chain_name}."


# Function to update a specific prompt chain by its name

@augmented_capability(description="Update a specific prompt chain.", example="update_prompt_chain('ConvertCode', new_objective='Convert C# to Python', new_prompt='Read C# code, convert to Python.')")
def update_prompt_chain(name, new_name=None, new_objective=None, new_prompt=None, new_instructions=None):
    chains = load_prompt_chains()
    
    # Find the chain to update
    chain_to_update = None
    for chain in chains:
        if chain["name"] == name:
            chain_to_update = chain
            break
    
    # If chain not found, return an error
    if not chain_to_update:
        return f"No prompt chain found with the name {name}."
    
    # Update the chain details
    if new_name:
        chain_to_update["name"] = new_name
    if new_objective:
        chain_to_update["objective"] = new_objective
    if new_prompt:
        chain_to_update["prompt"] = new_prompt
    if new_instructions:
        chain_to_update["instructions"] = new_instructions
    
    # Write the updated chains back to the file
    with open(prompt_chains_path, 'w') as file:
        for chain in chains:
            file.write(f"Name: {chain['name']}\n")
            file.write(f"Objective: {chain.get('objective', '')}\n")
            file.write(f"Prompt: {chain.get('prompt', '')}\n")
            file.write("Instructions:\n")
            for instruction in chain.get('instructions', []):
                file.write(f"    {instruction}\n")
            file.write("\n")
    
    return f"Prompt chain '{name}' updated successfully."


# Client Work

