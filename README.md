# ⚡ Electricity Consumption & Bill Predictor

## 📌 Overview

This project is a Machine Learning-based web application that predicts **next month’s electricity consumption (units)** and estimates the **electricity bill** based on user inputs such as household characteristics and usage patterns.

The application is built using **Streamlit** and a **Random Forest Regression model**.

---

## 🎯 Objectives

* Predict future electricity consumption accurately
* Estimate electricity bill using slab-based pricing
* Provide insights into energy usage
* Suggest energy-saving tips

---

## ⚙️ Features

* 📊 Predicts electricity units for next month
* 💰 Calculates bill using realistic slab rates
* 📈 Interactive graph (Units vs Bill)
* 🧠 Intelligent insights based on inputs
* 💡 Energy-saving recommendations
* ⚡ Usage category classification (Low / Moderate / High)

---

## 🧾 Input Parameters

The model uses the following features:

* Previous month electricity units
* Number of people in the house
* Season (Winter, Summer, Rainy)
* Temperature (°C)
* House size (sq.ft)
* House type (1BHK, 2BHK, 3BHK)
* Number of appliances
* Appliance usage hours per day
* Electricity tariff (₹/unit)

---

## 🧠 Machine Learning Model

* Model Used: **Random Forest Regressor**
* Type: Supervised Learning (Regression)
* Target Variable: Electricity Units Consumed

The model is trained on historical data to learn patterns between household features and electricity consumption.

---

## 💰 Billing Logic

Electricity bill is calculated using slab-based pricing:

* 0–100 units → ₹2/unit
* 101–200 units → ₹4/unit
* Above 200 units → ₹6/unit

---

## 📊 Visualization

The app generates an interactive graph showing:

* Electricity Units (X-axis)
* Electricity Bill (Y-axis)
* Predicted consumption point

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* Scikit-learn
* Plotly

---

## ▶️ How to Run

1. Install dependencies:

   ```bash
   pip install streamlit pandas scikit-learn plotly
   ```

2. Run the app:

   ```bash
   streamlit run app.py
   ```

---
