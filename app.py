# import streamlit as st
# import joblib
# import numpy as np

# st.title("Battery Thermal Management System")

# # Load models
# temp_model = joblib.load("temp_model.pkl")
# soh_model = joblib.load("soh_model.pkl")
# risk_model = joblib.load("risk_model.pkl")

# st.sidebar.header("Battery Inputs")

# voltage = st.sidebar.slider("Voltage",3.0,4.2,3.7)
# current = st.sidebar.slider("Current",0.5,5.0,2.0)
# temperature = st.sidebar.slider("Temperature",20,60,30)
# cycle = st.sidebar.slider("Cycle",1,500,100)

# power = voltage * current

# features = np.array([[voltage,current,temperature,cycle,power]])

# temp = temp_model.predict(features)
# soh = soh_model.predict(features)
# risk = risk_model.predict(features)

# st.metric("Battery Temperature",round(temp[0],2))
# st.metric("Battery SOH",round(soh[0],2))

# if risk[0]==1:
#     st.error("Thermal Risk Detected")
# else:
#     st.success("Battery Safe")

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="Battery Thermal Management System",
    layout="wide"
)

st.title("🔋 Battery Thermal Management Dashboard")

# Load models
temp_model = joblib.load("temp_model.pkl")
soh_model = joblib.load("soh_model.pkl")
risk_model = joblib.load("risk_model.pkl")

# Sidebar Inputs
st.sidebar.header("⚙️ Battery Parameters")

voltage = st.sidebar.slider("Voltage (V)",3.0,4.2,3.7)
current = st.sidebar.slider("Current (A)",0.5,5.0,2.0)
temperature = st.sidebar.slider("Ambient Temperature (°C)",20,60,30)
cycle = st.sidebar.slider("Cycle Number",1,500,100)

power = voltage * current

features = np.array([[voltage,current,temperature,cycle,power]])

# Predictions
temp = temp_model.predict(features)[0]
soh = soh_model.predict(features)[0]
risk = risk_model.predict(features)[0]

# Metrics Layout
col1, col2, col3 = st.columns(3)

col1.metric("🌡 Battery Temperature", f"{temp:.2f} °C")
col2.metric("🔋 Battery Health (SOH)", f"{soh:.2f} %")
col3.metric("⚡ Power", f"{power:.2f} W")

# Risk Alert
st.subheader("Battery Status")

if risk == 1:
    st.error("⚠️ Thermal Runaway Risk Detected")
else:
    st.success("✅ Battery Operating Safely")

# Progress Bar
st.subheader("Battery Health Indicator")
st.progress(int(max(min(soh,100),0)))

# Graph Section
st.subheader("📊 Battery Performance Graphs")

# Create sample data for visualization
cycles = np.arange(1,500)

temp_curve = temp + np.random.normal(0,1,499)
soh_curve = 100 - cycles*0.05

fig, ax = plt.subplots()
ax.plot(cycles,temp_curve,label="Temperature")
ax.set_xlabel("Cycle")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Battery Temperature vs Cycle")
ax.legend()

st.pyplot(fig)

fig2, ax2 = plt.subplots()
ax2.plot(cycles,soh_curve,label="SOH",color="green")
ax2.set_xlabel("Cycle")
ax2.set_ylabel("SOH (%)")
ax2.set_title("Battery SOH vs Cycle")
ax2.legend()

st.pyplot(fig2)

# Raw Data Section
st.subheader("📋 Current Input Data")

data = {
    "Voltage":[voltage],
    "Current":[current],
    "Temperature":[temperature],
    "Cycle":[cycle],
    "Power":[power]
}

df = pd.DataFrame(data)

st.dataframe(df)