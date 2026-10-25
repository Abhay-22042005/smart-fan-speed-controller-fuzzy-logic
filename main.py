"""Smart Fan Speed Controller using Mamdani fuzzy logic."""

import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
import tkinter as tk
from skfuzzy import control as ctrl
from tkinter import messagebox, ttk


# Temperature is measured in degrees Celsius; fan speed is a percentage.
temperature = ctrl.Antecedent(np.arange(15, 41, 1), "temperature")
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), "fan_speed")

# Overlapping triangles make transitions between categories gradual.
temperature["low"] = fuzz.trimf(temperature.universe, [15, 15, 25])
temperature["medium"] = fuzz.trimf(temperature.universe, [18, 27.5, 37])
temperature["high"] = fuzz.trimf(temperature.universe, [30, 40, 40])

fan_speed["low"] = fuzz.trimf(fan_speed.universe, [0, 0, 45])
fan_speed["medium"] = fuzz.trimf(fan_speed.universe, [25, 50, 75])
fan_speed["high"] = fuzz.trimf(fan_speed.universe, [55, 100, 100])
fan_speed.defuzzify_method = "centroid"

# These are fuzzy IF-THEN rules, processed by scikit-fuzzy's control system.
rules = [
    ctrl.Rule(temperature["low"], fan_speed["low"]),
    ctrl.Rule(temperature["medium"], fan_speed["medium"]),
    ctrl.Rule(temperature["high"], fan_speed["high"]),
]
fuzzy_control_system = ctrl.ControlSystem(rules)


def _validate_temperature(room_temperature_c: float) -> float:
    """Convert the input to a finite number within the accepted range."""
    try:
        value = float(room_temperature_c)
    except (TypeError, ValueError) as error:
        raise ValueError("Temperature must be a number.") from error

    if not np.isfinite(value):
        raise ValueError("Temperature must be a finite number.")
    if value < 15 or value > 40:
        raise ValueError("Temperature must be between 15°C and 40°C.")

    return value


def calculate_fan_speed(room_temperature_c: float) -> tuple[float, str]:
    """Return the fuzzy fan-speed recommendation and temperature category."""
    temperature_value = _validate_temperature(room_temperature_c)
    simulation = ctrl.ControlSystemSimulation(fuzzy_control_system)
    simulation.input["temperature"] = temperature_value
    simulation.compute()

    raw_speed_percent = float(simulation.output["fan_speed"])
    if not np.isfinite(raw_speed_percent) or not 0 <= raw_speed_percent <= 100:
        raise RuntimeError("The fuzzy controller produced an invalid fan speed.")
    speed_percent = round(raw_speed_percent, 2)

    # Report the category with the greatest membership at this temperature.
    membership_degrees = {
        category: fuzz.interp_membership(
            temperature.universe,
            temperature[category].mf,
            temperature_value,
        )
        for category in ("low", "medium", "high")
    }
    temperature_category = max(membership_degrees, key=membership_degrees.get)

    return speed_percent, temperature_category.title()


def create_membership_figure():
    """Build the temperature and fan-speed membership-function plots."""
    figure, (temperature_axes, speed_axes) = plt.subplots(1, 2, figsize=(11, 4.5))

    for category in ("low", "medium", "high"):
        temperature_axes.plot(
            temperature.universe,
            temperature[category].mf,
            label=category.title(),
            linewidth=2,
        )
        speed_axes.plot(
            fan_speed.universe,
            fan_speed[category].mf,
            label=category.title(),
            linewidth=2,
        )

    temperature_axes.set_title("Temperature Membership Functions")
    temperature_axes.set_xlabel("Temperature (°C)")
    temperature_axes.set_xlim(15, 40)
    speed_axes.set_title("Fan-Speed Membership Functions")
    speed_axes.set_xlabel("Fan speed (%)")
    speed_axes.set_xlim(0, 100)

    for axes in (temperature_axes, speed_axes):
        axes.set_ylabel("Membership degree")
        axes.set_ylim(0, 1.05)
        axes.set_yticks(np.linspace(0, 1, 6))
        axes.grid(True, linestyle="--", alpha=0.35)
        axes.legend()

    figure.suptitle("Fuzzy Membership Functions", fontsize=14, fontweight="bold")
    figure.tight_layout()
    return figure


def main() -> None:
    """Display the desktop interface for the fuzzy fan-speed controller."""
    background_color = "#F3F7FA"
    card_color = "#FFFFFF"
    text_color = "#183247"
    muted_color = "#5B6B78"
    accent_color = "#137C8B"

    root = tk.Tk()
    root.title("Smart Fan Speed Controller")
    root.geometry("620x560")
    root.minsize(520, 520)
    root.configure(background=background_color)

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    style.configure("TFrame", background=background_color)
    style.configure("Card.TFrame", background=card_color)
    style.configure(
        "Title.TLabel",
        background=background_color,
        foreground=text_color,
        font=("Segoe UI", 22, "bold"),
    )
    style.configure(
        "Subtitle.TLabel",
        background=background_color,
        foreground=muted_color,
        font=("Segoe UI", 10),
    )
    style.configure(
        "CardHeading.TLabel",
        background=card_color,
        foreground=text_color,
        font=("Segoe UI", 12, "bold"),
    )
    style.configure(
        "CardText.TLabel",
        background=card_color,
        foreground=muted_color,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Speed.TLabel",
        background=card_color,
        foreground=accent_color,
        font=("Segoe UI", 34, "bold"),
    )
    style.configure(
        "TEntry",
        padding=9,
        font=("Segoe UI", 12),
    )
    style.configure(
        "TButton",
        padding=(14, 9),
        font=("Segoe UI", 10),
    )
    style.configure(
        "Accent.TButton",
        background=accent_color,
        foreground="#FFFFFF",
        padding=(16, 10),
        font=("Segoe UI", 10, "bold"),
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#0F6875"), ("pressed", "#0B5661")],
    )
    style.configure(
        "Fan.Horizontal.TProgressbar",
        background=accent_color,
        troughcolor="#E3EBF0",
        bordercolor="#E3EBF0",
        thickness=16,
    )

    content = ttk.Frame(root, padding=(28, 24))
    content.pack(fill="both", expand=True)
    content.columnconfigure(0, weight=1)

    ttk.Label(
        content,
        text="Smart Fan Speed Controller",
        style="Title.TLabel",
    ).grid(row=0, column=0, sticky="w")
    ttk.Label(
        content,
        text="A fuzzy-logic recommendation based on room temperature",
        style="Subtitle.TLabel",
    ).grid(row=1, column=0, sticky="w", pady=(5, 20))

    input_card = ttk.Frame(content, style="Card.TFrame", padding=18)
    input_card.grid(row=2, column=0, sticky="ew", pady=(0, 16))
    input_card.columnconfigure(0, weight=1)
    ttk.Label(
        input_card,
        text="Room temperature",
        style="CardHeading.TLabel",
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

    temperature_entry = ttk.Entry(input_card, width=15)
    temperature_entry.grid(row=1, column=0, sticky="ew")
    ttk.Label(input_card, text="°C", style="CardText.TLabel").grid(
        row=1, column=1, padx=(9, 14)
    )

    result_card = ttk.Frame(content, style="Card.TFrame", padding=20)
    result_card.grid(row=3, column=0, sticky="ew", pady=(0, 16))
    result_card.columnconfigure(0, weight=1)
    ttk.Label(
        result_card,
        text="Recommended fan speed",
        style="CardHeading.TLabel",
    ).grid(row=0, column=0, sticky="w")

    speed_text = ttk.Label(result_card, text="—%", style="Speed.TLabel")
    speed_text.grid(row=1, column=0, sticky="w", pady=(4, 0))
    category_text = ttk.Label(
        result_card,
        text="Temperature category: —",
        style="CardText.TLabel",
    )
    category_text.grid(row=2, column=0, sticky="w", pady=(0, 14))

    speed_value = tk.DoubleVar(value=0)
    progress_bar = ttk.Progressbar(
        result_card,
        maximum=100,
        variable=speed_value,
        mode="determinate",
        style="Fan.Horizontal.TProgressbar",
    )
    progress_bar.grid(row=3, column=0, sticky="ew")

    def calculate() -> None:
        entered_temperature = temperature_entry.get().strip()
        if not entered_temperature:
            messagebox.showerror(
                "Temperature required",
                "Enter a room temperature between 15°C and 40°C.",
                parent=root,
            )
            temperature_entry.focus_set()
            return

        try:
            temperature_value = float(entered_temperature)
            recommended_speed, category = calculate_fan_speed(temperature_value)
        except ValueError as error:
            messagebox.showerror("Invalid temperature", str(error), parent=root)
            temperature_entry.focus_set()
            temperature_entry.selection_range(0, tk.END)
            return

        speed_text.configure(text=f"{recommended_speed:.1f}%")
        category_text.configure(text=f"Temperature category: {category}")
        speed_value.set(recommended_speed)

    def reset() -> None:
        temperature_entry.delete(0, tk.END)
        speed_text.configure(text="—%")
        category_text.configure(text="Temperature category: —")
        speed_value.set(0)
        temperature_entry.focus_set()

    def show_membership_graphs() -> None:
        create_membership_figure()
        plt.show(block=False)

    ttk.Button(
        input_card,
        text="Calculate Fan Speed",
        style="Accent.TButton",
        command=calculate,
    ).grid(row=1, column=2, sticky="ew")

    action_row = ttk.Frame(content)
    action_row.grid(row=4, column=0, sticky="ew")
    ttk.Button(
        action_row,
        text="View Membership Graphs",
        command=show_membership_graphs,
    ).pack(side="left")
    ttk.Button(action_row, text="Reset", command=reset).pack(
        side="right", padx=(10, 0)
    )
    ttk.Button(action_row, text="Exit", command=root.destroy).pack(side="right")

    ttk.Label(
        content,
        text="Simulation only — this app does not control a physical fan.",
        style="Subtitle.TLabel",
    ).grid(row=5, column=0, sticky="w", pady=(16, 0))

    root.bind("<Return>", lambda _event: calculate())
    temperature_entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()
