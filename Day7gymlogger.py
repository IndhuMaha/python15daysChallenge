import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
LOG_FILE = "workout_log.csv"

# Predefined exercises
DEFAULT_EXERCISES = [
    "Bench Press", "Squat", "Deadlift", "Overhead Press", "Barbell Row",
    "Pull-Ups", "Push-Ups", "Dumbbell Curl", "Lateral Raise", "Leg Press",
    "Lat Pulldown", "Cable Row", "Triceps Pushdown", "Plank", "Russian Twist",
    "Hip Thrust", "Farmer's Walk", "Face Pull", "Bulgarian Split Squat"
]

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def init_log_file():
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=["Date", "Exercise", "Sets", "Reps", "Weight"])
        df.to_csv(LOG_FILE, index=False)

def load_data():
    return pd.read_csv(LOG_FILE)

def save_entry(date, exercise, sets, reps, weight):
    df = load_data()
    new_entry = pd.DataFrame([{
        "Date": date,
        "Exercise": exercise,
        "Sets": sets,
        "Reps": reps,
        "Weight": weight
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)

def calculate_volume(row):
    return row["Sets"] * row["Reps"] * row["Weight"]

# ----------------------------
# STREAMLIT APP — NO CUSTOM CSS, NATIVE & RELIABLE
# ----------------------------
st.set_page_config(
    page_title="💪 My Gym Logger",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Simple title
st.title("💪 My Gym Workout Logger")
st.markdown("### _Track your lifts. See your progress._")

# Initialize log file
init_log_file()

# ----------------------------
# INPUT FORM — NATIVE STREAMLIT STYLING
# ----------------------------
st.header("📝 Log Your Workout")

# Load existing exercises
df_existing = load_data()
existing_exercises = df_existing["Exercise"].dropna().unique().tolist() if not df_existing.empty else []
all_exercises = list(set(DEFAULT_EXERCISES + existing_exercises))
all_exercises.sort()
all_exercises.append("➕ Add Custom Exercise")

with st.form("workout_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        selected_exercise = st.selectbox(
            "Exercise",
            all_exercises,
            help="Choose from list or add custom"
        )
        sets = st.number_input("Sets", min_value=1, step=1, value=3)
        reps = st.number_input("Reps per Set", min_value=1, step=1, value=10)

    with col2:
        if selected_exercise == "➕ Add Custom Exercise":
            exercise = st.text_input("Custom Exercise Name", placeholder="e.g., Zottman Curl")
        else:
            exercise = selected_exercise

        weight = st.number_input(
            "Weight (kg/lbs)",
            min_value=0.0,
            step=0.5,
            value=50.0,
            help="External weight lifted — not body weight"
        )

    # ✅ Simple, native button — black text by default in light/dark mode
    submitted = st.form_submit_button("✅ Log Workout", type="primary", use_container_width=True)

    if submitted:
        if not exercise or exercise.strip() == "":
            st.error("⚠️ Please enter or select an exercise.")
        elif exercise == "➕ Add Custom Exercise":
            st.error("⚠️ Please enter a custom exercise name.")
        else:
            today = datetime.today().strftime("%Y-%m-%d")
            save_entry(today, exercise.strip(), sets, reps, weight)
            st.success(f"✅ Logged: **{exercise}** — {sets} x {reps} @ {weight}")

st.divider()

# ----------------------------
# DISPLAY HISTORY
# ----------------------------
st.header("📊 Workout History")

df = load_data()

if df.empty:
    st.info("📭 No workouts logged yet. Start above!")
else:
    # Calculate volume
    df["Volume"] = df.apply(calculate_volume, axis=1)
    df["Date"] = pd.to_datetime(df["Date"])
    df_display = df[["Date", "Exercise", "Sets", "Reps", "Weight", "Volume"]].sort_values("Date", ascending=False)
    df_display["Date"] = df_display["Date"].dt.strftime("%b %d, %Y")

    st.dataframe(df_display, use_container_width=True)

    st.divider()

    # ----------------------------
    # WEEKLY PROGRESS GRAPH
    # ----------------------------
    st.header("📈 Weekly Progress (Total Volume)")

    df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
    weekly_volume = df.groupby('Week')["Volume"].sum().reset_index()
    weekly_volume['Week'] = weekly_volume['Week'].dt.strftime('%Y-%m-%d')

    if len(weekly_volume) > 0:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(
            weekly_volume['Week'],
            weekly_volume['Volume'],
            marker='o',
            linestyle='-',
            linewidth=2,
            color='#0066cc'
        )
        ax.set_title("Weekly Total Volume (Sets × Reps × Weight)")
        ax.set_xlabel("Week Starting")
        ax.set_ylabel("Volume")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("⏳ Log more workouts to see progress.")

    st.divider()

    # ----------------------------
    # DOWNLOAD BUTTON
    # ----------------------------
    st.download_button(
        label="📥 Download CSV Log",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='gym_log.csv',
        mime='text/csv',
        use_container_width=True
    )

# ----------------------------
# FOOTER
# ----------------------------
st.caption("💡 Weight = external load (barbell, dumbbell, etc.) — not body weight")
st.caption("🔁 Log consistently to track real progress!")