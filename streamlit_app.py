import streamlit as st
import os
import json

def list_topics(base_path="Quiz"):
    """List all quiz topics."""
    return [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]

def list_levels(topic, base_path="Quiz"):
    """List all levels within a topic."""
    topic_path = os.path.join(base_path, topic)
    return [name for name in os.listdir(topic_path) if os.path.isdir(os.path.join(topic_path, name))]

def list_quizzes(topic, level, base_path="Quiz"):
    """List all quizzes within a level of a topic."""
    level_path = os.path.join(base_path, topic, level)
    return [name for name in os.listdir(level_path) if name.endswith('.json')]

def load_quiz(topic, level, quiz_file, base_path="Quiz"):
    """Load a specific quiz JSON file."""
    quiz_path = os.path.join(base_path, topic, level, quiz_file)
    with open(quiz_path, 'r') as file:
        return json.load(file)


def display_questions_and_collect_answers(quiz):
    for i, question in enumerate(quiz["questions"], start=1):
        key = f"question_{i}"
        st.markdown(f"#### Q{i}: {question['question']}")

        if question["type"] == "MCQ":
            options = question['options']
            # Use checkboxes for MCQ to allow multiple selections
            user_responses = []
            for i, option in enumerate(options):
                if st.checkbox(option, key=f"{key}_option_{i}"):
                    user_responses.append(i + 1)  # Store 1-based index of selected options
            

        if question["type"] == "SCQ":
            options = question['options']
            # Use checkboxes for MCQ to allow multiple selections
            user_input = st.radio(question["question"], options, key=key)
            #print(f">>> === {user_input} === <<<")
            
def evaluate_answers_and_display_score(quiz):
    score = 0
    mcq_answers = {}  # To aggregate MCQ answers since they're spread across multiple keys

    for key, value in st.session_state.items():
        if key.startswith("question_"):
            question_num = int(key.split("_")[1])
            question = quiz["questions"][question_num - 1]
            
            # Handle MCQs: Aggregate answers based on question number
            if question["type"] == "MCQ" and "option" in key:
                if question_num not in mcq_answers:
                    mcq_answers[question_num] = []
                if value:  # If the option was selected (True), store its index
                    option_index = int(key.split("_")[-1]) + 1
                    mcq_answers[question_num].append(option_index)
            
            # Handle SCQs: Direct comparison since only one answer per question
            elif question["type"] == "SCQ":
                correct_answer = question["answer"]
                selected_answer = None
                if isinstance(value, str):  # Assuming the answer is stored as the option text
                    selected_answer = question["options"].index(value) + 1
                elif isinstance(value, int):  # Or if the answer is stored as an index
                    selected_answer = value
                
                if selected_answer == correct_answer:
                    score += 1

    # Evaluate MCQs now that all options are aggregated
    for question_num, selected_options in mcq_answers.items():
        question = quiz["questions"][question_num - 1]
        correct_answers = question["answers"]
        print(f">>> === MCQ{correct_answers} === <<<")
        if sorted(selected_options) == sorted(correct_answers):
            score += 1
            #print(f">>> === MCQ{score} === <<<")
            

    # Display the score
    total_questions = len(quiz['questions'])
    st.metric(label="Score", value=f"{score} / {total_questions}")


def main():
    st.sidebar.title("QuizMaster")

    # Adjusted Topic selection to include a "Select" prompt
    topics = ["Select"] + list_topics()  # Prepend "Select" to the list of topics
    selected_topic = st.sidebar.selectbox("Select a Topic", topics)

    # Adjusted Level selection to include a "Select" prompt and conditional display
    if selected_topic and selected_topic != "Select":
        levels = ["Select"] + list_levels(selected_topic)
        selected_level = st.sidebar.selectbox("Select a Level", levels)

        # Adjusted Quiz selection to include a "Select" prompt and conditional display
        if selected_level and selected_level != "Select":
            quizzes = ["Select"] + list_quizzes(selected_topic, selected_level)
            selected_quiz = st.sidebar.selectbox("Select a Quiz", quizzes)

            # Load and display the selected quiz, ensuring "Select" is not treated as a valid selection
            if selected_quiz and selected_quiz != "Select":
                quiz = load_quiz(selected_topic, selected_level, selected_quiz)
                st.title(quiz["title"])
                
                # Display questions and collect answers
                display_questions_and_collect_answers(quiz)

                # Button to submit answers and evaluate the quiz
                if st.button('Submit Quiz'):
                    print(f">>> === {st.session_state}=== <<<")
                    evaluate_answers_and_display_score(quiz)


# Ensure the main function is called when the script is run
if __name__ == "__main__":
    main()