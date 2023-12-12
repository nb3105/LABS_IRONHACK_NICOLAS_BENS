import streamlit as st

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

with st.form(key='my_form'):
    answers = [st.slider(f'## {i+1}. {question}', 0, 5, 2, key=f"slider_{i}") for i, question in enumerate(questions)]

    # Use st.form_submit_button() instead of st.button
    submit_button = st.form_submit_button('Submit forms', on_click=set_stage, args=(1,))

if st.session_state.stage > 0:
    st.write("User responses:")
    for i, (question, answer) in enumerate(zip(questions, answers)):
        st.write(f'{question}: {answer}')

    st.button('Reset', on_click=set_stage, args=(0,))
