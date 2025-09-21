import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="School Annual Day Registration",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for light green theme and professional UI
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background-color: #e8f5e9;
        color: #2e7d32;
    }
    
    /* Header styling */
    header {
        background-color: #4caf50 !important;
        color: white;
    }
    
    /* Form styling */
    .stForm {
        background-color: #c8e6c9;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Input fields */
    .stTextInput, .stSelectbox, .stNumberInput {
        background-color: white !important;
        border-radius: 5px;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    .stButton>button:hover {
        background-color: #388e3c;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Remove empty divs */
    div:empty {
        display: none;
    }
    
    /* Responsive columns */
    [data-testid="column"] {
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'registrations' not in st.session_state:
    st.session_state.registrations = pd.DataFrame(columns=[
        'Timestamp', 'Name', 'Event', 'Class', 'Class Teacher'
    ])

# Event options
EVENTS = ['Drawing', 'Dance', 'Singing', 'Karate', 'Acting']
TEACHERS = ['Mr. Johnson', 'Ms. Roberts', 'Dr. Smith', 'Mrs. Williams', 'Mr. Brown']

# App header
st.title("🎓 School Annual Day Registration")
st.markdown("---")

# Registration form
with st.form("registration_form", clear_on_submit=True):
    st.subheader("Register for Events")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Student Name", placeholder="Enter full name")
        event = st.selectbox("Choose Event", EVENTS)
        submit = st.form_submit_button("Register")
    
    with col2:
        student_class = st.text_input("Class", placeholder="e.g., Grade 5")
        teacher = st.selectbox("Class Teacher", TEACHERS)
    
    # Form submission
    if submit:
        if name and student_class:
            new_registration = pd.DataFrame({
                'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                'Name': [name],
                'Event': [event],
                'Class': [student_class],
                'Class Teacher': [teacher]
            })
            
            # Concatenate and ensure proper index
            st.session_state.registrations = pd.concat([
                st.session_state.registrations, 
                new_registration
            ], ignore_index=True)
            
            st.success(f"✅ Registered for {event} successfully!")
        else:
            st.error("Please fill in all required fields")

# Live registration counts
st.subheader("Live Registration Counts")
event_counts = st.session_state.registrations['Event'].value_counts()

cols = st.columns(len(EVENTS))
for i, event in enumerate(EVENTS):
    with cols[i]:
        count = event_counts.get(event, 0)
        st.metric(label=event, value=count)

# Export to CSV
if not st.session_state.registrations.empty:
    csv = st.session_state.registrations.to_csv(index=False)
    st.download_button(
        label="📥 Download Registration Data",
        data=csv,
        file_name="annual_day_registrations.csv",
        mime="text/csv"
    )

# Coordinator Contact Information
st.markdown("---")
st.markdown("<h3 style='color: #4caf50;'>Contact Information</h3>", unsafe_allow_html=True)
st.markdown("""
<div style='background-color: #f1f8e9; padding: 15px; border-radius: 10px; border-left: 5px solid #4caf50;'>
    <strong>Annual Day Coordinator:</strong><br>
    <em>Ms. Sarah Thompson</em><br>
    <strong>Email:</strong> sarah.thompson@school.edu<br>
    <strong>Phone:</strong> +1 (555) 123-4567<br>
    <strong>Office:</strong> Administration Building, Room 102<br>
    <strong>Availability:</strong> Monday-Friday, 9:00 AM - 5:00 PM
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("📅 School Annual Day Event Registration System | Developed with Streamlit")