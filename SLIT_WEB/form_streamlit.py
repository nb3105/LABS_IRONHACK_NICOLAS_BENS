import streamlit as st
import pandas as pd

st.title('Airport feedback forms')

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_stage(stage):
    st.session_state.stage = stage

# Define the fixed questions
questions = [
    "How satisfied are you with the cleanliness of the airport?",
    "How satisfied are you with the customer service?",
    "How satisfied are you with the facilities?",
    "How satisfied are you with the facilities?",
    "How satisfied are you with the facilities?",
    "How satisfied are you with the facilities?",
    "How satisfied are you with the facilities?",
    "How satisfied are you with the facilities?",
    "How satisfied are you with the facilities?",
    "How satisfied are you with the facilities?"
    # Add more questions as needed
]

# Load existing data or create an empty DataFrame
csv_file_path = 'user_responses.csv'
try:
    user_responses = pd.read_csv(csv_file_path)
except FileNotFoundError:
    user_responses = pd.DataFrame(columns=['Timestamp'] + questions)

with st.form(key='my_form'):
    answers = [st.slider(f'## {i+1}. {question}', 0, 5, 2, key=f"slider_{i}") for i, question in enumerate(questions)]

    submit_button = st.form_submit_button('Submit forms', on_click=set_stage, args=(1,))

if st.session_state.stage > 0:
    # Get current timestamp
    timestamp = pd.to_datetime('now').strftime('%Y-%m-%d %H:%M:%S')

    # Add user responses to DataFrame
    user_data = pd.DataFrame([[timestamp] + answers], columns=['Timestamp'] + questions)

    # If the user_responses DataFrame is empty, initialize it with the correct columns
    if user_responses.empty:
        user_responses = pd.DataFrame(columns=['Timestamp'] + questions)

    # Append user_data to user_responses
    user_responses = user_responses.append(user_data, ignore_index=True)

    # Save DataFrame to CSV
    user_responses.to_csv(csv_file_path, index=False)

    st.write("User responses:")
    for i, (question, answer) in enumerate(zip(questions, answers)):
        st.write(f'{question}: {answer}')

    st.button('Reset', on_click=set_stage, args=(0,))
