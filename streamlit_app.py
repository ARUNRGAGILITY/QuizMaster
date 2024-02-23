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
    """Display a question and store the user's response in session_state."""
    q_type = question.get("type")
    options = question.get("options", [])
    key = f"answer_{question_number}"  # Unique key for each question's response

    if q_type == "MCQ" and isinstance(question.get("answers"), list):  # Multiple answers
        st.session_state[key] = st.multiselect(question["question"], options, key=key)
    elif q_type == "MCQ":  # Single answer
        st.session_state[key] = [st.radio(question["question"], options, key=key)]
    else:
        # Handle other types similarly, adjusting for True/False and Yes/No as needed
        pass



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
