import streamlit as st

st.title('Airport feedback forms')

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_stage(stage):
    st.session_state.stage = stage

with st.form(key='my_form'):
    n_forms = 10  # Fixed number of questions
    answers = [st.slider(f'Question {i+1}', 0, 5, 2) for i in range(n_forms)]

    submit_button = st.form_submit_button(label='Submit forms', on_click=set_stage, args=(1,))

if st.session_state.stage > 0:
    st.write("User responses:")
    for i, answer in enumerate(answers):
        st.write(f'Question {i+1}: {answer}')

    st.button('Reset', on_click=set_stage, args=(0,))
