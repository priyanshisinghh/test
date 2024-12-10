import streamlit as st
import pandas as pd

# welcome page
def welcome_page():
    st.title("Stroke Risk Assessment and Personalized Health Plan")
    st.write("""
    Understanding your stroke risk is vital to taking control of your health. 
    This system helps you assess your risk and provides actionable, personalized health plans.
    """)
    if st.button("Start Assessment"):
        st.session_state.page = "input_form"

# input page
def input_form_page():
    st.title("Health Data Input Form")
    st.write("Please fill out the form below with your health details.")
    