# 🧮 BMI Calculator — Python

A desktop-based **BMI (Body Mass Index) Calculator** built with Python and Tkinter. The application provides a clean graphical interface for calculating BMI, validating user input, classifying BMI results, and visualizing BMI data.

This project was developed as a practical Python application to demonstrate GUI development, event-driven programming, input validation, data processing, and data visualization.

---

## 📌 Overview

The BMI Calculator allows users to enter their weight and height and instantly calculate their Body Mass Index.

The application then classifies the calculated BMI into one of four standard categories:

- Underweight
- Normal Weight
- Overweight
- Obese

The application also provides graphical feedback and visualization using Matplotlib.

---

## ✨ Features

### 🧮 BMI Calculation
- Calculates BMI using weight and height.
- Displays the calculated BMI rounded to two decimal places.
- Uses the standard BMI formula.

### 🎨 Graphical User Interface
- Built with Python's Tkinter library.
- Simple and user-friendly interface.
- Dedicated input fields for weight and height.
- Calculate button for processing the input.
- Clear result display.

### 📊 BMI Classification
The application categorizes BMI values into standard ranges:

| BMI Range | Category |
|-----------|----------|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal Weight |
| 25.0 – 29.9 | Overweight |
| 30.0 and above | Obese |

### ✅ Input Validation
The application handles invalid input such as:

- Empty fields
- Non-numeric values
- Zero or negative values
- Invalid height or weight values

Helpful error messages are displayed when invalid data is entered.

### 📈 Data Visualization
- Uses Matplotlib for graphical visualization.
- Helps users understand BMI results visually.
- Supports BMI trend visualization where applicable.

### ⚠️ Error Handling
The application includes error handling to prevent crashes caused by invalid user input and unexpected runtime conditions.

---

## 🧠 BMI Formula

The application calculates BMI using the following formula:

```text
BMI = Weight (kg) / Height² (m)
