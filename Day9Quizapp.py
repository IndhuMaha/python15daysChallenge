import streamlit as st
import time
from typing import Dict, List

# Page configuration
st.set_page_config(
    page_title="🧠 Interactive Quiz Game",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-family: 'Arial', sans-serif !important;
    }
    
    .main-header {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: fadeIn 1s ease-in;
    }
    
    .quiz-container {
        background: rgba(255, 255, 255, 0.98);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        color: #2c3e50 !important;
    }
    
    .question-header {
        color: #2c3e50;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(45deg, #f39c12, #e74c3c);
        color: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .progress-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .score-display {
        font-size: 1.2rem;
        font-weight: bold;
        color: #27ae60;
        text-align: center;
        margin: 1rem 0;
    }
    
    .final-score {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(45deg, #2ecc71, #27ae60);
        color: white;
        border-radius: 20px;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: bounce 1s ease-in-out;
    }
    
    .restart-button {
        text-align: center;
        margin: 2rem 0;
    }
    
    .question-counter {
        font-size: 1.1rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .question-text {
        color: #2c3e50 !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 !important;
        padding: 1rem !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        line-height: 1.6 !important;
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        margin: 0.5rem 0 !important;
        border: 2px solid rgba(52, 152, 219, 0.3) !important;
    }
    
    .stRadio label {
        color: #2c3e50 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #3498db, #2980b9) !important;
        color: white !important;
        border: none !important;
        padding: 1.2rem 3rem !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        font-size: 1.3rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        width: 100% !important;
        min-height: 60px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    }
    
    .correct-answer {
        background: linear-gradient(45deg, #2ecc71, #27ae60) !important;
        color: white !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        text-align: center !important;
        margin: 1rem 0 !important;
        font-weight: bold !important;
    }
    
    .incorrect-answer {
        background: linear-gradient(45deg, #e74c3c, #c0392b) !important;
        color: white !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        text-align: center !important;
        margin: 1rem 0 !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Quiz questions data
QUIZ_DATA: List[Dict] = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": 2,
        "explanation": "Paris is the capital and most populous city of France."
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": 1,
        "explanation": "Mars is called the Red Planet due to iron oxide (rust) on its surface."
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "correct": 1,
        "explanation": "The Blue Whale is the largest mammal and largest animal ever known to have lived on Earth."
    },
    {
        "question": "In which year did World War II end?",
        "options": ["1944", "1945", "1946", "1947"],
        "correct": 1,
        "explanation": "World War II ended in 1945 with the surrender of Japan in September."
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "correct": 2,
        "explanation": "Au comes from the Latin word 'aurum' meaning gold."
    },
    {
        "question": "Which programming language is known for its use in data science?",
        "options": ["JavaScript", "Python", "C++", "Ruby"],
        "correct": 1,
        "explanation": "Python is widely used in data science due to its extensive libraries and ease of use."
    },
    {
        "question": "What is the smallest unit of matter?",
        "options": ["Molecule", "Atom", "Electron", "Proton"],
        "correct": 1,
        "explanation": "An atom is the smallest unit of ordinary matter that forms a chemical element."
    },
    {
        "question": "Which ocean is the largest?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "correct": 3,
        "explanation": "The Pacific Ocean is the largest and deepest ocean on Earth."
    },
    {
        "question": "What does 'AI' stand for?",
        "options": ["Automated Intelligence", "Artificial Intelligence", "Advanced Integration", "Algorithmic Interface"],
        "correct": 1,
        "explanation": "AI stands for Artificial Intelligence, the simulation of human intelligence in machines."
    },
    {
        "question": "Which gas makes up most of Earth's atmosphere?",
        "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Argon"],
        "correct": 2,
        "explanation": "Nitrogen makes up approximately 78% of Earth's atmosphere."
    }
]

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False

def reset_quiz():
    """Reset all quiz-related session state"""
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_completed = False
    st.session_state.user_answers = []
    st.session_state.show_explanation = False

def display_progress():
    """Display quiz progress"""
    progress = (st.session_state.current_question / len(QUIZ_DATA)) * 100
    st.markdown(f"""
    <div class="progress-container">
        <h4>Quiz Progress: {st.session_state.current_question}/{len(QUIZ_DATA)} Questions</h4>
        <div style="background: #ecf0f1; border-radius: 10px; overflow: hidden;">
            <div style="background: linear-gradient(45deg, #3498db, #2980b9); height: 20px; width: {progress}%; border-radius: 10px; transition: width 0.5s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_current_score():
    """Display current score"""
    st.markdown(f"""
    <div class="score-display">
        Current Score: {st.session_state.score} / {st.session_state.current_question}
    </div>
    """, unsafe_allow_html=True)

def submit_answer(selected_option_index: int):
    """Process the submitted answer"""
    current_q = QUIZ_DATA[st.session_state.current_question]
    is_correct = selected_option_index == current_q["correct"]
    
    # Store user's answer
    st.session_state.user_answers.append({
        'question_index': st.session_state.current_question,
        'selected': selected_option_index,
        'correct': is_correct
    })
    
    # Update score if correct
    if is_correct:
        st.session_state.score += 1
    
    # Show explanation
    st.session_state.show_explanation = True

def next_question():
    """Move to next question or complete quiz"""
    st.session_state.current_question += 1
    st.session_state.show_explanation = False
    
    if st.session_state.current_question >= len(QUIZ_DATA):
        st.session_state.quiz_completed = True

def display_final_results():
    """Display final quiz results"""
    percentage = (st.session_state.score / len(QUIZ_DATA)) * 100
    
    # Performance message
    if percentage >= 90:
        performance = "🏆 Outstanding! You're a quiz master!"
        color = "#2ecc71"
    elif percentage >= 70:
        performance = "🎉 Great job! Well done!"
        color = "#3498db"
    elif percentage >= 50:
        performance = "👍 Good effort! Keep learning!"
        color = "#f39c12"
    else:
        performance = "📚 Keep studying and try again!"
        color = "#e74c3c"
    
    st.markdown(f"""
    <div class="final-score" style="background: linear-gradient(45deg, {color}, {color}dd);">
        <h2>{performance}</h2>
        <h1>Final Score: {st.session_state.score} / {len(QUIZ_DATA)}</h1>
        <h3>Percentage: {percentage:.1f}%</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed results
    st.markdown("### 📊 Detailed Results")
    
    for i, answer in enumerate(st.session_state.user_answers):
        question = QUIZ_DATA[answer['question_index']]
        status = "✅ Correct" if answer['correct'] else "❌ Incorrect"
        
        with st.expander(f"Question {i+1}: {status}"):
            st.write(f"**Question:** {question['question']}")
            st.write(f"**Your Answer:** {question['options'][answer['selected']]}")
            st.write(f"**Correct Answer:** {question['options'][question['correct']]}")
            st.write(f"**Explanation:** {question['explanation']}")

def main():
    """Main application function"""
    initialize_session_state()
    
    # App header
    st.markdown('<h1 class="main-header">🧠 Interactive Quiz Game</h1>', unsafe_allow_html=True)
    
    if not st.session_state.quiz_completed:
        # Display progress and score
        display_progress()
        if st.session_state.current_question > 0:
            display_current_score()
        
        # Current question
        current_q = QUIZ_DATA[st.session_state.current_question]
        
        st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
        
        # Question header
        st.markdown(f"""
        <div class="question-header">
            Question {st.session_state.current_question + 1} of {len(QUIZ_DATA)}
        </div>
        """, unsafe_allow_html=True)
        
        # Question text
        st.markdown(f"""
        <div class="question-text">
            {current_q['question']}
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.show_explanation:
            # Display options as radio buttons
            selected_option = st.radio(
                "Choose your answer:",
                options=range(len(current_q["options"])),
                format_func=lambda x: current_q["options"][x],
                key=f"q_{st.session_state.current_question}"
            )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Submit Answer", key="submit"):
                    submit_answer(selected_option)
                    st.rerun()
        
        else:
            # Show explanation and result
            user_answer = st.session_state.user_answers[-1]
            is_correct = user_answer['correct']
            
            if is_correct:
                st.markdown(f"""
                <div class="correct-answer">
                    ✅ Correct! Great job!
                </div>
                """, unsafe_allow_html=True)
            else:
                selected_option = current_q["options"][user_answer['selected']]
                correct_option = current_q["options"][current_q['correct']]
                st.markdown(f"""
                <div class="incorrect-answer">
                    ❌ Incorrect. You selected: {selected_option}<br>
                    Correct answer: {correct_option}
                </div>
                """, unsafe_allow_html=True)
            
            # Explanation
            st.info(f"💡 **Explanation:** {current_q['explanation']}")
            
            # Next question button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.session_state.current_question < len(QUIZ_DATA) - 1:
                    if st.button("Next Question", key="next"):
                        next_question()
                        st.rerun()
                else:
                    if st.button("View Results", key="finish"):
                        next_question()
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Quiz completed - show results
        display_final_results()
        
        # Restart option
        st.markdown('<div class="restart-button">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Start New Quiz", key="restart"):
                reset_quiz()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()