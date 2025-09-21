import streamlit as st
import random
import time

# Page config with emoji favicon
st.set_page_config(
    page_title="✨ Ultimate Tic-Tac-Toe",
    page_icon="🎮",
    layout="centered"
)

# Advanced Styling — Background removed, clean UI preserved
st.markdown("""
    <style>
    /* Clean background */
    .main {
        background-color: #f8f9fa;
        min-height: 100vh;
        padding: 2rem 0;
    }

    /* Header */
    .game-header {
        text-align: center;
        padding: 2rem 1rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 2rem;
        color: #212529;
    }

    .game-header h1 {
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: 1.5px;
        background: linear-gradient(to right, #d63384, #0d6efd, #198754);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Game Board Container */
    .board-container {
        display: flex;
        justify-content: center;
        padding: 1.5rem;
        background: white;
        border-radius: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid #dee2e6;
        margin: 1rem auto;
        max-width: 420px;
    }

    /* Game Buttons */
    .stButton>button {
        font-size: 2.5rem;
        font-weight: bold;
        height: 4.5em;
        width: 4.5em;
        border-radius: 15px;
        margin: 0.3em;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #e9ecef;
        background: white;
        color: #495057;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        background: #f8f9fa;
    }

    .stButton>button:active {
        transform: translateY(0px) scale(0.98);
    }

    /* Player X Button */
    .x-button {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52) !important;
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4) !important;
    }

    /* Player O Button */
    .o-button {
        background: linear-gradient(135deg, #4ecdc4, #44a08d) !important;
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4) !important;
    }

    /* Winning Button Animation */
    .win-button {
        background: linear-gradient(135deg, #ffd93d, #ff9a00) !important;
        color: #5c3d00 !important;
        text-shadow: 1px 1px 3px rgba(255,255,255,0.8) !important;
        box-shadow: 0 0 30px rgba(255, 217, 61, 0.8) !important;
        animation: glowing 1.5s infinite alternate, float 2s ease-in-out infinite;
        transform: scale(1.05) !important;
        z-index: 10;
        border: none !important;
    }

    @keyframes glowing {
        from { box-shadow: 0 0 10px rgba(255, 217, 61, 0.5); }
        to { box-shadow: 0 0 30px rgba(255, 217, 61, 1); }
    }

    @keyframes float {
        0% { transform: translateY(0px) scale(1.05); }
        50% { transform: translateY(-10px) scale(1.1); }
        100% { transform: translateY(0px) scale(1.05); }
    }

    /* Status Box */
    .status-box {
        text-align: center;
        padding: 1.2rem;
        border-radius: 20px;
        margin: 1.5rem auto;
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        max-width: 500px;
        background: white;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e9ecef;
        color: #212529;
        transition: all 0.3s ease;
    }

    .status-x {
        border-left: 5px solid #ff6b6b;
        background: #fff5f5;
    }
    .status-o {
        border-left: 5px solid #4ecdc4;
        background: #f0fdfc;
    }
    .status-win {
        border-left: 5px solid #ffd93d;
        background: #fffbeb;
        color: #854d00;
    }

    /* Control Buttons */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0d6efd, #0b5ed7) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(13, 110, 253, 0.4) !important;
    }

    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #6c757d, #495057) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(108, 117, 125, 0.4) !important;
    }

    /* Scoreboard */
    .score-container {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 2rem auto;
        max-width: 500px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid #dee2e6;
    }

    .score-title {
        color: #212529;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }

    .score-item {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .score-x { border-left: 5px solid #ff6b6b; }
    .score-o { border-left: 5px solid #4ecdc4; }
    .score-tie { border-left: 5px solid #ffd93d; }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 1rem 1rem;
        color: #6c757d;
        font-size: 0.9rem;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .stButton>button {
            height: 3.5em;
            width: 3.5em;
            font-size: 2rem;
        }
        .game-header h1 {
            font-size: 2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'winning_line' not in st.session_state:
    st.session_state.winning_line = []
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = '2player'
if 'scores' not in st.session_state:
    st.session_state.scores = {'X': 0, 'O': 0, 'Ties': 0}

def check_winner(board):
    """Check for winner and return winning line if exists"""
    lines = [
        [(0,0), (0,1), (0,2)],  # Rows
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        [(0,0), (1,0), (2,0)],  # Columns
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)],  # Diagonals
        [(0,2), (1,1), (2,0)]
    ]
    
    for line in lines:
        symbols = [board[i][j] for i, j in line]
        if symbols[0] != '' and symbols[0] == symbols[1] == symbols[2]:
            return symbols[0], line
    
    if all(board[i][j] != '' for i in range(3) for j in range(3)):
        return 'Tie', []
    
    return None, []

def reset_game():
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = []

def make_computer_move():
    # Try to win
    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == '':
                st.session_state.board[i][j] = 'O'
                winner, _ = check_winner(st.session_state.board)
                if winner == 'O':
                    return
                st.session_state.board[i][j] = ''
    
    # Block player
    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == '':
                st.session_state.board[i][j] = 'X'
                winner, _ = check_winner(st.session_state.board)
                if winner == 'X':
                    st.session_state.board[i][j] = 'O'
                    return
                st.session_state.board[i][j] = ''
    
    # Random move
    empty_cells = [(i, j) for i in range(3) for j in range(3) if st.session_state.board[i][j] == '']
    if empty_cells:
        row, col = random.choice(empty_cells)
        st.session_state.board[row][col] = 'O'

def handle_click(row, col):
    if st.session_state.board[row][col] == '' and not st.session_state.game_over:
        st.session_state.board[row][col] = st.session_state.current_player
        
        winner, winning_line = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
            st.session_state.winning_line = winning_line
            if winner != 'Tie':
                st.session_state.scores[winner] += 1
            else:
                st.session_state.scores['Ties'] += 1
        else:
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
            
            if st.session_state.game_mode == 'vs_computer' and st.session_state.current_player == 'O':
                time.sleep(0.5)
                make_computer_move()
                winner, winning_line = check_winner(st.session_state.board)
                if winner:
                    st.session_state.game_over = True
                    st.session_state.winner = winner
                    st.session_state.winning_line = winning_line
                    if winner != 'Tie':
                        st.session_state.scores[winner] += 1
                    else:
                        st.session_state.scores['Ties'] += 1

# --- UI ---

st.markdown('<div class="game-header"><h1>✨ ULTIMATE TIC-TAC-TOE</h1></div>', unsafe_allow_html=True)

# Game mode buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("👥 2 PLAYER MODE", key="mode1", use_container_width=True, type="primary"):
        st.session_state.game_mode = '2player'
        reset_game()
with col2:
    if st.button("🤖 VS COMPUTER", key="mode2", use_container_width=True, type="primary"):
        st.session_state.game_mode = 'vs_computer'
        reset_game()
with col3:
    if st.button("🔄 NEW GAME", key="reset_btn", use_container_width=True, type="secondary"):
        reset_game()

# Status box
if st.session_state.game_over:
    if st.session_state.winner == 'Tie':
        status_text = "🤝 GAME OVER: IT'S A TIE!"
        status_class = "status-win"
    else:
        status_text = f"🎉 GAME OVER: PLAYER {st.session_state.winner} WINS!"
        status_class = "status-win"
elif st.session_state.game_mode == 'vs_computer':
    if st.session_state.current_player == 'X':
        status_text = "✏️ YOUR TURN (X)"
        status_class = "status-x"
    else:
        status_text = "🤖 COMPUTER THINKING... (O)"
        status_class = "status-o"
else:
    status_text = f"🎮 PLAYER {st.session_state.current_player}'S TURN"
    status_class = "status-x" if st.session_state.current_player == 'X' else "status-o"

st.markdown(f'<div class="status-box {status_class}">{status_text}</div>', unsafe_allow_html=True)

# Game board
st.markdown('<div class="board-container">', unsafe_allow_html=True)
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        cell_value = st.session_state.board[i][j]
        button_key = f"button_{i}_{j}"
        
        button_class = ""
        if cell_value == 'X':
            button_class = "x-button"
        elif cell_value == 'O':
            button_class = "o-button"
        if (i, j) in st.session_state.winning_line:
            button_class = "win-button"
        
        if cols[j].button(
            "❌" if cell_value == 'X' else "⭕" if cell_value == 'O' else "",
            key=button_key,
            on_click=handle_click,
            args=(i, j),
            use_container_width=True
        ):
            pass
st.markdown('</div>', unsafe_allow_html=True)

# Scoreboard
st.markdown('<div class="score-container">', unsafe_allow_html=True)
st.markdown('<div class="score-title">🏆 SCOREBOARD</div>', unsafe_allow_html=True)
score_cols = st.columns(3)
with score_cols[0]:
    st.markdown(f'<div class="score-item score-x"><h3>PLAYER X</h3><h2 style="color: #ff6b6b;">{st.session_state.scores["X"]}</h2></div>', unsafe_allow_html=True)
with score_cols[1]:
    st.markdown(f'<div class="score-item score-tie"><h3>TIES</h3><h2 style="color: #ffd93d;">{st.session_state.scores["Ties"]}</h2></div>', unsafe_allow_html=True)
with score_cols[2]:
    st.markdown(f'<div class="score-item score-o"><h3>PLAYER O</h3><h2 style="color: #4ecdc4;">{st.session_state.scores["O"]}</h2></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Instructions
with st.expander("🎮 HOW TO PLAY", expanded=False):
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 15px; border: 1px solid #e9ecef;">
    <h4 style="color: #212529; margin-bottom: 1rem;">🌟 Game Rules</h4>
    <ul style="color: #495057; padding-left: 1.5rem; line-height: 1.8;">
        <li>Two players take turns marking X and O on a 3×3 grid</li>
        <li>The first player to get 3 of their marks in a row wins!</li>
        <li>In "Vs Computer" mode, you play as X, computer plays as O</li>
        <li>If all squares are filled with no winner → it’s a tie</li>
    </ul>
    <h4 style="color: #212529; margin-top: 1.5rem; margin-bottom: 1rem;">🎨 Visual Guide</h4>
    <ul style="color: #495057; padding-left: 1.5rem; line-height: 1.8;">
        <li><strong style="color: #ff6b6b;">❌ Player X</strong> — Red gradient buttons</li>
        <li><strong style="color: #4ecdc4;">⭕ Player O</strong> — Teal gradient buttons</li>
        <li><strong style="color: #ffd93d;">✨ Winning Line</strong> — Golden glowing animation</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>✨ Created with Streamlit &amp; Love | Click, Play, Enjoy! ✨</p>
        <p>💡 Pro Tip: Computer AI tries to block your winning moves!</p>
    </div>
""", unsafe_allow_html=True)