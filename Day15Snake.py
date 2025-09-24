import streamlit as st
import random
import time
from enum import Enum

# Page configuration
st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="centered"
)

# Game constants
GRID_SIZE = 12  # Even smaller for better visibility
CELL_SIZE = 30

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# Initialize session state
def init_game():
    st.session_state.snake = [(GRID_SIZE//2, GRID_SIZE//2)]
    st.session_state.direction = Direction.RIGHT
    st.session_state.food = generate_food()
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_running = False
    st.session_state.last_move_time = time.time()

def generate_food():
    """Generate food at a random position not occupied by snake"""
    while True:
        food_pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        if food_pos not in st.session_state.snake:
            return food_pos

def move_snake():
    """Move the snake in the current direction"""
    if st.session_state.game_over or not st.session_state.game_running:
        return
    
    head = st.session_state.snake[0]
    dx, dy = st.session_state.direction.value
    new_head = (head[0] + dx, head[1] + dy)
    
    # Check wall collision
    if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or 
        new_head[1] < 0 or new_head[1] >= GRID_SIZE):
        st.session_state.game_over = True
        return
    
    # Check self collision
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return
    
    st.session_state.snake.insert(0, new_head)
    
    # Check food collision
    if new_head == st.session_state.food:
        st.session_state.score += 10
        st.session_state.food = generate_food()
    else:
        st.session_state.snake.pop()

def render_game_grid():
    """Render the game using Streamlit columns for a proper grid layout"""
    # Create the game grid using columns
    for y in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for x in range(GRID_SIZE):
            with cols[x]:
                if (x, y) == st.session_state.snake[0]:  # Snake head
                    st.markdown("🟢", help="Snake Head")
                elif (x, y) in st.session_state.snake[1:]:  # Snake body
                    st.markdown("🟩", help="Snake Body")
                elif (x, y) == st.session_state.food:  # Food
                    st.markdown("🍎", help="Food")
                else:  # Empty space
                    st.markdown("⬛", help="Empty")

def render_game_simple():
    """Simple text-based rendering with better formatting"""
    game_display = "```\n"
    
    for y in range(GRID_SIZE):
        row = ""
        for x in range(GRID_SIZE):
            if (x, y) == st.session_state.snake[0]:  # Snake head
                row += "🟢 "
            elif (x, y) in st.session_state.snake[1:]:  # Snake body
                row += "🟩 "
            elif (x, y) == st.session_state.food:  # Food
                row += "🍎 "
            else:  # Empty space
                row += "⬛ "
        game_display += row + "\n"
    
    game_display += "```"
    return game_display

def render_game_html():
    """Alternative HTML rendering with better compatibility"""
    # Create a simple table-based grid
    html = """
    <style>
    .game-grid {
        font-family: monospace;
        line-height: 1.2;
        font-size: 14px;
        text-align: center;
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        display: inline-block;
        margin: 10px auto;
    }
    .game-row {
        margin: 0;
        padding: 0;
    }
    </style>
    <div class="game-grid">
    """
    
    for y in range(GRID_SIZE):
        html += '<div class="game-row">'
        for x in range(GRID_SIZE):
            if (x, y) == st.session_state.snake[0]:  # Snake head
                html += "🟢"
            elif (x, y) in st.session_state.snake:  # Snake body
                html += "🟩"
            elif (x, y) == st.session_state.food:  # Food
                html += "🍎"
            else:  # Empty space
                html += "⬛"
        html += '</div>'
    
    html += "</div>"
    return html

# Initialize game if not already done
if 'snake' not in st.session_state:
    init_game()

# Main game interface
st.title("🐍 Snake Game")
st.markdown("---")

# Score and game status
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.metric("Score", st.session_state.score)

with col2:
    if st.session_state.game_over:
        st.error("💀 Game Over!")
    elif st.session_state.game_running:
        st.success("🎮 Playing...")
    else:
        st.info("🎯 Ready to Start!")

with col3:
    st.metric("Length", len(st.session_state.snake))

# Control buttons
st.markdown("### 🎮 Controls")
control_col1, control_col2, control_col3, control_col4, control_col5 = st.columns([1, 1, 1, 1, 1])

with control_col1:
    if st.button("🟢 Start", disabled=st.session_state.game_running):
        st.session_state.game_running = True
        st.session_state.last_move_time = time.time()
        st.rerun()

with control_col2:
    if st.button("⏸️ Pause", disabled=not st.session_state.game_running or st.session_state.game_over):
        st.session_state.game_running = False
        st.rerun()

with control_col3:
    if st.button("🔄 Restart"):
        init_game()
        st.rerun()

# Direction controls
st.markdown("### 🕹️ Direction")
dir_col1, dir_col2, dir_col3, dir_col4, dir_col5 = st.columns([1, 1, 1, 1, 1])

with dir_col2:
    if st.button("⬆️ Up", disabled=st.session_state.game_over):
        if st.session_state.direction != Direction.DOWN:  # Can't reverse
            st.session_state.direction = Direction.UP

with dir_col1:
    if st.button("⬅️ Left", disabled=st.session_state.game_over):
        if st.session_state.direction != Direction.RIGHT:  # Can't reverse
            st.session_state.direction = Direction.LEFT

with dir_col3:
    if st.button("➡️ Right", disabled=st.session_state.game_over):
        if st.session_state.direction != Direction.LEFT:  # Can't reverse
            st.session_state.direction = Direction.RIGHT

with dir_col4:
    if st.button("⬇️ Down", disabled=st.session_state.game_over):
        if st.session_state.direction != Direction.UP:  # Can't reverse
            st.session_state.direction = Direction.DOWN

# Game speed control
speed = st.select_slider(
    "🏃 Game Speed",
    options=[0.5, 0.4, 0.3, 0.2, 0.15, 0.1],
    value=0.3,
    format_func=lambda x: f"{'🐌' if x > 0.3 else '🏃' if x < 0.2 else '🚶'} {x}s"
)

# Render the game grid
st.markdown("### 🎯 Game Board")

# Display current positions for debugging
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"🟢 Snake Head: ({st.session_state.snake[0][0]}, {st.session_state.snake[0][1]})")
with col2:
    st.error(f"🍎 Food: ({st.session_state.food[0]}, {st.session_state.food[1]})")  
with col3:
    st.success(f"🐍 Length: {len(st.session_state.snake)}")

# Game board container
game_container = st.container()

with game_container:
    # Use simple markdown rendering for clear visibility
    st.markdown(render_game_simple(), unsafe_allow_html=False)
    
    # Add visual legend
    st.markdown("**Legend:** 🟢 Head | 🟩 Body | 🍎 Food | ⬛ Empty")

# Game loop for automatic movement
if st.session_state.game_running and not st.session_state.game_over:
    current_time = time.time()
    
    if current_time - st.session_state.last_move_time >= speed:
        move_snake()
        st.session_state.last_move_time = current_time
        st.rerun()
    else:
        # Small delay before next check
        time.sleep(0.05)
        st.rerun()

# Game statistics and high score
if st.session_state.score > 0 or st.session_state.game_over:
    st.markdown("---")
    st.markdown("### 📊 Game Stats")
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.metric("Current Score", st.session_state.score)
    
    with stats_col2:
        # Calculate food eaten
        food_eaten = (len(st.session_state.snake) - 1)
        st.metric("Food Eaten", food_eaten)
    
    with stats_col3:
        # Calculate efficiency (score per length)
        if len(st.session_state.snake) > 1:
            efficiency = round(st.session_state.score / len(st.session_state.snake), 1)
            st.metric("Efficiency", efficiency)

# Instructions
with st.expander("📖 How to Play"):
    st.markdown("""
    **Objective:** Control the snake to eat food and grow as long as possible!
    
    **Controls:**
    - Use the direction buttons to change the snake's direction
    - The snake moves automatically in the chosen direction
    - You cannot reverse directly into the snake's body
    
    **Rules:**
    - 🍎 Eat food to grow and increase your score (+10 points)
    - 🐍 The snake grows longer with each food consumed
    - 💀 Game ends if you hit the walls or your own body
    - 🏃 Adjust game speed with the speed slider
    
    **Tips:**
    - Plan your moves ahead to avoid getting trapped
    - Use the pause button if you need a moment to think
    - Try different speeds to find your optimal challenge level
    """)

# Game over message with restart prompt
if st.session_state.game_over:
    st.markdown("---")
    st.error("🎮 Game Over! Your snake crashed!")
    
    if st.session_state.score > 0:
        st.balloons()  # Celebrate if they scored!
        st.success(f"🎉 Final Score: {st.session_state.score} points!")
        st.info(f"🐍 Snake Length: {len(st.session_state.snake)} segments")
    
    if st.button("🚀 Play Again", type="primary"):
        init_game()
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 12px;'>"
    "🐍 Snake Game built with Streamlit • Use direction buttons to control the snake!"
    "</div>", 
    unsafe_allow_html=True
)