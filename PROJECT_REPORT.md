# Project Report: Smart Fan Speed Controller Using Fuzzy Logic

## 1. Synopsis

The Smart Fan Speed Controller is a local desktop simulation that recommends
fan speed based on room temperature. The user enters a value from 15°C to
40°C. A Mamdani fuzzy controller fuzzifies the input, evaluates three
IF–THEN rules, aggregates the output fuzzy sets, and uses centroid
defuzzification to produce a speed percentage. A Tkinter interface displays
the recommendation, its temperature category, and a progress bar. Matplotlib
plots the controller's membership functions.

The application is for learning and demonstration only. It has no physical
sensor, fan, or hardware-control connection.

## 2. Problem statement

Develop a fuzzy-logic system that accepts room temperature from 15°C to 40°C
and recommends a fan speed from 0% to 100%. The system must use fuzzy sets,
membership functions, fuzzy rules, inference, and defuzzification, and present
the result in a desktop GUI.

## 3. Objectives

- Represent temperature and fan speed with overlapping fuzzy sets.
- Apply fuzzy IF–THEN rules using Mamdani inference.
- Produce a numerical speed percentage by centroid defuzzification.
- Display the speed and temperature category in a beginner-friendly GUI.
- Reject empty, non-numeric, non-finite, and out-of-range input.
- Plot and test the membership functions.

## 4. Requirements and technology

**Input:** A manually entered temperature from 15°C through 40°C.

**Output:** A numerical speed between 0% and 100%, plus a Low, Medium, or High
temperature category.

**Technology:** Python 3, NumPy, scikit-fuzzy, NetworkX, Tkinter, Matplotlib,
and VS Code. Tkinter is part of the standard Python distribution on Windows.

## 5. Why fuzzy logic?

Room temperature changes gradually, so an abrupt threshold can make a
recommendation jump suddenly at a boundary. Fuzzy sets let a temperature
partly belong to two neighboring categories. The rules combine those
memberships and produce a gradual speed recommendation. This makes fuzzy
logic suitable for explaining approximate, human-readable control decisions.

## 6. Fuzzy sets and rules

Triangular membership functions are used. The three parameters are the
triangle's left point, peak, and right point. At the domain endpoints,
triangles such as `[15, 15, 25]` and `[30, 40, 40]` have full membership at
the endpoint.

| Variable | Category | Triangle parameters |
|---|---|---|
| Temperature (°C) | Low | `[15, 15, 25]` |
| Temperature (°C) | Medium | `[18, 27.5, 37]` |
| Temperature (°C) | High | `[30, 40, 40]` |
| Fan speed (%) | Low | `[0, 0, 45]` |
| Fan speed (%) | Medium | `[25, 50, 75]` |
| Fan speed (%) | High | `[55, 100, 100]` |

The fuzzy rules are:

1. IF temperature is Low, THEN fan speed is Low.
2. IF temperature is Medium, THEN fan speed is Medium.
3. IF temperature is High, THEN fan speed is High.

The displayed temperature category is the category with the greatest
membership at the entered temperature. The controller output itself is
calculated by the fuzzy control system, not by this category label.

## 7. System architecture

```text
Manual temperature (15–40 °C)
              |
              v
       Input validation
              |
              v
        Fuzzification
  Low / Medium / High degrees
              |
              v
      Mamdani fuzzy rules
              |
              v
   Aggregate output fuzzy sets
              |
              v
 Centroid defuzzification
              |
              v
 Speed percentage + temperature category
              |
              v
   Tkinter result and progress bar

Membership definitions ----------> Matplotlib graphs
```

## 8. Algorithm

1. Read the temperature entered by the user.
2. Reject the input if it is empty, non-numeric, non-finite, or outside
   15°C–40°C.
3. Calculate its membership in the Low, Medium, and High temperature sets.
4. Evaluate the three Mamdani IF–THEN rules using scikit-fuzzy.
5. Combine the activated output sets.
6. Apply centroid defuzzification to obtain the speed percentage.
7. Select the temperature category with the greatest membership.
8. Display the percentage, category, and progress bar in the GUI.

## 9. Test cases and results

The automated tests were run with Python 3.14.7 using:

```powershell
python -m unittest -v test_main.py
```

All five automated tests passed. The controller also was checked at 251
temperature points from 15.0°C through 40.0°C in 0.1°C increments; the speed
stayed in range and did not decrease as temperature increased.

| Input | Expected behavior | Observed result | Status |
|---|---|---|---|
| 15°C | Accept lower boundary; Low category; speed in range | 15.00%, Low | PASS |
| 20°C | Low category; speed in range | 28.58%, Low | PASS |
| 27.5°C | Medium category; speed in range | 50.00%, Medium | PASS |
| 35°C | High category; speed in range | 71.42%, High | PASS |
| 40°C | Accept upper boundary; High category; speed in range | 85.00%, High | PASS |
| Empty input | Show an input-required message | Rejected; GUI dialog confirmed | PASS |
| `abc` | Show a numeric-input error | Rejected; GUI dialog confirmed | PASS |
| 14°C or 41°C | Show an out-of-range error | Rejected | PASS |
| NaN or infinity | Reject non-finite value | Rejected | PASS |
| Increasing input | Speed remains in range and does not decrease | Verified at 251 points | PASS |
| Membership plots | Two plots, three terms each, labeled axes and membership scale | Automated graph test passed; GUI display confirmed | PASS |

Manual GUI checks of calculation, validation dialogs, Reset, Exit, and the
membership-graph button were confirmed during the project walkthrough.

## 10. Screenshots to capture

1. The application before a temperature is entered.
2. The result after entering 27.5°C (50.0%, Medium).
3. An input-validation dialog, such as for 41°C.
4. The window containing both membership-function plots.

## 11. Advantages and limitations

**Advantages**

- Demonstrates the full fuzzy-logic pipeline, not a crisp threshold substitute.
- Overlapping sets allow gradual transitions.
- Local and simple to run; it needs no sensor, database, cloud service, or
  physical fan.
- Input validation and repeatable tests make it easy to demonstrate.

**Limitations**

- Temperature is typed manually; there is no live sensor input.
- Only temperature is considered; humidity, occupancy, and energy use are not.
- Three rules and triangular sets are intentionally simple and may not match
  the tuning of a real fan or room.
- The application only recommends a speed and cannot control hardware.

## 12. Future enhancements

- Add humidity or occupancy as additional fuzzy input variables.
- Let a user compare or adjust membership-function shapes.
- Add a real sensor and fan only as a separate, safely designed hardware
  extension.
- Explore energy-aware rules and compare the results with other control
  strategies.

## 13. Conclusion

The project demonstrates a complete Mamdani fuzzy controller for a
temperature-based fan-speed recommendation. Its overlapping membership
functions, rules, and centroid defuzzification produce valid, non-decreasing
recommendations across the accepted temperature range. The Tkinter GUI and
Matplotlib plots make the result easier to demonstrate and explain. It remains
a simulation and does not control a physical fan.

## 14. Viva questions and simple answers

1. **What is fuzzy logic?**  
   It represents degrees of truth between 0 and 1 rather than only true or
   false.

2. **What is a crisp input?**  
   It is the exact measured or entered value, such as 27.5°C.

3. **What is a membership function?**  
   It maps an input value to a membership degree in a fuzzy set.

4. **What does fuzzification do?**  
   It converts the crisp temperature into its Low, Medium, and High
   membership degrees.

5. **Why do the membership functions overlap?**  
   Overlap lets a value belong partly to neighboring categories and avoids
   abrupt changes.

6. **What are the fuzzy rules in this project?**  
   Low temperature gives Low fan speed, Medium gives Medium, and High gives
   High.

7. **What is Mamdani inference?**  
   It is a fuzzy-inference method where rules produce fuzzy output sets.

8. **What does the fuzzy control system do?**  
   It evaluates the input memberships, applies the rules, and combines their
   output sets.

9. **What is defuzzification?**  
   It converts the combined fuzzy output into one crisp numerical value.

10. **Which defuzzification method is used?**  
    Centroid, which finds the balance point of the combined output set.

11. **Why is the output universe 0–100?**  
    Fan speed is represented as a percentage, so the domain covers zero to
    full speed.

12. **How is the displayed temperature category chosen?**  
    It is the category with the greatest membership degree at the input
    temperature.

13. **Does the program control a real fan?**  
    No. It only simulates a recommendation; no physical fan or sensor is
    connected.

14. **What is the role of Tkinter?**  
    Tkinter creates the desktop window, input field, buttons, labels, and
    progress bar.

15. **What is the role of Matplotlib?**  
    Matplotlib draws the temperature and fan-speed membership-function
    graphs.
