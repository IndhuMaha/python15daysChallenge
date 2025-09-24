import streamlit as st
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Stopwatch App",
    page_icon="⏱️",
    layout="centered"
)

# Initialize session state variables
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'lap_times' not in st.session_state:
    st.session_state.lap_times = []
if 'lap_counter' not in st.session_state:
    st.session_state.lap_counter = 0

# Helper function to format time
def format_time(seconds):
    """Format time in MM:SS.ms format"""
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes:02d}:{secs:06.3f}"

# Helper function to get current elapsed time
def get_current_elapsed():
    """Get current elapsed time"""
    if st.session_state.is_running and st.session_state.start_time:
        return st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
    return st.session_state.elapsed_time

# Main app layout
st.title("⏱️ Stopwatch App")
st.markdown("---")

# Create columns for layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Display the main timer
    current_time = get_current_elapsed()
    st.markdown(
        f"""
        <div style="
            font-size: 48px; 
            font-weight: bold; 
            text-align: center; 
            font-family: 'Courier New', monospace;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 20px 0;
        ">
            {format_time(current_time)}
        </div>
        """, 
        unsafe_allow_html=True
    )

# Control buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("▶️ Start", disabled=st.session_state.is_running, use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.is_running = True
        st.rerun()

with col2:
    if st.button("⏸️ Stop", disabled=not st.session_state.is_running, use_container_width=True):
        if st.session_state.is_running:
            st.session_state.elapsed_time += time.time() - st.session_state.start_time
            st.session_state.is_running = False
            st.session_state.start_time = None
        st.rerun()

with col3:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.start_time = None
        st.session_state.elapsed_time = 0
        st.session_state.is_running = False
        st.session_state.lap_times = []
        st.session_state.lap_counter = 0
        st.rerun()

with col4:
    if st.button("🏁 Lap", disabled=not st.session_state.is_running, use_container_width=True):
        if st.session_state.is_running:
            lap_time = get_current_elapsed()
            st.session_state.lap_counter += 1
            st.session_state.lap_times.append({
                'lap': st.session_state.lap_counter,
                'time': lap_time,
                'split': lap_time - (st.session_state.lap_times[-1]['time'] if st.session_state.lap_times else 0)
            })
        st.rerun()

# Auto-refresh when running - using a placeholder for real-time updates
if st.session_state.is_running:
    # Create a placeholder for auto-refresh
    placeholder = st.empty()
    # Small delay and rerun for real-time effect
    time.sleep(0.01)
    st.rerun()

# Lap times section
if st.session_state.lap_times:
    st.markdown("---")
    st.subheader("🏁 Lap Times")
    
    # Create a more reliable table display
    st.write("**Recent Laps:**")
    
    # Display lap times in a cleaner format
    for i, lap in enumerate(reversed(st.session_state.lap_times)):
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.write(f"**Lap {lap['lap']}**")
        with col2:
            st.write(f"Total: {format_time(lap['time'])}")
        with col3:
            st.write(f"Split: {format_time(lap['split'])}")
        
        if i < len(st.session_state.lap_times) - 1:  # Add separator except for last item
            st.write("---")

# Statistics section - make sure it shows up
if st.session_state.lap_times and len(st.session_state.lap_times) > 0:
    st.markdown("---")
    st.subheader("📊 Lap Statistics")
    
    # Calculate statistics from split times
    split_times = [lap['split'] for lap in st.session_state.lap_times]
    
    if len(split_times) > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            best_lap = min(split_times)
            st.metric("🏆 Best Lap", format_time(best_lap))
        
        with col2:
            worst_lap = max(split_times)
            st.metric("🐌 Worst Lap", format_time(worst_lap))
        
        with col3:
            avg_split = sum(split_times) / len(split_times)
            st.metric("📊 Average", format_time(avg_split))
            
        # Additional stats
        st.markdown("**Summary:**")
        st.write(f"• Total laps recorded: {len(st.session_state.lap_times)}")
        st.write(f"• Current elapsed time: {format_time(get_current_elapsed())}")
        
        # Show improvement trend
        if len(split_times) >= 2:
            last_lap = split_times[-1]
            second_last_lap = split_times[-2]
            improvement = second_last_lap - last_lap
            
            if improvement > 0:
                st.success(f"🎯 Last lap was {format_time(improvement)} faster!")
            elif improvement < 0:
                st.warning(f"📈 Last lap was {format_time(abs(improvement))} slower")
            else:
                st.info("🎯 Last lap same as previous")

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    - **Start**: Begin the stopwatch
    - **Stop**: Pause the stopwatch (can be resumed)
    - **Reset**: Clear all times and reset to 00:00.000
    - **Lap**: Record a lap time while the stopwatch is running
    
    The timer displays in MM:SS.mmm format (minutes:seconds.milliseconds).
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 12px;'>"
    "Built with Streamlit ❤️"
    "</div>", 
    unsafe_allow_html=True
)