import streamlit as st
import datetime
import matplotlib.pyplot as plt

# --- Constants ---
DAILY_GOAL_LITERS = 3.0
DATE_TODAY = datetime.date.today()

# --- Initialize session state ---
if "water_log" not in st.session_state:
    st.session_state.water_log = {}  # {date: intake}

# --- Title ---
st.title("💧 Daily Water Tracker")
st.subheader(f"Goal: {DAILY_GOAL_LITERS} Liters per day")

# --- Input Section ---
st.markdown("### 🚰 Log Today's Intake")
intake = st.number_input("Enter water intake (liters)", min_value=0.0, step=0.1)

if st.button("Add Intake"):
    today = DATE_TODAY
    st.session_state.water_log[today] = st.session_state.water_log.get(today, 0.0) + intake
    st.success(f"Added {intake}L to {today}'s total!")

# --- Progress Section ---
today_intake = st.session_state.water_log.get(DATE_TODAY, 0.0)
progress = min(today_intake / DAILY_GOAL_LITERS, 1.0)

st.markdown("### 📊 Today's Progress")
st.progress(progress)
st.write(f"**{today_intake:.2f}L / {DAILY_GOAL_LITERS}L**")

# --- Weekly Chart ---
st.markdown("### 📅 Weekly Hydration Chart")

# Prepare last 7 days data
dates = [DATE_TODAY - datetime.timedelta(days=i) for i in range(6, -1, -1)]
intakes = [st.session_state.water_log.get(date, 0.0) for date in dates]

fig, ax = plt.subplots()
ax.bar([d.strftime("%a") for d in dates], intakes, color="#00BFFF")
ax.axhline(DAILY_GOAL_LITERS, color="gray", linestyle="--", label="Daily Goal")
ax.set_ylabel("Liters")
ax.set_title("Water Intake Over Last 7 Days")
ax.legend()

st.pyplot(fig)

# --- Reset Option ---
if st.button("Reset Today's Intake"):
    st.session_state.water_log[DATE_TODAY] = 0.0
    st.info("Today's intake has been reset.")

# --- Optional: Show full log ---
with st.expander("📜 View Full Intake Log"):
    for date, liters in sorted(st.session_state.water_log.items()):
        st.write(f"{date}: {liters:.2f}L")
