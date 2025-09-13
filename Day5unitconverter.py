import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Universal Unit Converter",
    page_icon="📊",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .conversion-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .result-box {
        background-color: #e6f3ff;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="main-header">🔁 Universal Unit Converter</h1>', unsafe_allow_html=True)

# Conversion categories
conversion_type = st.selectbox(
    "Select Conversion Type:",
    ["Currency", "Temperature", "Length", "Weight"],
    index=0
)

st.markdown('<div class="conversion-box">', unsafe_allow_html=True)

# Currency Conversion
if conversion_type == "Currency":
    st.subheader("💱 Currency Converter")
    
    # Currency options (major currencies)
    currencies = {
        "USD": "US Dollar",
        "EUR": "Euro",
        "GBP": "British Pound",
        "JPY": "Japanese Yen",
        "CAD": "Canadian Dollar",
        "AUD": "Australian Dollar",
        "CHF": "Swiss Franc",
        "CNY": "Chinese Yuan",
        "INR": "Indian Rupee",
        "BRL": "Brazilian Real"
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        from_currency = st.selectbox("From:", list(currencies.keys()), format_func=lambda x: f"{x} - {currencies[x]}")
        amount = st.number_input("Amount:", min_value=0.0, value=100.0, step=1.0)
    
    with col2:
        to_currency = st.selectbox("To:", list(currencies.keys()), format_func=lambda x: f"{x} - {currencies[x]}")
    
    # Convert button
    if st.button("Convert Currency"):
        try:
            # Using free currency API (example - you might need an API key for production)
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                rate = data['rates'][to_currency]
                converted_amount = amount * rate
                
                st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
                st.success(f"**{amount} {from_currency} = {converted_amount:.2f} {to_currency}**")
                st.info(f"Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show last updated time
                last_updated = datetime.fromtimestamp(data['time_last_updated'])
                st.caption(f"Rates updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.error("Unable to fetch exchange rates. Please try again later.")
                
        except Exception as e:
            st.error(f"Error converting currency: {str(e)}")
            # Fallback to manual rates (for demo purposes)
            fallback_rates = {
                'USD': {'EUR': 0.85, 'GBP': 0.75, 'JPY': 110.0},
                'EUR': {'USD': 1.18, 'GBP': 0.88, 'JPY': 130.0},
                'GBP': {'USD': 1.33, 'EUR': 1.14, 'JPY': 150.0}
            }
            if from_currency in fallback_rates and to_currency in fallback_rates[from_currency]:
                rate = fallback_rates[from_currency][to_currency]
                converted_amount = amount * rate
                st.warning("Using fallback rates (demo mode)")
                st.success(f"**{amount} {from_currency} = {converted_amount:.2f} {to_currency}**")

# Temperature Conversion
elif conversion_type == "Temperature":
    st.subheader("🌡️ Temperature Converter")
    
    temp_units = ["Celsius", "Fahrenheit", "Kelvin"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        from_temp = st.selectbox("From:", temp_units)
        temp_value = st.number_input("Temperature:", value=0.0, step=0.1)
    
    with col2:
        to_temp = st.selectbox("To:", temp_units)
    
    # Convert instantly as user types
    if temp_value is not None:
        try:
            # Convert to Celsius first
            if from_temp == "Celsius":
                base_temp = temp_value
            elif from_temp == "Fahrenheit":
                base_temp = (temp_value - 32) * 5/9
            else:  # Kelvin
                base_temp = temp_value - 273.15
            
            # Convert from Celsius to target unit
            if to_temp == "Celsius":
                result = base_temp
            elif to_temp == "Fahrenheit":
                result = (base_temp * 9/5) + 32
            else:  # Kelvin
                result = base_temp + 273.15
            
            st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
            st.success(f"**{temp_value:.2f}° {from_temp[0]} = {result:.2f}° {to_temp[0]}**")
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error in temperature conversion: {str(e)}")

# Length Conversion
elif conversion_type == "Length":
    st.subheader("📏 Length Converter")
    
    length_units = {
        "Meters": 1.0,
        "Kilometers": 1000.0,
        "Centimeters": 0.01,
        "Millimeters": 0.001,
        "Miles": 1609.34,
        "Yards": 0.9144,
        "Feet": 0.3048,
        "Inches": 0.0254
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        from_length = st.selectbox("From:", list(length_units.keys()))
        length_value = st.number_input("Length:", min_value=0.0, value=1.0, step=0.1)
    
    with col2:
        to_length = st.selectbox("To:", list(length_units.keys()))
    
    # Convert instantly
    if length_value is not None:
        try:
            # Convert to meters first
            meters_value = length_value * length_units[from_length]
            # Convert to target unit
            result = meters_value / length_units[to_length]
            
            st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
            st.success(f"**{length_value:.4f} {from_length} = {result:.6f} {to_length}**")
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error in length conversion: {str(e)}")

# Weight Conversion
elif conversion_type == "Weight":
    st.subheader("⚖️ Weight Converter")
    
    weight_units = {
        "Grams": 1.0,
        "Kilograms": 1000.0,
        "Milligrams": 0.001,
        "Pounds": 453.592,
        "Ounces": 28.3495,
        "Tons": 1000000.0
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        from_weight = st.selectbox("From:", list(weight_units.keys()))
        weight_value = st.number_input("Weight:", min_value=0.0, value=1.0, step=0.1)
    
    with col2:
        to_weight = st.selectbox("To:", list(weight_units.keys()))
    
    # Convert instantly
    if weight_value is not None:
        try:
            # Convert to grams first
            grams_value = weight_value * weight_units[from_weight]
            # Convert to target unit
            result = grams_value / weight_units[to_weight]
            
            st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
            st.success(f"**{weight_value:.4f} {from_weight} = {result:.6f} {to_weight}**")
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error in weight conversion: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🔁 Universal Unit Converter | Instant conversions for currency, temperature, length, and weight")