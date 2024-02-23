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
        user_answer = st.session_state.get(f"answer_{i}", None)
        correct_answer = question.get("answer", question.get("answers"))
        if isinstance(correct_answer, list):
            correct_answer = [question["options"][index-1] for index in correct_answer]
        else:
            correct_answer = question["options"][correct_answer-1]
        
        if user_answer == correct_answer:
            score += 1
    
    return score

def display_quiz(quiz):
    """Display the quiz questions and evaluate answers on submission."""
    st.subheader(quiz["title"])

    # Display questions
    for i, question in enumerate(quiz["questions"], start=1):
        display_question(question, i)

    # Submission button
    if st.button("Submit Quiz"):
        score = evaluate_answers(quiz)
        total = len(quiz["questions"])
        st.write(f"Score: {score} out of {total}")

def display_question(question, question_number):
    """Display a question based on its type and capture the user's response using checkboxes for MCQ."""
    q_type = question.get("type")
    options = question.get("options", [])
    key_prefix = f"answer_{question_number}_"  # Unique key prefix for each option's response

    if q_type == "MCQ":
        user_responses = []
        for i, option in enumerate(options, start=1):
            # Create a unique key for each checkbox representing an option
            option_key = f"{key_prefix}{i}"
            # Render the checkbox and check if it's selected
            if st.checkbox(option, key=option_key):
                # If selected, append the option's index (1-based) to the user_responses
                user_responses.append(i)
        # Store the indices of selected options in session_state under a consolidated key
        st.session_state[f"answer_{question_number}"] = user_responses

    elif q_type == "SCQ":
        # Render a single-choice question using radio buttons
        selected_index = st.radio(question["question"], options, key=key_prefix)
        # Store the index of the selected option (1-based)
        st.session_state[f"answer_{question_number}"] = [selected_index + 1] if selected_index is not None else []

    elif q_type in ["TF", "YN"]:
        # For True/False and Yes/No questions, map answers to boolean values and use radio buttons
        yn_options = ["True", "False"] if q_type == "TF" else ["Yes", "No"]
        selected_option = st.radio(question["question"], yn_options, key=key_prefix)
        # Store the selected option directly
        st.session_state[f"answer_{question_number}"] = selected_option

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
