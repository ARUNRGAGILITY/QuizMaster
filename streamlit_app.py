import streamlit as st
import os
import json

def load_quiz(file_path):
    """Load the quiz JSON from the given file path."""
    with open(file_path, 'r') as f:
        return json.load(f)

def evaluate_answers(quiz):
    """Evaluate the answers stored in session_state and calculate the score."""
    score = 0
    for i, question in enumerate(quiz["questions"], start=1):
        user_answers = st.session_state.get(f"answer_{i}", [])
        question_type = question.get("type")
        # Handle MCQ and SCQ differently since their correct answers are stored differently
        if question_type in ["MCQ", "SCQ"]:
            # For MCQ and SCQ, correct answers are indicated by index/indices
            correct_indices = question.get("answers") if question_type == "MCQ" else [question.get("answer")]
            # Convert user_answers to indices for comparison
            user_indices = user_answers if question_type == "MCQ" else [user_answers]
            # Check if user_indices match correct_indices (MCQ may have multiple correct answers)
            if sorted(user_indices) == sorted(correct_indices):
                score += 1
        elif question_type in ["TF", "YN"]:
            # For TF and YN, the answer is directly "True", "False", "Yes", or "No"
            correct_answer = question.get("answer")
            # Since user_answers for TF and YN are stored directly as the answer string
            if user_answers == correct_answer:
                score += 1
        else:
            st.error(f"Unknown question type: {question_type}")

    return score



def display_quiz(quiz):
    """Display the quiz questions and evaluate answers on submission."""
    st.subheader(quiz["title"])
    # Reserve space for the score at the top
    top_space_left, top_space_right = st.columns([4, 1])
    score_placeholder = top_space_right.empty()  # This reserves space for the score

    # Display questions in the left (main) column
    with left_col:
        for i, question in enumerate(quiz["questions"], start=1):
            display_question(question, i)

        # Place the submit button in the main column
        if st.button("Submit Quiz"):
            # Calculate the score
            score = evaluate_answers(quiz)
            total = len(quiz["questions"])
            # Use session_state to store the score so we can display it outside the button's conditional block
            st.session_state['score'] = f"Score: {score} out of {total}"

    # Display the score in the right column, but only after the quiz has been submitted
    with right_col:
        if 'score' in st.session_state:
            st.markdown("##")  # Add some space
            st.markdown(f"**{st.session_state['score']}**", unsafe_allow_html=True)


def display_question(question, question_number):
    """Display a question based on its type and capture the user's response."""
    q_type = question.get("type")
    options = question.get("options", [])
    key = f"answer_{question_number}"  # Unique key for each question's response

    # Handle MCQ and SCQ with single or multiple correct answers
    if q_type == "MCQ":
        # Use checkboxes for MCQ to allow multiple selections
        user_responses = []
        for i, option in enumerate(options):
            if st.checkbox(option, key=f"{key}_option_{i}"):
                user_responses.append(i + 1)  # Store 1-based index of selected options
        st.session_state[key] = user_responses
    elif q_type == "SCQ":  # Single Choice Question
        # Single correct answer, use radio for selection
        _ = st.radio(question["question"], options, key=key)
    elif q_type in ["TF", "YN"]:  # True/False and Yes/No Questions
        yn_options = {"TF": ["True", "False"], "YN": ["Yes", "No"]}
        _ = st.radio(question["question"], yn_options[q_type], key=key)
    else:
        st.error("Unknown question type")


# Example usage in Streamlit
def main():
    st.title("Quiz App")

    # Assuming a base path for demonstration
    base_path = "Quiz"
    
   

    # Example for loading a specific quiz - you'll want to replace this with dynamic selection logic
    quiz_path = os.path.join(base_path, "Python", "Basics", "Python_Quiz1.json")
    quiz = load_quiz(quiz_path)

    display_quiz(quiz)

if __name__ == "__main__":
    main()
