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
    """Display a question based on its type and capture the user's response."""
    q_type = question.get("type")
    options = question.get("options", [])
    key = f"answer_{question_number}"  # Unique key for each question's response

    if q_type == "MCQ":
        # Use checkboxes for MCQ to allow multiple selections
        user_responses = []
        for i, option in enumerate(options):
            if st.checkbox(option, key=f"{key}_option_{i}"):
                user_responses.append(i + 1)  # Store 1-based index of selected options
        st.session_state[key] = user_responses

    elif q_type == "SCQ":
        # Use radio buttons for SCQ to allow a single selection
        selected_index = st.radio(question["question"], options, key=key)
        # Store the 1-based index of the selected option
        st.session_state[key] = [options.index(selected_index) + 1]

    elif q_type == "TF":
        # True/False questions treated as SCQ with True/False options
        tf_options = ["True", "False"]
        selected_option = st.radio(question["question"], tf_options, key=key)
        # Store "True" or "False" as the answer
        st.session_state[key] = selected_option

    elif q_type == "YN":
        # Yes/No questions treated similarly to TF
        yn_options = ["Yes", "No"]
        selected_option = st.radio(question["question"], yn_options, key=key)
        # Store "Yes" or "No" as the answer
        st.session_state[key] = selected_option

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
