import streamlit as st
import re
import pandas as pd
import numpy as np
 
 
st.title('Airport feedback forms')
 
 
if 'stage' not in st.session_state:
    st.session_state.stage = 0
 
def set_stage(stage):
    st.session_state.stage = stage
     
     
     
 
with st.form(key='my_form'):
     
     
    n_forms=st.number_input('Number of forms to create', 0, 10)
     
    submit_button = st.form_submit_button(label='Submit forms', on_click=set_stage, args=(1,))
 
 
if st.session_state.stage > 0:
     
    forms_dict={}
    for i in range(0,n_forms):
        forms_dict[i]=st.text_input(str(i))
 
    st.button('Submit', on_click=set_stage, args=(2,))
     
 
     
if st.session_state.stage > 1:
    for i in forms_dict:
        st.write(forms_dict[i])
         
         
st.button('Reset', on_click=set_stage, args=(0,))