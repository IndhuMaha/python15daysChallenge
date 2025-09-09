import streamlit as st

# Title
st.title("👋 Welcome Buddy")

# Form layout
with st.form("user_form"):
    name = st.text_input("Enter your name")
    age = st.slider("Select your age", min_value=0, max_value=120, step=1)
    submitted = st.form_submit_button("Submit")

# Validation and response
if submitted:
    if not name:
        st.error("⚠️ Please enter your name.")
    elif age == 0:
        st.error("⚠️ Please select a valid age.")
    else:
        st.success(f"🎉 Hello {name}! You are {age} years young.")
