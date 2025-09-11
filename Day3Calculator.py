import streamlit as st

# Title
st.title("🧮 Simple Calculator")

# Input fields
num1 = st.text_input("Enter first number")
num2 = st.text_input("Enter second number")

# Operation selection
operation = st.selectbox("Choose operation", ["Add", "Subtract", "Multiply", "Divide"])

# Buttons
col1, col2 = st.columns(2)
calculate = col1.button("Calculate")
clear = col2.button("Clear")

# Result placeholder
result_placeholder = st.empty()
calc_text_placeholder = st.empty()
error_placeholder = st.empty()

# Clear button logic
if clear:
    st.experimental_rerun()

# Calculation logic
if calculate:
    try:
        a = float(num1)
        b = float(num2)
        error_placeholder.empty()  # Clear previous errors

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

        # Display result
        result_placeholder.success(f"The result is {result}")
        calc_text_placeholder.info(f"Calculation: {a} {symbol} {b}")

    except ValueError:
        error_placeholder.error("❌ Please enter valid numbers.")
    except ZeroDivisionError as e:
        error_placeholder.error(f"❌ {e}")
