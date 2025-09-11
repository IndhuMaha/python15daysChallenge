import streamlit as st

# Step 1: Initialize session state
if "reset_triggered" not in st.session_state:
    st.session_state.reset_triggered = False
if "result" not in st.session_state:
    st.session_state.result = ""
if "calc_text" not in st.session_state:
    st.session_state.calc_text = ""
if "error" not in st.session_state:
    st.session_state.error = ""

# Step 2: Reset logic BEFORE rendering widgets
if st.session_state.reset_triggered:
    st.session_state.input1_value = ""
    st.session_state.input2_value = ""
    st.session_state.result = ""
    st.session_state.calc_text = ""
    st.session_state.error = ""
    st.session_state.reset_triggered = False

# Step 3: Title
st.title("🧮 Simple Calculator")

# Step 4: Input fields
input1 = st.text_input("Enter first number", key="input1_value")
input2 = st.text_input("Enter second number", key="input2_value")

# Step 5: Operation selection
operation = st.selectbox("Choose operation", ["Add", "Subtract", "Multiply", "Divide"])

# Step 6: Buttons with message
col1, col2 = st.columns([1, 2])
calculate = col1.button("Calculate")
with col2:
    reset = st.button("Reset")
    st.caption("🛈 Double click the button")

# Step 7: Reset flag
if reset:
    st.session_state.reset_triggered = True

# Step 8: Calculation logic
if calculate:
    try:
        a = float(input1)
        b = float(input2)

        if operation == "Add":
            result = a + b
            symbol = "+"
        elif operation == "Subtract":
            result = a - b
            symbol = "-"
        elif operation == "Multiply":
            result = a * b
            symbol = "×"
        elif operation == "Divide":
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = a / b
            symbol = "÷"

        st.session_state.result = f"The result is {result}"
        st.session_state.calc_text = f"Calculation: {a} {symbol} {b}"
        st.session_state.error = ""

    except ValueError:
        st.session_state.result = ""
        st.session_state.calc_text = ""
        st.session_state.error = "❌ Please enter valid numbers."
    except ZeroDivisionError as e:
        st.session_state.result = ""
        st.session_state.calc_text = ""
        st.session_state.error = f"❌ {e}"

# Step 9: Display output
if st.session_state.result:
    st.success(st.session_state.result)
if st.session_state.calc_text:
    st.info(st.session_state.calc_text)
if st.session_state.error:
    st.error(st.session_state.error)
