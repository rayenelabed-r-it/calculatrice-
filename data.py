# Data persistence and file operations
import json
import os
from tkinter import filedialog

# File paths (in app folder)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(SCRIPT_DIR, "history.json")
ERRORS_FILE = os.path.join(SCRIPT_DIR, "errors.json")

# Maximum history entries
MAX_HISTORY = 100

# Default error types
DEFAULT_ERRORS = {
    "division_by_zero": 0,
    "negative_number": 0,
    "integer_required": 0,
    "tangent_undefined": 0,
    "invalid_input": 0,
    "empty_field": 0,
    "no_solution": 0,
    "infinite_solutions": 0,
    "not_quadratic": 0,
    "no_real_solution": 0
}

# Error message to type mapping
ERROR_TYPE_MAP = {
    "Error: division by zero": "division_by_zero",
    "Error: negative number": "negative_number",
    "Error: integer required": "integer_required",
    "Tangent undefined at this value": "tangent_undefined",
    "Invalid input": "invalid_input",
    "Please enter a value": "empty_field",
    "No solution": "no_solution",
    "Infinite solutions": "infinite_solutions",
    "Error: not quadratic": "not_quadratic",
    "No real solution": "no_real_solution"
}

# In-memory storage
_history = []
_errors = {}

# History functions
def load_history():
    global _history
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                _history = json.load(f)
        else:
            _history = []
    except:
        _history = []
    return _history

def save_history():
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(_history, f, indent=2, ensure_ascii=False)
    except:
        pass

def add_history_entry(operation, operands, result):
    from datetime import datetime
    entry = {
        "operation": operation,
        "operands": operands,
        "result": result,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }
    _history.append(entry)
    # Keep only last MAX_HISTORY entries
    while len(_history) > MAX_HISTORY:
        _history.pop(0)
    save_history()

def clear_history():
    global _history
    _history = []
    save_history()

def get_history():
    return _history.copy()

# Error statistics functions
def load_errors():
    global _errors
    try:
        if os.path.exists(ERRORS_FILE):
            with open(ERRORS_FILE, 'r', encoding='utf-8') as f:
                _errors = json.load(f)
            # Ensure all error types exist
            for key in DEFAULT_ERRORS:
                if key not in _errors:
                    _errors[key] = 0
        else:
            _errors = DEFAULT_ERRORS.copy()
    except:
        _errors = DEFAULT_ERRORS.copy()
    return _errors

def save_errors():
    try:
        with open(ERRORS_FILE, 'w', encoding='utf-8') as f:
            json.dump(_errors, f, indent=2, ensure_ascii=False)
    except:
        pass

def increment_error(error_message):
    # Map error message to error type
    error_type = ERROR_TYPE_MAP.get(error_message)
    if error_type and error_type in _errors:
        _errors[error_type] += 1
        save_errors()

def reset_errors():
    global _errors
    _errors = DEFAULT_ERRORS.copy()
    save_errors()

def get_error_counts():
    return _errors.copy()

def get_total_errors():
    return sum(_errors.values())

# Graph export function
def export_graph(figure):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Save Graph As"
    )
    if file_path:
        figure.savefig(file_path, dpi=100, bbox_inches='tight')
        return True
    return False
