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


    # Reset or initialize the response in session_state
    if key not in st.session_state:
        st.session_state[key] = []

    # Display MCQs with checkboxes
    if q_type == "MCQ":
        for i, option in enumerate(options):
            # Render checkbox for each option
            if st.checkbox(option, key=f"{key}_option_{i}"):
                # If checkbox is selected, add the option index (1-based) to the response list
                if (i + 1) not in st.session_state[key]:
                    st.session_state[key].append(i + 1)
            else:
                # If checkbox is deselected, remove the option index from the response list
                if (i + 1) in st.session_state[key]:
                    st.session_state[key].remove(i + 1)
   elif q_type == "SCQ":
        # Assuming there's no pre-selected option; the first option will be selected by default
        selected_option = st.radio(question["question"], options, key=key)
        # Since options are 1-based indices in your JSON, find the index of the selected option + 1
        st.session_state[key] = options.index(selected_option) + 1

    elif q_type == "TF":
        # Handling for True/False questions...
        selected_option = st.radio(question["question"], ["True", "False"], key=key)
        st.session_state[key] = "True" if selected_option == "True" else "False"

    elif q_type == "YN":
        # Handling for Yes/No questions...
        selected_option = st.radio(question["question"], ["Yes", "No"], key=key)
        st.session_state[key] = "Yes" if selected_option == "Yes" else "No"
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
