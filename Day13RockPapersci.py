import streamlit as st
import random

# --- Custom pastel styling ---
st.markdown("""
    <style>
        body {
            background-color: #fdf6f0;
        }
        .main {
            background-color: #fdf6f0;
        }
        h1, h2, h3 {
            color: #6c5b7b;
        }
        .stButton>button {
            background-color: #f7cac9;
            color: #355c7d;
            border-radius: 10px;
            padding: 0.5em 1em;
            font-weight: bold;
        }
        .score-box {
            background-color: #e0f7fa;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("🎮 Rock Paper Scissors")
st.subheader("Player: You vs Computer 🤖")

# --- Session State for Score ---
if "score" not in st.session_state:
    st.session_state.score = {"Wins": 0, "Losses": 0, "Ties": 0}

# --- Game Logic ---
choices = {
    "🪨 Rock": "Rock",
    "📄 Paper": "Paper",
    "✂️ Scissors": "Scissors"
}

user_choice_label = st.radio("Choose your move:", list(choices.keys()), horizontal=True)
user_choice = choices[user_choice_label]
computer_choice = random.choice(list(choices.values()))

result = ""
if st.button("Play"):
    if user_choice == computer_choice:
        result = "It's a Tie! 🤝"
        st.session_state.score["Ties"] += 1
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = "You Win! 🎉"
        st.session_state.score["Wins"] += 1
    else:
        result = "You Lose! 😢"
        st.session_state.score["Losses"] += 1

    st.markdown(f"### You chose: `{user_choice}`")
    st.markdown(f"### Computer chose: `{computer_choice}`")
    st.markdown(f"## {result}")

# --- Scoreboard ---
st.markdown("<div class='score-box'>", unsafe_allow_html=True)
st.markdown(f"**🏆 Wins:** {st.session_state.score['Wins']} &nbsp;&nbsp; | &nbsp;&nbsp; **💔 Losses:** {st.session_state.score['Losses']} &nbsp;&nbsp; | &nbsp;&nbsp; **🤝 Ties:** {st.session_state.score['Ties']}")
st.markdown("</div>", unsafe_allow_html=True)

# --- Game Rules ---
with st.expander("📜 Game Rules"):
    st.markdown("""
    - 🪨 **Rock beats Scissors**
    - ✂️ **Scissors beats Paper**
    - 📄 **Paper beats Rock**
    - If both choose the same, it's a **Tie**
    - Play as many rounds as you like!
    """)

# --- Reset Button ---
if st.button("🔄 Reset Score"):
    st.session_state.score = {"Wins": 0, "Losses": 0, "Ties": 0}
    st.success("Scoreboard reset!")