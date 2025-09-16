

import streamlit as st

# ----------------------------
# STATIC EXCHANGE RATES (as of sample date)
# Base Currency: USD (1 USD = X)
# ----------------------------
EXCHANGE_RATES = {
    "USD": 1.0,        # US Dollar
    "EUR": 0.93,       # Euro
    "GBP": 0.79,       # British Pound
    "JPY": 156.0,      # Japanese Yen
    "INR": 83.5,       # Indian Rupee
    "CAD": 1.37,       # Canadian Dollar
    "AUD": 1.53,       # Australian Dollar
    "CHF": 0.90,       # Swiss Franc
    "CNY": 7.25,       # Chinese Yuan
}

# ----------------------------
# APP TITLE
# ----------------------------
st.set_page_config(page_title="💱 Currency Converter", page_icon="💱")
st.title("💱 Simple Currency Converter")
st.markdown("Convert between major currencies using static rates.")

# ----------------------------
# USER INPUTS
# ----------------------------
st.subheader("Enter Conversion")

# Get list of currency codes
currencies = list(EXCHANGE_RATES.keys())

col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox("From Currency", currencies, index=0)

with col2:
    to_currency = st.selectbox("To Currency", currencies, index=1)

amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.01)

# ----------------------------
# CONVERT & DISPLAY
# ----------------------------
if amount > 0:
    # Convert to USD first, then to target currency
    usd_amount = amount / EXCHANGE_RATES[from_currency]
    converted_amount = usd_amount * EXCHANGE_RATES[to_currency]

    st.subheader("🔁 Result")
    st.success(f"**{amount:,.2f} {from_currency}** = **{converted_amount:,.2f} {to_currency}**")

    # Show exchange rate used
    rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]
    st.caption(f"Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")
else:
    st.info("Enter an amount greater than 0 to see conversion.")

# ----------------------------
# FOOTER
# ----------------------------
st.divider()
st.caption("ℹ️ Rates are static and for demonstration only. Not real-time.")
st.caption("✅ Built with Streamlit — Simple, Fast, Reliable")


