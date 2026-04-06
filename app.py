import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go

# ---------------- PAGE ----------------
st.set_page_config(page_title="Electricity Predictor", layout="centered")
st.title("⚡ Electricity Consumption & Bill Predictor")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("electricity_units.csv")

# ---------------- ENCODING ----------------
season_map = {"Winter":0, "Summer":1, "Rainy":2}
house_map = {"1BHK":1, "2BHK":2, "3BHK":3}

df['Season'] = df['Season'].map(season_map)
df['House_Type'] = df['House_Type'].map(house_map)

# ---------------- MODEL ----------------
features = ['Prev_Month_Units','No_of_People','Season','Temperature',
            'House_Size','House_Type','Num_Appliances','Usage_Hours','Tariff']

X = df[features]
y = df['Units_Consumed']

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# ---------------- INPUT ----------------
st.subheader("📝 Enter Details")

prev_units = st.number_input("Previous Month Units", 0, 1000, 200)
people = st.number_input("Number of People", 1, 10, 3)
season = st.selectbox("Season", ["Winter","Summer","Rainy"])
temp = st.number_input("Temperature (°C)", 0, 50, 28)
house_size = st.number_input("House Size (sq.ft)", 200, 5000, 1000)
house_type = st.selectbox("House Type", ["1BHK","2BHK","3BHK"])
appliances = st.number_input("Number of Appliances", 1, 30, 10)
usage_hours = st.number_input("Usage Hours per Day", 1, 24, 6)
tariff = st.number_input("Electricity Tariff (₹/unit)", 1, 20, 5)

# ---------------- BILL FUNCTION ----------------
def calculate_bill(units):
    if units <= 100:
        return units * 2
    elif units <= 200:
        return (100*2) + (units-100)*4
    else:
        return (100*2) + (100*4) + (units-200)*6

# ---------------- PREDICT ----------------
if st.button("🚀 Predict"):

    input_data = pd.DataFrame({
        'Prev_Month_Units':[prev_units],
        'No_of_People':[people],
        'Season':[season_map[season]],
        'Temperature':[temp],
        'House_Size':[house_size],
        'House_Type':[house_map[house_type]],
        'Num_Appliances':[appliances],
        'Usage_Hours':[usage_hours],
        'Tariff':[tariff]
    })

    pred_units = round(model.predict(input_data)[0])
    bill = calculate_bill(pred_units)

    # ---------------- RESULTS ----------------
    st.subheader("📊 Prediction Results")

    col1, col2 = st.columns(2)
    col1.metric("🔋 Predicted Units", f"{pred_units} units")
    col2.metric("💰 Estimated Bill", f"₹ {bill}")

    # ---------------- CATEGORY ----------------
    if pred_units <= 150:
        category = "Low Usage"
    elif pred_units <= 300:
        category = "Moderate Usage"
    else:
        category = "High Usage"

    st.success(f"⚡ Usage Category: {category}")

    # ---------------- INSIGHTS ----------------
    st.subheader("🧠 Insights")

    if pred_units > prev_units:
        st.write("📈 Consumption is expected to increase.")
    else:
        st.write("📉 Consumption is stable or decreasing.")

    if season == "Summer":
        st.write("☀️ High usage due to cooling appliances.")
    elif season == "Winter":
        st.write("❄️ Moderate usage expected.")

    if appliances > 12:
        st.write("⚠️ More appliances increase electricity consumption.")

    # ---------------- ENERGY TIPS ----------------
    st.subheader("💡 Energy Saving Tips")

    if pred_units > 350:
        st.write("• Reduce AC usage")
        st.write("• Use energy-efficient appliances")
        st.write("• Turn off unused devices")
    elif pred_units > 200:
        st.write("• Optimize usage of appliances")
        st.write("• Avoid standby power")
    else:
        st.write("• Good usage! Maintain 👍")

    # ---------------- GRAPH ----------------
    st.subheader("📊 Electricity Consumption vs Cost Analysis")

    units_range = list(range(0, pred_units + 100))
    bills = [calculate_bill(u) for u in units_range]

    fig = go.Figure()

    # Bill curve
    fig.add_trace(go.Scatter(
        x=units_range,
        y=bills,
        mode='lines',
        name='Bill Curve'
    ))

    # Predicted point
    fig.add_trace(go.Scatter(
        x=[pred_units],
        y=[bill],
        mode='markers',
        name='Predicted Point',
        marker=dict(size=10)
    ))

    fig.update_layout(
        title="Electricity Bill vs Units",
        xaxis_title="Units Consumed",
        yaxis_title="Bill (₹)",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Enter details and click Predict")
