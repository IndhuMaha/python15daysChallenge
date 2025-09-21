import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Page config
st.set_page_config(
    page_title="🍽️ Gourmet Bistro - Order & Billing",
    page_icon="🍽️",
    layout="centered"
)

# Light Yellow Background + Clean UI Styling
st.markdown("""
    <style>
    .main {
        background-color: #fffbeb;
        padding: 2rem 0;
    }

    /* Header */
    .app-header {
        text-align: center;
        padding: 2rem 1rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid #f0e6d2;
    }
    .app-header h1 {
        margin: 0;
        font-size: 2.5rem;
        color: #8b6b0f;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .app-header p {
        color: #a0864a;
        margin-top: 0.5rem;
    }

    /* Menu Title */
    .menu-title {
        color: #8b6b0f;
        border-bottom: 2px solid #f9d976;
        padding: 1rem 0 0.5rem;
        margin: 2rem 0 1rem;
        font-size: 1.5rem;
        font-weight: 700;
    }

    /* Menu Item Card */
    .menu-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        margin-bottom: 1rem;
        background: #fdf6ec;
        border-radius: 12px;
        border: 1px solid #fbeec1;
        transition: all 0.3s ease;
    }
    .menu-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background: #fdf0d5;
    }
    .item-info {
        flex: 1;
    }
    .item-name {
        font-weight: 600;
        color: #5c4a1a;
        font-size: 1.1rem;
    }
    .item-desc {
        font-size: 0.9rem;
        color: #8c7b5d;
        margin-top: 0.2rem;
    }
    .item-price {
        font-weight: 700;
        color: #d4a33f;
        font-size: 1.2rem;
        min-width: 80px;
        text-align: right;
    }

    /* Quantity Selector */
    div.stNumberInput > div > div {
        border-radius: 10px !important;
        border: 1px solid #f0e6d2 !important;
    }

    /* Bill Summary */
    .bill-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        border: 1px solid #f0e6d2;
        margin: 2rem auto;
        max-width: 500px;
    }
    .bill-title {
        text-align: center;
        color: #8b6b0f;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    .bill-row {
        display: flex;
        justify-content: space-between;
        padding: 0.7rem 0;
        font-size: 1.1rem;
        border-bottom: 1px dashed #f5e9c9;
        color: #5c4a1a;
    }
    .bill-total {
        font-weight: 700;
        font-size: 1.3rem;
        color: #8b6b0f;
        border: none;
        margin-top: 1rem;
        padding-top: 1rem;
    }
    .bill-amount {
        font-weight: 600;
        color: #d4a33f;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 12px !important;
        height: 3.5rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin: 0.5rem 0 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.15) !important;
    }
    .btn-csv {
        background: linear-gradient(135deg, #28a745, #20c997) !important;
        color: white !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 1rem 1rem;
        color: #a0864a;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sample Menu Data
MENU = {
    "Appetizers": [
        {"name": "Garlic Bread", "price": 8.99, "desc": "Toasted with herb butter"},
        {"name": "Caesar Salad", "price": 10.99, "desc": "Romaine, parmesan, croutons"},
        {"name": "Mozzarella Sticks", "price": 9.99, "desc": "Crispy fried with marinara"},
    ],
    "Main Courses": [
        {"name": "Grilled Salmon", "price": 24.99, "desc": "With lemon herb butter"},
        {"name": "Ribeye Steak", "price": 32.99, "desc": "12oz, served with mashed potatoes"},
        {"name": "Chicken Alfredo", "price": 18.99, "desc": "Fettuccine in creamy parmesan sauce"},
        {"name": "Veggie Burger", "price": 15.99, "desc": "House-made patty with avocado"},
    ],
    "Desserts": [
        {"name": "Chocolate Lava Cake", "price": 9.99, "desc": "Warm center with vanilla ice cream"},
        {"name": "Cheesecake", "price": 8.99, "desc": "New York style with berry compote"},
        {"name": "Tiramisu", "price": 10.99, "desc": "Classic Italian coffee dessert"},
    ],
    "Beverages": [
        {"name": "Fresh Lemonade", "price": 4.99, "desc": "Homemade with mint"},
        {"name": "Iced Tea", "price": 3.99, "desc": "Sweet or unsweetened"},
        {"name": "Cappuccino", "price": 5.99, "desc": "Espresso with steamed milk"},
    ]
}

TAX_RATE = 0.08  # 8% tax

# Initialize session state
if 'order' not in st.session_state:
    st.session_state.order = {}

def add_to_order(item_name, qty, price):
    if qty > 0:
        st.session_state.order[item_name] = {"quantity": qty, "price": price}
    elif item_name in st.session_state.order:
        del st.session_state.order[item_name]

def calculate_bill():
    subtotal = sum(item["quantity"] * item["price"] for item in st.session_state.order.values())
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    return subtotal, tax, total

def generate_csv():
    if not st.session_state.order:
        return None
    
    data = []
    for name, details in st.session_state.order.items():
        data.append({
            "Item": name,
            "Quantity": details["quantity"],
            "Price": f"${details['price']:.2f}",
            "Total": f"${details['quantity'] * details['price']:.2f}"
        })
    
    subtotal, tax, total = calculate_bill()
    data.append({"Item": "SUBTOTAL", "Quantity": "", "Price": "", "Total": f"${subtotal:.2f}"})
    data.append({"Item": "TAX (8%)", "Quantity": "", "Price": "", "Total": f"${tax:.2f}"})
    data.append({"Item": "TOTAL", "Quantity": "", "Price": "", "Total": f"${total:.2f}"})
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

# --- UI ---

st.markdown('<div class="app-header"><h1>🍽️ Gourmet Bistro</h1><p>Order Your Favorite Dishes</p></div>', unsafe_allow_html=True)

# Display Menu — FIXED: No more empty divs!
for category, items in MENU.items():
    st.markdown(f'<div class="menu-title">{category}</div>', unsafe_allow_html=True)
    
    for item in items:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f'''
                <div class="menu-item">
                    <div class="item-info">
                        <div class="item-name">{item["name"]}</div>
                        <div class="item-desc">{item["desc"]}</div>
                    </div>
                    <div class="item-price">${item["price"]:.2f}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            qty = st.number_input(
                f"Qty_{item['name']}",
                min_value=0,
                max_value=10,
                value=st.session_state.order.get(item['name'], {}).get('quantity', 0),
                key=f"qty_{item['name']}",
                label_visibility="collapsed"
            )
            add_to_order(item['name'], qty, item['price'])

# Bill Summary
subtotal, tax, total = calculate_bill()

st.markdown('<div class="bill-container">', unsafe_allow_html=True)
st.markdown('<div class="bill-title">🧾 BILL SUMMARY</div>', unsafe_allow_html=True)

st.markdown(f'<div class="bill-row"><div>Subtotal</div><div class="bill-amount">${subtotal:.2f}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="bill-row"><div>Tax (8%)</div><div class="bill-amount">${tax:.2f}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="bill-row bill-total"><div>TOTAL</div><div class="bill-amount">${total:.2f}</div></div>', unsafe_allow_html=True)

# Download CSV Button Only
csv_data = generate_csv()
if csv_data:
    b64 = base64.b64encode(csv_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="invoice_{datetime.now().strftime("%Y%m%d")}.csv"><button class="btn-csv">💾 Download CSV Invoice</button></a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    st.button("💾 Download CSV Invoice (No Items)", disabled=True, key="csv_disabled")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>✨ Thank you for choosing Gourmet Bistro! | All prices in USD ✨</p>
        <p>Need help? Call (555) 123-4567 or email order@gourmetbistro.com</p>
    </div>
""", unsafe_allow_html=True)