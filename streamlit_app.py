import streamlit as st
import os
import json

def load_quiz(file_path):
    """Load the quiz JSON from the given file path."""
    with open(file_path, 'r') as f:
        return json.load(f)
def display_question(question):
    """Display a question based on its type and collect answers."""
    q_type = question.get("type")
    options = question.get("options", [])
    if q_type == "MCQ":
        # For multiple choice questions with possibly multiple answers
        if question.get("multiple_answers", False):
            answer = st.multiselect(question["question"], options)
        else:
            answer = [st.radio(question["question"], options)]
    elif q_type in ["SCQ", "TF", "YN"]:
        # Single-choice questions, True/False, and Yes/No can use the same radio button control
        answer = [st.radio(question["question"], options)]
    else:
        st.write("Unknown question type")
        return None
    return answer

def evaluate_answers(quiz):
    """Evaluate the answers provided by the user and calculate the score."""
    score = 0
    for question in quiz["questions"]:
        user_answer = display_question(question)
        correct_answer = question.get("answer", question.get("answers", []))
        if user_answer is not None and sorted(user_answer) == sorted(correct_answer if isinstance(correct_answer, list) else [correct_answer]):
            score += 1
    return score

def display_quiz(quiz):
    """Display the quiz and evaluate answers."""
    st.subheader(quiz["title"])
    if st.button("Submit Quiz"):
        score = evaluate_answers(quiz)
        total = len(quiz["questions"])
        st.write(f"Score: {score} out of {total}")


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
