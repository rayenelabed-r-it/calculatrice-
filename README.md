# Math Calculator

A powerful and user-friendly desktop calculator with a graphical interface built using Python's Tkinter library. It offers a wide range of mathematical functions, equation solving, graph plotting, and data persistence features.

## Features

- **Standard & Advanced Calculations**: Performs basic arithmetic, power, roots, factorial, and trigonometric operations (sine, cosine, tangent).
- **Equation Solvers**:
  - Solves first-degree equations (`ax + b = 0`).
  - Solves second-degree equations (`ax² + bx + c = 0`) and shows real solutions.
- **Graphing Tool**:
  - Plot various types of functions: Linear, Quadratic, Exponential, Sine, Cosine, and Tangent.
  - Customize the plot range (X and Y axes).
  - Export graphs as PNG images.
- **Persistent History**:
  - Automatically saves a history of all successful calculations.
  - History is reloaded when the application starts.
  - Click on a history entry to reload the inputs into the calculator.
- **Error Statistics**:
  - Tracks the frequency of different error types (e.g., division by zero, invalid input).
  - Statistics are saved and reloaded across sessions.
- **User-Friendly Interface**:
  - A clean, tabbed interface separating the calculator and graphing tools.
  - A responsive layout that adjusts to window size.
  - A sidebar for easy access to calculation history and error statistics.
  - Color-coded feedback for results and errors.

## Project Structure

The project is organized into several modules:

- `main.py`: The entry point of the application that launches the graphical interface.
- `ui.py`: Contains all the code for the Tkinter-based user interface, including window layout, widgets, and event handling.
- `core.py`: Implements all the core mathematical logic and functions used by the calculator.
- `data.py`: Handles data persistence, including saving and loading the calculation history and error statistics to/from JSON files.
- `Folder UML/`: Contains UML diagrams (`Diagramme_de_packages.png` and `Diagramme_de_sequence.png`) illustrating the project's architecture.

## How to Run

1.  **Prerequisites**:
    *   Python 3.6 or newer is recommended.
    *   Install the `matplotlib` library. `tkinter` is usually included with standard Python installations.
        ```bash
        pip install matplotlib
        ```

2.  **Execute the application**:
    ```bash
    python main.py
    ```

## Modules Description

### `main.py`
This is the main script to launch the application. It calls the `create_interface` function from the `ui` module.

### `core.py`
This module provides the core functionalities of the calculator.
- **Basic Operations**: `addition`, `subtraction`, `multiplication`, `division`, `power`, `modulo`.
- **Roots and Factorial**: `square_root`, `cube_root`, `factorial`.
- **Trigonometry**: `cosine`, `sine`, `tangent` (implemented using Taylor series).
- **Equation Solvers**: `first_degree_equation`, `second_degree_equation`.
- **Utilities**: `absolute_value`, `degrees_to_radians`, `get_pi`.
- **Formatting**: `format_result` to present results cleanly.

### `data.py`
This module handles all data storage needs.
- **History**:
  - `load_history()`: Loads calculation history from `history.json`.
  - `save_history()`: Saves the history.
  - `add_history_entry()`: Adds a new entry to the history.
- **Errors**:
  - `load_errors()`: Loads error statistics from `errors.json`.
  - `save_errors()`: Saves the statistics.
  - `increment_error()`: Increments the count for a specific error type.
- **Export**:
  - `export_graph()`: Opens a file dialog to save a Matplotlib figure as a PNG file.

### `ui.py`
This module is responsible for building the entire graphical user interface using Tkinter.
- **Main Window**: Creates the main application window, header, and paned layout.
- **Calculator Tab**:
  - Dynamically creates input fields and buttons for all operations defined in `core.py`.
  - Handles user input, calls the appropriate core functions, and displays results or errors.
- **Graphs Tab**:
  - Provides controls to select a function type, set parameters, and define the plot range.
  - Uses `matplotlib` to render and embed the graph in the Tkinter window.
- **Sidebar**:
  - **History**: Displays a scrollable list of past calculations. Allows clearing the history.
  - **Statistics**: Displays a summary of recorded errors. Allows resetting the stats.
- **Interactivity**:
  - Binds keyboard events (like "Enter") for quick calculations.
  - Allows reusing history entries by clicking on them.
  - Provides hover effects and clear visual feedback.