import streamlit as st
import pandas as pd
import io
import plotly.express as px

# Page setup
st.set_page_config(page_title="Expense Splitter", layout="centered")
st.title("💸 Expense Splitter App")
st.markdown("Split expenses among friends and track who owes what.")

# Initialize session state
if "total_amount" not in st.session_state:
    st.session_state["total_amount"] = 0.0
if "num_people" not in st.session_state:
    st.session_state["num_people"] = 2

# Input: Total amount and number of people
total_amount = st.number_input("Enter Total Expense Amount", min_value=0.0, format="%.2f", key="total_amount")
num_people = st.number_input("Enter Number of People", min_value=1, max_value=20, value=st.session_state["num_people"], key="num_people")

# Display per-person share immediately
if total_amount > 0 and num_people > 0:
    per_person_share = total_amount / num_people
    st.info(f"💡 Each person should contribute: ₹{per_person_share:.2f}")

# Initialize dynamic fields
for i in range(num_people):
    st.session_state.setdefault(f"name_{i}", "")
    st.session_state.setdefault(f"contrib_{i}", 0.0)

# Input: Names and Contributions
st.subheader("Enter Names and Their Contributions")
names = []
contributions = []

for i in range(num_people):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"Name of Person {i+1}", key=f"name_{i}")
    with col2:
        contribution = st.number_input(f"Contribution by {name or f'Person {i+1}'}", min_value=0.0, format="%.2f", key=f"contrib_{i}")
    names.append(name)
    contributions.append(contribution)

# Buttons: Calculate and Clear
col_calc, col_clear = st.columns([1, 1])
calculate_clicked = col_calc.button("Calculate Split")
clear_clicked = col_clear.button("Clear All")

# Clear all inputs
if clear_clicked:
    st.session_state["total_amount"] = 0.0
    st.session_state["num_people"] = 2
    for i in range(20):
        st.session_state[f"name_{i}"] = ""
        st.session_state[f"contrib_{i}"] = 0.0
    st.experimental_rerun()

# Calculate and display results
if calculate_clicked:
    if total_amount == 0 or any(name.strip() == "" for name in names):
        st.warning("Please enter a valid total amount and all names.")
    else:
        per_person_share = total_amount / num_people
        st.success(f"Each person should contribute: ₹{per_person_share:.2f}")

        balances = [round(per_person_share - c, 2) for c in contributions]
        data = {
            "Name": names,
            "Contributed": contributions,
            "Balance": balances
        }

        df = pd.DataFrame(data)

        st.subheader("💰 Contribution Summary")
        st.dataframe(df)

        # Pie Chart of Contributions with amount and percentage labels
        st.subheader("📊 Contribution Breakdown")
        fig = px.pie(
            df,
            names="Name",
            values="Contributed",
            title="Who Paid What",
            hole=0.3
        )
        fig.update_traces(
            textinfo='label+percent+value',
            textposition='inside'
        )
        st.plotly_chart(fig, use_container_width=True)

        # People who owe money or should be refunded
        st.subheader("🔍 Settlement Status")
        owes = df[df["Balance"] > 0]
        overpaid = df[df["Balance"] < 0]

        if not owes.empty:
            for _, row in owes.iterrows():
                st.write(f"👉 {row['Name']} owes ₹{row['Balance']:.2f}")
        if not overpaid.empty:
            for _, row in overpaid.iterrows():
                st.write(f"✅ {row['Name']} should be returned ₹{abs(row['Balance']):.2f}")
        if owes.empty and overpaid.empty:
            st.success("All contributions are perfectly balanced! 🎉")

        # Export as CSV
        st.subheader("📥 Download Summary")
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download CSV",
            data=csv_buffer.getvalue(),
            file_name="expense_summary.csv",
            mime="text/csv"
        )
