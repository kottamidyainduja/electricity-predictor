import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Electricity Predictor", layout="centered")

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center; color:#00C9A7;'>⚡ Electricity Consumption & Bill Predictor</h1>", unsafe_allow_html=True)

st.write("This system predicts electricity consumption and estimates the bill using machine learning based on user inputs.")

# ---------------- LOAD DATA ----------------
if not os.path.exists("electricity_units.csv"):
    st.error("Dataset not found!")
    st.stop()

df = pd.read_csv("electricity_units.csv")

# ---------------- MODEL ----------------
X = df[['Past_Units', 'No_of_People', 'Season']]
y = df['Current_Units']

model = LinearRegression()
model.fit(X, y)

# ---------------- INPUT FORM ----------------
st.subheader("📝 Enter Details")

with st.form("form"):
    past_units = st.number_input("Last Month Units", 0, 1000, 100)
    people = st.slider("Number of People", 1, 10, 3)
    season = st.selectbox("Season", ["Winter", "Summer", "Rainy"])
    submit = st.form_submit_button("🚀 Predict")

season_map = {"Winter": 0, "Summer": 1, "Rainy": 2}

# ---------------- BILL FUNCTION ----------------
def calculate_bill(units):
    if units <= 100:
        return units * 2
    elif units <= 200:
        return (100 * 2) + (units - 100) * 4
    else:
        return (100 * 2) + (100 * 4) + (units - 200) * 6

# ---------------- OUTPUT ----------------
if submit:
    input_data = pd.DataFrame({
        'Past_Units': [past_units],
        'No_of_People': [people],
        'Season': [season_map[season]]
    })

    predicted_units = model.predict(input_data)[0]
    bill = calculate_bill(predicted_units)

    # -------- RESULTS --------
    st.subheader("📊 Prediction Results")

    col1, col2 = st.columns(2)
    col1.metric("🔋 Predicted Units", f"{predicted_units:.2f}")
    col2.metric("💰 Estimated Bill", f"₹ {bill:.2f}")

    st.info("Model used: Linear Regression (Machine Learning)")

    # -------- CATEGORY --------
    if predicted_units <= 100:
        category = "Low Usage"
    elif predicted_units <= 200:
        category = "Moderate Usage"
    else:
        category = "High Usage"

    st.success(f"⚡ Usage Category: {category}")

    
    # -------- INSIGHTS --------
    st.subheader("🧠 Insights")

    if predicted_units > past_units:
        st.write("📈 Consumption is expected to increase compared to last month.")
    else:
        st.write("📉 Consumption is stable or decreasing.")

    if people > 4:
        st.write("👨‍👩‍👧 More people increases electricity usage.")

    if season == "Summer":
        st.write("☀️ Summer increases usage due to AC and cooling appliances.")

    # -------- SAVING TIPS --------
    st.subheader("💡 Energy Saving Tips")

    if predicted_units > 200:
        st.write("• Use energy-efficient appliances")
        st.write("• Reduce AC usage")
        st.write("• Turn off unused devices")
    elif predicted_units > 120:
        st.write("• Optimize fan and light usage")
        st.write("• Avoid standby power consumption")
    else:
        st.write("• Great! Maintain your usage 👍")

    

    # -------- CLEAN INTERACTIVE GRAPH --------
    st.subheader("📊 Electricity Consumption vs Cost Analysis")

    units_range = list(range(0, 300))
    bills = [calculate_bill(u) for u in units_range]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=units_range,
        y=bills,
        mode='lines',
        name='Bill Curve'
    ))

    fig.update_layout(
        title="Electricity Bill vs Units",
        xaxis_title="Units Consumed",
        yaxis_title="Bill (₹)",
        hovermode='x'
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Enter details and click Predict")