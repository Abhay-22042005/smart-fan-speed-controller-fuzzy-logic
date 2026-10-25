# Smart Fan Speed Controller Using Fuzzy Logic

This local Python desktop application recommends a fan speed from a manually
entered room temperature. It demonstrates fuzzy logic; it does **not** control
a physical fan or read a real sensor.

## Features

- Accepts temperatures from 15°C to 40°C.
- Uses Mamdani fuzzy inference with Low, Medium, and High sets and rules.
- Displays a recommended speed from 0% to 100% and a temperature category.
- Includes input validation, a progress bar, Reset, and Exit controls.
- Plots the temperature and fan-speed membership functions.

## Project files

- `main.py` — fuzzy controller, Tkinter interface, and graph creation.
- `test_main.py` — repeatable controller and graph tests using `unittest`.
- `requirements.txt` — pinned Python package versions.
- `PROJECT_REPORT.md` — project synopsis, design, test results, and viva questions.

## Requirements

- Windows with Python 3 installed. The project was tested with Python 3.14.7.
- VS Code with the Microsoft Python extension.
- Tkinter, normally included with the standard Windows Python installer.

## Set up in VS Code

1. Open this project folder in VS Code.
2. Select the Python interpreter you will use: press **Ctrl+Shift+P**, choose
   **Python: Select Interpreter**, then select the intended Python executable.
   Install the packages into that same interpreter.
3. Open the integrated terminal with **Ctrl+`** and confirm Python is available:

   ```powershell
   python --version
   ```

4. Install the project packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

   If `pip` is missing, run `python -m ensurepip --upgrade` first. If the
   `python` command is unavailable, use `py -3 --version` and
   `py -3 -m pip install -r requirements.txt`, making sure VS Code selects the
   same Python installation.
5. Run the tests:

   ```powershell
   python -m unittest -v test_main.py
   ```

6. Launch the desktop application:

   ```powershell
   python main.py
   ```

If you use a virtual environment, create it once with `py -3 -m venv .venv`,
activate it in PowerShell with `.\.venv\Scripts\Activate.ps1`, select its
interpreter in VS Code, and run the install, test, and launch commands above.
Do not recreate an existing environment unless you intend to replace it.

## Using the application

Enter a room temperature from 15 to 40 and select **Calculate Fan Speed**.
The progress bar and percentage show the fuzzy controller's recommendation.
Select **View Membership Graphs** to open both plots, **Reset** to clear the
input and result, or **Exit** to close the application. Pressing Enter also
calculates the recommendation.

## Notes

- Speed is calculated by fuzzy inference and centroid defuzzification, not by
  hardcoded temperature thresholds.
- NetworkX is listed explicitly because the installed scikit-fuzzy control
  module imports it.
- A non-failing NumPy deprecation warning may be printed by scikit-fuzzy 0.5.0
  during calculation. It does not affect the tested results.
