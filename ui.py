# Tkinter interface and user interaction
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import core
import data

# Color scheme
COLOR_HEADER = "#a2e0db"      # Teal
COLOR_BACKGROUND = "#fee1d3"  # Peach
COLOR_ERROR = "#f55e55"       # Coral Red
COLOR_PRIMARY = "#ff857a"     # Salmon
COLOR_VALID = "#a2e0db"       # Teal (for results)
COLOR_TEXT_DARK = "#2c3e50"   # Dark text
COLOR_TEXT_SECONDARY = "#7f8c8d"  # Gray timestamps
COLOR_INPUT_BG = "white"

# Global references for tab switching
notebook = None
tab_calculator = None
calculator_inputs = {}

def create_interface():
    global notebook, tab_calculator

    # Load persisted data
    data.load_history()
    data.load_errors()

    root = tk.Tk()
    root.title("Math Calculator")
    root.geometry("1200x700")
    root.configure(bg=COLOR_BACKGROUND)

    # Header
    header_frame = tk.Frame(root, bg=COLOR_HEADER, height=60)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    title = tk.Label(header_frame, text="Math Calculator",
                    font=("Arial", 18, "bold"), fg=COLOR_TEXT_DARK, bg=COLOR_HEADER)
    title.pack(expand=True)

    # Main container with PanedWindow
    main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg=COLOR_TEXT_DARK,
                                 sashwidth=6, sashrelief=tk.RAISED)
    main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Left side: Notebook with Calculator and Graphs
    left_frame = tk.Frame(main_paned, bg=COLOR_BACKGROUND)
    main_paned.add(left_frame, minsize=400)

    # Style configuration
    style = ttk.Style()
    style.configure("TNotebook", background=COLOR_BACKGROUND)
    style.configure("TNotebook.Tab", padding=[15, 5])

    notebook = ttk.Notebook(left_frame)
    notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Tab 1: Calculator
    tab_calculator = tk.Frame(notebook, bg=COLOR_BACKGROUND)
    notebook.add(tab_calculator, text="  Calculator  ")
    create_calculator_tab(tab_calculator)

    # Tab 2: Graphs
    tab_graphs = tk.Frame(notebook, bg=COLOR_BACKGROUND)
    notebook.add(tab_graphs, text="  Graphs  ")
    create_graphs_tab(tab_graphs)

    # Right side: Sidebar with History and Statistics
    sidebar_frame = tk.Frame(main_paned, bg=COLOR_BACKGROUND)
    main_paned.add(sidebar_frame, minsize=250)

    create_sidebar(sidebar_frame)

    # Set initial sash position
    root.update()
    main_paned.sash_place(0, 850, 0)

    root.mainloop()

def create_sidebar(parent):
    # Scrollable sidebar
    canvas = tk.Canvas(parent, bg=COLOR_BACKGROUND, highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLOR_BACKGROUND)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Make scrollable frame expand to canvas width
    def configure_frame_width(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", configure_frame_width)

    # Linux mouse wheel support for sidebar
    def on_mousewheel_linux(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
    canvas.bind("<Button-4>", on_mousewheel_linux)
    canvas.bind("<Button-5>", on_mousewheel_linux)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # History Section
    create_sidebar_history(scrollable_frame)

    # Separator
    separator = tk.Frame(scrollable_frame, bg=COLOR_TEXT_DARK, height=2)
    separator.pack(fill=tk.X, padx=10, pady=10)

    # Statistics Section
    create_sidebar_statistics(scrollable_frame)

def create_sidebar_history(parent):
    global history_frame_ref

    # Header
    header_frame = tk.Frame(parent, bg=COLOR_BACKGROUND)
    header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

    tk.Label(header_frame, text="History", font=("Arial", 12, "bold"),
            bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).pack(side=tk.LEFT)

    def clear_all():
        if messagebox.askyesno("Confirm", "Are you sure?"):
            data.clear_history()
            refresh_history()

    tk.Button(header_frame, text="Clear", font=("Arial", 9),
             bg=COLOR_ERROR, fg="white", command=clear_all).pack(side=tk.RIGHT)

    # History list container
    history_container = tk.Frame(parent, bg=COLOR_BACKGROUND)
    history_container.pack(fill=tk.X, padx=5)

    history_frame_ref = history_container
    refresh_history()

def create_sidebar_statistics(parent):
    global stats_frame_ref

    # Header
    header_frame = tk.Frame(parent, bg=COLOR_BACKGROUND)
    header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

    tk.Label(header_frame, text="Statistics", font=("Arial", 12, "bold"),
            bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).pack(side=tk.LEFT)

    def reset_all():
        if messagebox.askyesno("Confirm", "Are you sure?"):
            data.reset_errors()
            refresh_stats()

    tk.Button(header_frame, text="Reset", font=("Arial", 9),
             bg=COLOR_ERROR, fg="white", command=reset_all).pack(side=tk.RIGHT)

    # Total errors display
    total_frame = tk.Frame(parent, bg=COLOR_HEADER)
    total_frame.pack(fill=tk.X, padx=10, pady=5)

    total_label = tk.Label(total_frame, text="", font=("Arial", 12, "bold"),
                          bg=COLOR_HEADER, fg=COLOR_TEXT_DARK)
    total_label.pack(pady=5)

    # Stats list container
    stats_container = tk.Frame(parent, bg=COLOR_BACKGROUND)
    stats_container.pack(fill=tk.X, padx=5)

    stats_frame_ref = (stats_container, total_label)
    refresh_stats()

# Calculator Tab
def create_calculator_tab(parent):
    global calculator_inputs

    # Scrollable canvas
    canvas = tk.Canvas(parent, bg=COLOR_BACKGROUND, highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLOR_BACKGROUND)

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Linux mouse wheel support
    def on_mousewheel_linux(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
    canvas.bind_all("<Button-4>", on_mousewheel_linux)
    canvas.bind_all("<Button-5>", on_mousewheel_linux)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Create all section frames
    section_frames = []

    # Section 1: Basic Operations
    frame_basic = tk.LabelFrame(scrollable_frame, text="Basic Operations",
                                font=("Arial", 12, "bold"), bg=COLOR_BACKGROUND,
                                fg=COLOR_TEXT_DARK, padx=10, pady=10)
    create_operation_2_inputs(frame_basic, "Addition (+)", core.addition, "addition")
    create_operation_2_inputs(frame_basic, "Subtraction (-)", core.subtraction, "subtraction")
    create_operation_2_inputs(frame_basic, "Multiplication (*)", core.multiplication, "multiplication")
    create_operation_2_inputs(frame_basic, "Division (/)", core.division, "division")
    create_operation_2_inputs(frame_basic, "Power (^)", core.power, "power")
    create_operation_2_inputs(frame_basic, "Modulo (%)", core.modulo, "modulo")
    section_frames.append(frame_basic)

    # Section 2: Roots & Factorial
    frame_roots = tk.LabelFrame(scrollable_frame, text="Roots & Factorial",
                                font=("Arial", 12, "bold"), bg=COLOR_BACKGROUND,
                                fg=COLOR_TEXT_DARK, padx=10, pady=10)
    create_operation_1_input(frame_roots, "Square Root", core.square_root, "square_root")
    create_operation_1_input(frame_roots, "Cube Root", core.cube_root, "cube_root")
    create_operation_1_input(frame_roots, "Factorial (n!)", core.factorial, "factorial")
    section_frames.append(frame_roots)

    # Section 3: Trigonometry
    frame_trig = tk.LabelFrame(scrollable_frame, text="Trigonometry (radians)",
                               font=("Arial", 12, "bold"), bg=COLOR_BACKGROUND,
                               fg=COLOR_TEXT_DARK, padx=10, pady=10)
    create_operation_1_input(frame_trig, "Cosine", core.cosine, "cosine")
    create_operation_1_input(frame_trig, "Sine", core.sine, "sine")
    create_operation_1_input(frame_trig, "Tangent", core.tangent, "tangent")
    section_frames.append(frame_trig)

    # Section 4: Equations
    frame_eq = tk.LabelFrame(scrollable_frame, text="Equations",
                            font=("Arial", 12, "bold"), bg=COLOR_BACKGROUND,
                            fg=COLOR_TEXT_DARK, padx=10, pady=10)
    create_first_degree_equation(frame_eq)
    create_second_degree_equation(frame_eq)
    section_frames.append(frame_eq)

    # Section 5: Utilities
    frame_util = tk.LabelFrame(scrollable_frame, text="Utilities",
                               font=("Arial", 12, "bold"), bg=COLOR_BACKGROUND,
                               fg=COLOR_TEXT_DARK, padx=10, pady=10)
    create_operation_1_input(frame_util, "Absolute Value", core.absolute_value, "absolute_value")
    create_operation_1_input(frame_util, "Degrees to Radians", core.degrees_to_radians, "degrees_to_radians")
    create_pi_display(frame_util)
    section_frames.append(frame_util)

    # Flow layout function
    padding = 10
    def reflow_frames(event=None):
        canvas_width = canvas.winfo_width()
        if canvas_width <= 1:
            return

        # Update frame sizes
        for frame in section_frames:
            frame.update_idletasks()

        # First pass: determine rows and max height per row
        rows = []
        current_row = []
        x = padding

        for frame in section_frames:
            frame_width = frame.winfo_reqwidth()

            # Check if frame fits in current row
            if x + frame_width + padding > canvas_width and current_row:
                rows.append(current_row)
                current_row = []
                x = padding

            current_row.append(frame)
            x += frame_width + padding

        if current_row:
            rows.append(current_row)

        # Second pass: place frames with equal height per row
        y = padding
        for row in rows:
            # Find max height in this row
            row_height = max(f.winfo_reqheight() for f in row)

            # Place frames in this row
            x = padding
            for frame in row:
                frame_width = frame.winfo_reqwidth()
                frame.place(x=x, y=y, height=row_height)
                x += frame_width + padding

            y += row_height + padding

        # Update scrollable frame size
        total_height = y
        scrollable_frame.config(width=canvas_width, height=total_height)
        canvas.configure(scrollregion=(0, 0, canvas_width, total_height))

    # Bind resize event
    canvas.bind("<Configure>", reflow_frames)

    # Initial layout after window is ready
    parent.after(100, reflow_frames)

def create_operation_2_inputs(parent, label_text, function, operation_name):
    global calculator_inputs

    frame = tk.Frame(parent, bg=COLOR_BACKGROUND)
    frame.pack(fill=tk.X, pady=5)

    tk.Label(frame, text=label_text, font=("Arial", 10), bg=COLOR_BACKGROUND,
            fg=COLOR_TEXT_DARK, width=20, anchor="w").pack(side=tk.LEFT, padx=5)

    entry_a = tk.Entry(frame, font=("Arial", 10), width=10, bg=COLOR_INPUT_BG)
    entry_a.pack(side=tk.LEFT, padx=5)

    entry_b = tk.Entry(frame, font=("Arial", 10), width=10, bg=COLOR_INPUT_BG)
    entry_b.pack(side=tk.LEFT, padx=5)

    result_label = tk.Label(frame, text="", font=("Arial", 10, "bold"),
                           bg=COLOR_BACKGROUND, fg=COLOR_VALID, width=25, anchor="w")
    result_label.pack(side=tk.LEFT, padx=5)

    # Store references for history reuse
    calculator_inputs[operation_name] = {"entries": [entry_a, entry_b], "result": result_label}

    def calculate(event=None):
        val_a = entry_a.get().strip()
        val_b = entry_b.get().strip()

        if not val_a or not val_b:
            result_label.config(text="Please enter a value", fg=COLOR_ERROR)
            data.increment_error("Please enter a value")
            return

        try:
            a = float(val_a)
            b = float(val_b)
        except ValueError:
            result_label.config(text="Invalid input", fg=COLOR_ERROR)
            data.increment_error("Invalid input")
            return

        result = function(a, b)

        if isinstance(result, str):
            result_label.config(text=result, fg=COLOR_ERROR)
            data.increment_error(result)
        else:
            formatted = core.format_result(result)
            result_label.config(text=f"= {formatted}", fg=COLOR_VALID)
            data.add_history_entry(operation_name, [a, b], result)

    btn = tk.Button(frame, text="=", font=("Arial", 10, "bold"), bg=COLOR_PRIMARY,
                   fg="white", width=3, command=calculate)
    btn.pack(side=tk.LEFT, padx=5)

    # Enter key binding
    entry_a.bind("<Return>", calculate)
    entry_b.bind("<Return>", calculate)

def create_operation_1_input(parent, label_text, function, operation_name):
    global calculator_inputs

    frame = tk.Frame(parent, bg=COLOR_BACKGROUND)
    frame.pack(fill=tk.X, pady=5)

    tk.Label(frame, text=label_text, font=("Arial", 10), bg=COLOR_BACKGROUND,
            fg=COLOR_TEXT_DARK, width=20, anchor="w").pack(side=tk.LEFT, padx=5)

    entry = tk.Entry(frame, font=("Arial", 10), width=10, bg=COLOR_INPUT_BG)
    entry.pack(side=tk.LEFT, padx=5)

    # Spacer to align with 2-input operations (same font as Entry for consistent height)
    tk.Label(frame, text="", font=("Arial", 10), width=10, bg=COLOR_BACKGROUND).pack(side=tk.LEFT, padx=5)

    result_label = tk.Label(frame, text="", font=("Arial", 10, "bold"),
                           bg=COLOR_BACKGROUND, fg=COLOR_VALID, width=25, anchor="w")
    result_label.pack(side=tk.LEFT, padx=5)

    # Store references for history reuse
    calculator_inputs[operation_name] = {"entries": [entry], "result": result_label}

    def calculate(event=None):
        val = entry.get().strip()

        if not val:
            result_label.config(text="Please enter a value", fg=COLOR_ERROR)
            data.increment_error("Please enter a value")
            return

        try:
            n = float(val)
        except ValueError:
            result_label.config(text="Invalid input", fg=COLOR_ERROR)
            data.increment_error("Invalid input")
            return

        result = function(n)

        if isinstance(result, str):
            result_label.config(text=result, fg=COLOR_ERROR)
            data.increment_error(result)
        else:
            formatted = core.format_result(result)
            result_label.config(text=f"= {formatted}", fg=COLOR_VALID)
            data.add_history_entry(operation_name, [n], result)

    btn = tk.Button(frame, text="=", font=("Arial", 10, "bold"), bg=COLOR_PRIMARY,
                   fg="white", width=3, command=calculate)
    btn.pack(side=tk.LEFT, padx=5)

    # Enter key binding
    entry.bind("<Return>", calculate)

def create_first_degree_equation(parent):
    global calculator_inputs

    frame = tk.LabelFrame(parent, text="ax + b = 0", font=("Arial", 10, "bold"),
                         bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK, padx=10, pady=5)
    frame.pack(fill=tk.X, pady=5)

    input_frame = tk.Frame(frame, bg=COLOR_BACKGROUND)
    input_frame.pack()

    tk.Label(input_frame, text="a =", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=0, column=0, padx=5)
    entry_a = tk.Entry(input_frame, width=10, bg=COLOR_INPUT_BG)
    entry_a.grid(row=0, column=1, padx=5)

    tk.Label(input_frame, text="b =", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=0, column=2, padx=5)
    entry_b = tk.Entry(input_frame, width=10, bg=COLOR_INPUT_BG)
    entry_b.grid(row=0, column=3, padx=5)

    result_label = tk.Label(frame, text="", font=("Arial", 10, "bold"),
                           bg=COLOR_BACKGROUND, fg=COLOR_VALID)
    result_label.pack(pady=5)

    # Store references
    calculator_inputs["first_degree_equation"] = {"entries": [entry_a, entry_b], "result": result_label}

    def solve(event=None):
        val_a = entry_a.get().strip()
        val_b = entry_b.get().strip()

        if not val_a or not val_b:
            result_label.config(text="Please enter a value", fg=COLOR_ERROR)
            data.increment_error("Please enter a value")
            return

        try:
            a = float(val_a)
            b = float(val_b)
        except ValueError:
            result_label.config(text="Invalid input", fg=COLOR_ERROR)
            data.increment_error("Invalid input")
            return

        result = core.first_degree_equation(a, b)

        if isinstance(result, str):
            result_label.config(text=result, fg=COLOR_ERROR)
            data.increment_error(result)
        else:
            formatted = core.format_result(result)
            result_label.config(text=f"x = {formatted}", fg=COLOR_VALID)
            data.add_history_entry("first_degree_equation", {"a": a, "b": b}, f"x = {formatted}")

    btn = tk.Button(frame, text="Solve", font=("Arial", 10, "bold"),
                   bg=COLOR_PRIMARY, fg="white", command=solve)
    btn.pack()

    entry_a.bind("<Return>", solve)
    entry_b.bind("<Return>", solve)

def create_second_degree_equation(parent):
    global calculator_inputs

    frame = tk.LabelFrame(parent, text="ax² + bx + c = 0", font=("Arial", 10, "bold"),
                         bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK, padx=10, pady=5)
    frame.pack(fill=tk.X, pady=5)

    input_frame = tk.Frame(frame, bg=COLOR_BACKGROUND)
    input_frame.pack()

    tk.Label(input_frame, text="a =", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=0, column=0, padx=5)
    entry_a = tk.Entry(input_frame, width=8, bg=COLOR_INPUT_BG)
    entry_a.grid(row=0, column=1, padx=5)

    tk.Label(input_frame, text="b =", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=0, column=2, padx=5)
    entry_b = tk.Entry(input_frame, width=8, bg=COLOR_INPUT_BG)
    entry_b.grid(row=0, column=3, padx=5)

    tk.Label(input_frame, text="c =", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=0, column=4, padx=5)
    entry_c = tk.Entry(input_frame, width=8, bg=COLOR_INPUT_BG)
    entry_c.grid(row=0, column=5, padx=5)

    result_label = tk.Label(frame, text="", font=("Arial", 10, "bold"),
                           bg=COLOR_BACKGROUND, fg=COLOR_VALID)
    result_label.pack(pady=5)

    # Store references
    calculator_inputs["second_degree_equation"] = {"entries": [entry_a, entry_b, entry_c], "result": result_label}

    def solve(event=None):
        val_a = entry_a.get().strip()
        val_b = entry_b.get().strip()
        val_c = entry_c.get().strip()

        if not val_a or not val_b or not val_c:
            result_label.config(text="Please enter a value", fg=COLOR_ERROR)
            data.increment_error("Please enter a value")
            return

        try:
            a = float(val_a)
            b = float(val_b)
            c = float(val_c)
        except ValueError:
            result_label.config(text="Invalid input", fg=COLOR_ERROR)
            data.increment_error("Invalid input")
            return

        result = core.second_degree_equation(a, b, c)

        if isinstance(result, str):
            result_label.config(text=result, fg=COLOR_ERROR)
            data.increment_error(result)
        elif isinstance(result, tuple):
            if len(result) == 1:
                formatted = core.format_result(result[0])
                result_text = f"x = {formatted} (double)"
            else:
                x1 = core.format_result(result[0])
                x2 = core.format_result(result[1])
                result_text = f"x1 = {x1}, x2 = {x2}"
            result_label.config(text=result_text, fg=COLOR_VALID)
            data.add_history_entry("second_degree_equation", {"a": a, "b": b, "c": c}, result_text)

    btn = tk.Button(frame, text="Solve", font=("Arial", 10, "bold"),
                   bg=COLOR_PRIMARY, fg="white", command=solve)
    btn.pack()

    entry_a.bind("<Return>", solve)
    entry_b.bind("<Return>", solve)
    entry_c.bind("<Return>", solve)

def create_pi_display(parent):
    frame = tk.Frame(parent, bg=COLOR_BACKGROUND)
    frame.pack(fill=tk.X, pady=5)

    tk.Label(frame, text="Pi constant", font=("Arial", 10), bg=COLOR_BACKGROUND,
            fg=COLOR_TEXT_DARK, width=20, anchor="w").pack(side=tk.LEFT, padx=5)

    pi_value = core.format_result(core.get_pi())
    pi_label = tk.Label(frame, text=pi_value, font=("Arial", 10, "bold"),
                       bg=COLOR_BACKGROUND, fg=COLOR_VALID)
    pi_label.pack(side=tk.LEFT, padx=5)

    def copy_pi():
        parent.winfo_toplevel().clipboard_clear()
        parent.winfo_toplevel().clipboard_append(str(core.get_pi()))

    btn = tk.Button(frame, text="Copy", font=("Arial", 10), bg=COLOR_HEADER,
                   fg=COLOR_TEXT_DARK, command=copy_pi)
    btn.pack(side=tk.LEFT, padx=5)

# Graphs Tab
def create_graphs_tab(parent):
    # Left panel (controls)
    left_frame = tk.Frame(parent, bg=COLOR_BACKGROUND, width=300)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    left_frame.pack_propagate(False)

    tk.Label(left_frame, text="Function Type", font=("Arial", 12, "bold"),
            bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).pack(pady=10)

    type_var = tk.StringVar(value="linear")

    # Radio buttons
    radio_frame = tk.Frame(left_frame, bg=COLOR_BACKGROUND)
    radio_frame.pack(fill=tk.X, padx=10)

    tk.Radiobutton(radio_frame, text="Linear (y = ax + b)", variable=type_var,
                  value="linear", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK,
                  activebackground=COLOR_BACKGROUND).pack(anchor="w")
    tk.Radiobutton(radio_frame, text="Quadratic (y = ax² + bx + c)", variable=type_var,
                  value="quadratic", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK,
                  activebackground=COLOR_BACKGROUND).pack(anchor="w")
    tk.Radiobutton(radio_frame, text="Exponential (y = a^x)", variable=type_var,
                  value="exponential", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK,
                  activebackground=COLOR_BACKGROUND).pack(anchor="w")
    tk.Radiobutton(radio_frame, text="Sine (y = sin(x))", variable=type_var,
                  value="sine", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK,
                  activebackground=COLOR_BACKGROUND).pack(anchor="w")
    tk.Radiobutton(radio_frame, text="Cosine (y = cos(x))", variable=type_var,
                  value="cosine", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK,
                  activebackground=COLOR_BACKGROUND).pack(anchor="w")
    tk.Radiobutton(radio_frame, text="Tangent (y = tan(x))", variable=type_var,
                  value="tangent", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK,
                  activebackground=COLOR_BACKGROUND).pack(anchor="w")

    # Parameters
    tk.Label(left_frame, text="Parameters", font=("Arial", 12, "bold"),
            bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).pack(pady=10)

    param_frame = tk.Frame(left_frame, bg=COLOR_BACKGROUND)
    param_frame.pack(fill=tk.X, padx=20)

    tk.Label(param_frame, text="a =", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=0, column=0, pady=5, sticky="e")
    entry_a = tk.Entry(param_frame, width=10, bg=COLOR_INPUT_BG)
    entry_a.grid(row=0, column=1, pady=5, padx=5)
    entry_a.insert(0, "1")

    tk.Label(param_frame, text="b =", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=1, column=0, pady=5, sticky="e")
    entry_b = tk.Entry(param_frame, width=10, bg=COLOR_INPUT_BG)
    entry_b.grid(row=1, column=1, pady=5, padx=5)
    entry_b.insert(0, "0")

    tk.Label(param_frame, text="c =", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=2, column=0, pady=5, sticky="e")
    entry_c = tk.Entry(param_frame, width=10, bg=COLOR_INPUT_BG)
    entry_c.grid(row=2, column=1, pady=5, padx=5)
    entry_c.insert(0, "0")

    # X range
    tk.Label(left_frame, text="X Range", font=("Arial", 12, "bold"),
            bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).pack(pady=10)

    range_frame = tk.Frame(left_frame, bg=COLOR_BACKGROUND)
    range_frame.pack(fill=tk.X, padx=20)

    tk.Label(range_frame, text="Min:", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=0, column=0, pady=5, sticky="e")
    entry_xmin = tk.Entry(range_frame, width=8, bg=COLOR_INPUT_BG)
    entry_xmin.grid(row=0, column=1, pady=5, padx=5)
    entry_xmin.insert(0, "-10")

    tk.Label(range_frame, text="Max:", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=0, column=2, pady=5, sticky="e")
    entry_xmax = tk.Entry(range_frame, width=8, bg=COLOR_INPUT_BG)
    entry_xmax.grid(row=0, column=3, pady=5, padx=5)
    entry_xmax.insert(0, "10")

    # Y range
    tk.Label(left_frame, text="Y Range", font=("Arial", 12, "bold"),
            bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).pack(pady=10)

    yrange_frame = tk.Frame(left_frame, bg=COLOR_BACKGROUND)
    yrange_frame.pack(fill=tk.X, padx=20)

    auto_y_var = tk.BooleanVar(value=True)
    tk.Checkbutton(yrange_frame, text="Auto", variable=auto_y_var,
                  bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK,
                  activebackground=COLOR_BACKGROUND).grid(row=0, column=0, columnspan=2)

    tk.Label(yrange_frame, text="Min:", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=1, column=0, pady=5, sticky="e")
    entry_ymin = tk.Entry(yrange_frame, width=8, bg=COLOR_INPUT_BG)
    entry_ymin.grid(row=1, column=1, pady=5, padx=5)
    entry_ymin.insert(0, "-10")

    tk.Label(yrange_frame, text="Max:", bg=COLOR_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=1, column=2, pady=5, sticky="e")
    entry_ymax = tk.Entry(yrange_frame, width=8, bg=COLOR_INPUT_BG)
    entry_ymax.grid(row=1, column=3, pady=5, padx=5)
    entry_ymax.insert(0, "10")

    # Export notification label
    export_label = tk.Label(left_frame, text="", font=("Arial", 10),
                           bg=COLOR_BACKGROUND, fg=COLOR_VALID)
    export_label.pack(pady=5)

    # Right panel (graph)
    right_frame = tk.Frame(parent, bg=COLOR_BACKGROUND)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor('#fee1d3')
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_graph():
        try:
            ax.clear()
            ax.set_facecolor('white')
            ax.grid(True, alpha=0.5)
            ax.axhline(y=0, color='k', linewidth=1)
            ax.axvline(x=0, color='k', linewidth=1)

            xmin = float(entry_xmin.get())
            xmax = float(entry_xmax.get())

            # Generate x values
            x_values = []
            for i in range(1000):
                x_values.append(xmin + i * (xmax - xmin) / 999)

            func_type = type_var.get()
            title = ""

            if func_type == "linear":
                a = float(entry_a.get())
                b = float(entry_b.get())
                y_values = [a * x + b for x in x_values]
                title = f"y = {a}x + {b}"
                ax.plot(x_values, y_values, 'b-', linewidth=2, label=title)

            elif func_type == "quadratic":
                a = float(entry_a.get())
                b = float(entry_b.get())
                c = float(entry_c.get())
                y_values = [a * x * x + b * x + c for x in x_values]
                title = f"y = {a}x² + {b}x + {c}"
                ax.plot(x_values, y_values, 'r-', linewidth=2, label=title)

            elif func_type == "exponential":
                a = float(entry_a.get())
                if a <= 0:
                    return
                y_values = []
                for x in x_values:
                    val = core.power(a, x)
                    if abs(val) < 1000:
                        y_values.append(val)
                    else:
                        y_values.append(None)
                title = f"y = {a}^x"
                ax.plot(x_values, y_values, 'g-', linewidth=2, label=title)

            elif func_type == "sine":
                y_values = [core.sine(x) for x in x_values]
                title = "y = sin(x)"
                ax.plot(x_values, y_values, 'm-', linewidth=2, label=title)

            elif func_type == "cosine":
                y_values = [core.cosine(x) for x in x_values]
                title = "y = cos(x)"
                ax.plot(x_values, y_values, 'c-', linewidth=2, label=title)

            elif func_type == "tangent":
                y_values = []
                for x in x_values:
                    t = core.tangent(x)
                    if isinstance(t, str) or abs(t) > 10:
                        y_values.append(None)
                    else:
                        y_values.append(t)
                title = "y = tan(x)"
                ax.plot(x_values, y_values, color='orange', linewidth=2, label=title)

            ax.set_xlim(xmin, xmax)
            if not auto_y_var.get():
                ymin = float(entry_ymin.get())
                ymax = float(entry_ymax.get())
                ax.set_ylim(ymin, ymax)

            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(title)
            ax.legend(loc='upper right')
            canvas.draw()

        except Exception as e:
            pass

    def export_graph():
        if data.export_graph(fig):
            export_label.config(text="Exported!")
            left_frame.after(2000, lambda: export_label.config(text=""))

    # Buttons frame
    btn_frame = tk.Frame(left_frame, bg=COLOR_BACKGROUND)
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="Plot", font=("Arial", 12, "bold"),
             bg=COLOR_PRIMARY, fg="white", command=plot_graph, width=8).pack(side=tk.LEFT, padx=5)

    tk.Button(btn_frame, text="Export", font=("Arial", 12, "bold"),
             bg=COLOR_HEADER, fg=COLOR_TEXT_DARK, command=export_graph, width=8).pack(side=tk.LEFT, padx=5)

# History functions
history_frame_ref = None

def refresh_history():
    global history_frame_ref

    if history_frame_ref is None:
        return

    # Clear existing entries
    for widget in history_frame_ref.winfo_children():
        widget.destroy()

    history = data.get_history()

    if not history:
        tk.Label(history_frame_ref, text="No calculations yet", font=("Arial", 12),
                bg=COLOR_BACKGROUND, fg=COLOR_TEXT_SECONDARY).pack(pady=50)
        return

    # Show most recent first
    for entry in reversed(history):
        create_history_entry_widget(history_frame_ref, entry)

def create_history_entry_widget(parent, entry):
    frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=1)
    frame.pack(fill=tk.X, pady=2, padx=5)

    operation = entry["operation"]
    operands = entry["operands"]
    result = entry["result"]
    timestamp = entry["timestamp"]

    # Format display text
    display_text = format_history_display(operation, operands, result)

    # Format timestamp
    ts_display = format_timestamp(timestamp)

    content_frame = tk.Frame(frame, bg="white")
    content_frame.pack(fill=tk.X, padx=10, pady=5)

    tk.Label(content_frame, text=display_text, font=("Arial", 10),
            bg="white", fg=COLOR_TEXT_DARK, anchor="w").pack(side=tk.LEFT)

    tk.Label(content_frame, text=ts_display, font=("Arial", 9),
            bg="white", fg=COLOR_TEXT_SECONDARY, anchor="e").pack(side=tk.RIGHT)

    # Click to reuse
    def on_click(event=None):
        load_history_entry(operation, operands)

    frame.bind("<Button-1>", on_click)
    content_frame.bind("<Button-1>", on_click)
    for child in content_frame.winfo_children():
        child.bind("<Button-1>", on_click)

    # Hover effect
    def on_enter(event):
        frame.config(bg=COLOR_HEADER)
        content_frame.config(bg=COLOR_HEADER)
        for child in content_frame.winfo_children():
            child.config(bg=COLOR_HEADER)

    def on_leave(event):
        frame.config(bg="white")
        content_frame.config(bg="white")
        for child in content_frame.winfo_children():
            child.config(bg="white")

    frame.bind("<Enter>", on_enter)
    frame.bind("<Leave>", on_leave)

def format_history_display(operation, operands, result):
    # Format based on operation type
    op_symbols = {
        "addition": "+",
        "subtraction": "-",
        "multiplication": "*",
        "division": "/",
        "power": "^",
        "modulo": "%"
    }

    if operation in op_symbols:
        return f"{operands[0]} {op_symbols[operation]} {operands[1]} = {core.format_result(result)}"
    elif operation == "square_root":
        return f"sqrt({operands[0]}) = {core.format_result(result)}"
    elif operation == "cube_root":
        return f"cbrt({operands[0]}) = {core.format_result(result)}"
    elif operation == "factorial":
        return f"{int(operands[0])}! = {core.format_result(result)}"
    elif operation == "cosine":
        return f"cos({operands[0]}) = {core.format_result(result)}"
    elif operation == "sine":
        return f"sin({operands[0]}) = {core.format_result(result)}"
    elif operation == "tangent":
        return f"tan({operands[0]}) = {core.format_result(result)}"
    elif operation == "absolute_value":
        return f"|{operands[0]}| = {core.format_result(result)}"
    elif operation == "degrees_to_radians":
        return f"{operands[0]}° = {core.format_result(result)} rad"
    elif operation == "first_degree_equation":
        return f"{operands['a']}x + {operands['b']} = 0 -> {result}"
    elif operation == "second_degree_equation":
        return f"{operands['a']}x² + {operands['b']}x + {operands['c']} = 0 -> {result}"
    else:
        return f"{operation}: {result}"

def format_timestamp(timestamp):
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        today = datetime.now().date()
        if dt.date() == today:
            return dt.strftime("%H:%M")
        else:
            return dt.strftime("%m/%d")
    except:
        return timestamp

def load_history_entry(operation, operands):
    global notebook, calculator_inputs

    if operation not in calculator_inputs:
        return

    entries = calculator_inputs[operation]["entries"]

    if isinstance(operands, dict):
        # Equation format
        if "a" in operands and len(entries) >= 2:
            entries[0].delete(0, tk.END)
            entries[0].insert(0, str(operands["a"]))
            entries[1].delete(0, tk.END)
            entries[1].insert(0, str(operands["b"]))
            if "c" in operands and len(entries) >= 3:
                entries[2].delete(0, tk.END)
                entries[2].insert(0, str(operands["c"]))
    elif isinstance(operands, list):
        for i, val in enumerate(operands):
            if i < len(entries):
                entries[i].delete(0, tk.END)
                entries[i].insert(0, str(val))

    # Switch to Calculator tab
    if notebook:
        notebook.select(0)

# Statistics functions
stats_frame_ref = None

def refresh_stats():
    global stats_frame_ref

    if stats_frame_ref is None:
        return

    scrollable_frame, total_label = stats_frame_ref

    # Clear existing entries
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    errors = data.get_error_counts()
    total = data.get_total_errors()

    total_label.config(text=f"Total Errors: {total}")

    if total == 0:
        tk.Label(scrollable_frame, text="No errors recorded", font=("Arial", 12),
                bg=COLOR_BACKGROUND, fg=COLOR_TEXT_SECONDARY).pack(pady=50)
        return

    # Error type labels
    error_labels = {
        "division_by_zero": "Division by zero",
        "negative_number": "Negative number (sqrt/factorial)",
        "integer_required": "Integer required (factorial)",
        "tangent_undefined": "Tangent undefined",
        "invalid_input": "Invalid input",
        "empty_field": "Empty field",
        "no_solution": "No solution (1st degree)",
        "infinite_solutions": "Infinite solutions (1st degree)",
        "not_quadratic": "Not quadratic (a=0)",
        "no_real_solution": "No real solution (2nd degree)"
    }

    for error_type, count in errors.items():
        if count > 0:
            frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=2, padx=5)

            label = error_labels.get(error_type, error_type)

            tk.Label(frame, text=label, font=("Arial", 10),
                    bg="white", fg=COLOR_TEXT_DARK, anchor="w").pack(side=tk.LEFT, padx=10, pady=5)

            tk.Label(frame, text=str(count), font=("Arial", 10, "bold"),
                    bg="white", fg=COLOR_ERROR, anchor="e").pack(side=tk.RIGHT, padx=10, pady=5)
