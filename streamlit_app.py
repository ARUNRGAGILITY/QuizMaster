import streamlit as st
import os
import json
from datetime import datetime, timedelta


# === OBO ===

def display_current_question(quiz, current_index):
    question = quiz["questions"][current_index]
    st.write(f"{question}")
    this_question = question["question"]
    this_no = current_index + 1
    st.markdown(f"##### Q{this_no}: {this_question}")
    options = question['options']
    if question["type"] == "MCQ":
        st.markdown(f"##### {options}")


def display_progress_with_text(current, total):
    """Displays a progress bar with text indicating the current question number out of total questions."""
    progress_text = f"{current} / {total}"
    st.write(progress_text)  # Display text like "1/5"
    progress_value = current / total
    st.progress(progress_value)

def display_navigation_buttons(current_index, total_questions):
    # Create a row with three columns: Previous, Submit, and Next
    prev_col, submit_col, next_col = st.columns([1, 1, 1], gap="small")

    # Display "Previous" button if not the first question
    with prev_col:
        if current_index > 0:
            if st.button("Previous"):
                st.session_state.current_question_index -= 1

    # "Submit" button centered in the middle column
    with submit_col:
        if st.button("Submit"):
            st.session_state.quiz_complete = True

    # Display "Next" button if not the last question
    with next_col:
        if current_index < total_questions - 1:
            if st.button("Next"):
                st.session_state.current_question_index += 1

    st.write("")
    


def display_question_with_navigation(quiz):
    current_index = st.session_state.get("current_question_index", 0)
    total_questions = len(quiz["questions"])
    # Display progress bar with text
    display_progress_with_text(current_index + 1, total_questions)
    # Display navigation buttons
    display_navigation_buttons(current_index, total_questions)
    display_current_question(quiz, current_index)


def setup_quiz_environment(quiz):
    """Setup initial quiz state including timing and progress, ensuring timer is initialized only once."""
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0  # Start with the first question
        st.session_state.score = 0  # Initial score

    # Check if the timer has already been initialized to avoid resetting it
    if 'timer_initialized' not in st.session_state:
        # Setup timing based on quiz specification
        if quiz.get("timed", "no") != "no":
            st.session_state.is_timed = True
            st.session_state.start_time = datetime.now()
            st.session_state.time_limit = quiz["timed"]
            st.session_state.end_time = st.session_state.start_time + timedelta(seconds=st.session_state.time_limit)
        else:
            st.session_state.is_timed = False
        
        # Mark the timer as initialized to prevent re-initialization
        st.session_state.timer_initialized = True


def display_progress(current, total):
    """Displays a progress bar based on the current question index and total questions."""
    progress_value = current / total
    st.progress(progress_value)

def display_timer(quiz):
    """Displays a timer if the quiz is timed."""
    # var1 = quiz.get("timed", "no") != "no"
    # var2 = 'end_time' in st.session_state
    # st.sidebar.write(f"===== VAR1 {var1} {var2}")
    if quiz.get("timed", "no") != "no" and 'end_time'  in st.session_state:
        #st.sidebar.write("==========TIMER=============")
        time_left = st.session_state.end_time - datetime.now()
        total_seconds = int(time_left.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_left.total_seconds() > 0:
            st.sidebar.write(f"Time left: {hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            st.sidebar.write("Time's up!")


# Update display_questions_and_collect_answers to show one question at a time, and evaluate_answers_and_display_score as needed


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
                
                 # Setup initial state if not already set
                if 'current_question_index' not in st.session_state:
                    st.session_state.current_question_index = 0
                    st.session_state.quiz_complete = False

                                       
                setup_quiz_environment(quiz)  # Initialize quiz environment including timing
                display_timer(quiz)  # Display the timer
        
                question_display_mode = quiz.get("question_display", "all")
                total_questions = len(quiz["questions"])
        
                # Check if we are displaying questions one at a time
                if question_display_mode == "1":
                    display_question_with_navigation(quiz)
                    print(f"One question by question")
                elif question_display_mode == "all":
                    display_questions_and_collect_answers(quiz) 
                            
                # Button to submit answers and evaluate the quiz
                if st.button('Submit Quiz'):
                    print(f">>> === {st.session_state}=== <<<")
                    evaluate_answers_and_display_score(quiz)    


# Ensure the main function is called when the script is run
if __name__ == "__main__":
    main()