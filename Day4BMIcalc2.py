import streamlit as st
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="BMI Calculator", page_icon="🧍‍♂️", layout="centered")

# --- Title ---
st.title("🎯 BMI Calculator (WHO Standard)")

# --- WHO BMI Classification ---
st.markdown("### 📊 WHO BMI Classification")
st.table({
    "Category": ["Underweight", "Normal weight", "Overweight", "Obese"],
    "BMI Range": ["< 18.5", "18.5 – 24.9", "25.0 – 29.9", "≥ 30.0"]
})

# --- Age & Gender ---
st.markdown("### 🧬 Personal Info")
col_age, col_gender = st.columns(2)
with col_age:
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
with col_gender:
    gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)

# --- Unit Selection Toggles ---
st.markdown("### ⚙️ Select Units")
unit_col1, unit_col2 = st.columns(2)
with unit_col1:
    height_unit = "cm" if st.toggle("Height in cm", value=True) else "feet"
with unit_col2:
    weight_unit = "kg" if st.toggle("Weight in kg", value=True) else "lb"

# --- Input Fields ---
st.markdown("### ✍️ Enter Your Height and Weight")
input_col1, input_col2 = st.columns(2)
with input_col1:
    height = st.number_input(f"Height ({height_unit})", min_value=0.0, format="%.2f")
with input_col2:
    weight = st.number_input(f"Weight ({weight_unit})", min_value=0.0, format="%.2f")

# --- Conversion Logic ---
def convert_to_metric(height, weight, h_unit, w_unit):
    height_cm = height * 30.48 if h_unit == "feet" else height
    weight_kg = weight * 0.453592 if w_unit == "lb" else weight
    return height_cm, weight_kg

# --- Custom Balloons ---
def show_custom_balloons():
    st.markdown("""
    <style>
    .balloon {
        position: fixed;
        bottom: -100px;
        left: 50%;
        animation: floatUp 10s ease-in-out infinite;
        font-size: 50px;
        z-index: 9999;
    }
    @keyframes floatUp {
        0% { bottom: -100px; opacity: 0; }
        50% { opacity: 1; }
        100% { bottom: 100vh; opacity: 0; }
    }
    </style>
    <div class="balloon">🎈</div>
    <div class="balloon" style="left: 30%;">🎈</div>
    <div class="balloon" style="left: 70%;">🎈</div>
    """, unsafe_allow_html=True)

# --- Health Tips ---
def get_health_tip(category):
    tips = {
        "Underweight": "💡 Tip: Include more nutrient-rich foods like nuts, dairy, and whole grains. Consider consulting a dietitian.",
        "Normal weight": "💡 Tip: Maintain your weight with regular physical activity and a balanced diet.",
        "Overweight": "💡 Tip: Try reducing sugar and processed foods. Walking 30 minutes a day can make a big difference.",
        "Obese": "💡 Tip: Focus on portion control and consult a healthcare provider for a personalized plan."
    }
    return tips.get(category, "")

# --- BMI Gauge ---
def show_bmi_gauge(bmi):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        title={'text': "Your BMI"},
        gauge={
            'axis': {'range': [0, 40]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 18.5], 'color': "lightblue"},
                {'range': [18.5, 25], 'color': "lightgreen"},
                {'range': [25, 30], 'color': "orange"},
                {'range': [30, 40], 'color': "red"},
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# --- Calculate Button ---
if st.button("🚀 Calculate BMI"):
    if height > 0 and weight > 0:
        height_cm, weight_kg = convert_to_metric(height, weight, height_unit, weight_unit)
        height_m = height_cm / 100
        bmi = round(weight_kg / (height_m ** 2), 2)

        # --- Classification & Emoji Feedback ---
        if bmi < 18.5:
            category = "Underweight"
            message = "You are underweight. Consider consulting a healthcare provider."
            emoji = "😟"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            message = "You have a healthy weight. Great job!"
            emoji = "🎉😊"
            show_custom_balloons()
        elif 25 <= bmi < 30:
            category = "Overweight"
            message = "You are overweight. A balanced diet and regular exercise can help."
            emoji = "🤔"
        else:
            category = "Obese"
            message = "You are in the obese range. It's important to seek medical advice."
            emoji = "😢"

        # --- Result Display ---
        st.markdown(f"## ✅ Your BMI is **{bmi}** — *{category}* {emoji}")
        st.info(message)

        # --- Visual Gauge ---
        show_bmi_gauge(bmi)

        # --- Health Tip ---
        st.markdown(get_health_tip(category))
    else:
        st.error("Please enter valid height and weight to calculate your BMI.")
