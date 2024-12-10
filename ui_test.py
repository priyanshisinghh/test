import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Set page config
st.set_page_config(
    page_title="Stroke Risk Assessment",
    page_icon="🩺",
    layout="centered"
)

# Load the trained model and preprocessing tools
@st.cache_resource
def load_model_and_preprocessors():
    model = joblib.load('model.pkl')  # Load your trained model
    scaler = joblib.load('scaler.pkl')  # Load the scaler (if saved separately)
    preprocessor = joblib.load('preprocessor.pkl')  # Load the preprocessor (if saved separately)
    return model, scaler, preprocessor

model, scaler, preprocessor = load_model_and_preprocessors()

# Inject Custom CSS
def inject_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #f9f9f9;
            font-family: 'Arial', sans-serif;
        }

        h1, h2, h3 {
            color: #4CAF50;
        }

        .stButton > button {
            font-size: 18px;
            background-color: #007BFF;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }

        .stButton > button:hover {
            background-color: #0056b3;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Welcome page
def welcome_page():
    st.title(":blue[Stroke Risk Assessment and Personalized Health Plan]")
    st.write("Understand your stroke risk and get personalized health plans.")
    if st.button("Start Assessment"):
        st.session_state.page = "input_form"

# Input Form Page
def input_form_page():
    st.title("Health Data Input Form")
    st.write("Please fill out the form below with your health details.")
    
    # Collect user inputs
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    avg_glucose = st.number_input("Average Glucose Level (mg/dL)", min_value=50.0, max_value=300.0, value=100.0)
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)
    gender = st.radio("Gender", ["Male", "Female"])
    work_type = st.selectbox("Work Type", ["Child", "Never worked", "Self-Employed", "Private", "Government employed"])
    residence_type = st.selectbox("Residence Type", ["Urban", "Rural"])
    smoking_status = st.selectbox("Smoking Status", ["Never Smoked", "Formerly Smoked", "Smokes", "Unknown"])
    
    # Save inputs
    user_data = pd.DataFrame({
        'age': [age],
        'avg_glucose_level': [avg_glucose],
        'bmi': [bmi],
        'gender': [gender],
        'work_type': [work_type],
        'Residence_type': [residence_type],
        'smoking_status': [smoking_status]
    })

    if st.button("Submit"):
        st.session_state.user_data = user_data
        st.session_state.page = "risk_analysis"

# Risk Analysis Page
def risk_analysis_page():
    st.title("Stroke Risk Analysis")
    user_data = st.session_state.user_data
    
    # Preprocess user input
    user_transformed = preprocessor.transform(user_data)
    user_transformed_df = pd.DataFrame(user_transformed.toarray() if hasattr(user_transformed, 'toarray') else user_transformed)
    
    # Predict stroke risk
    prediction_proba = model.predict_proba(user_transformed_df)[:, 1]
    prediction = (prediction_proba >= 0.3).astype(int)

    st.write("### Prediction:")
    if prediction[0] == 1:
        st.error(f"High Stroke Risk: {prediction_proba[0] * 100:.2f}%")
    else:
        st.success(f"Low Stroke Risk: {prediction_proba[0] * 100:.2f}%")
    
    if st.button("View Recommendations"):
        st.session_state.page = "recommendations"

# Recommendation Page
def recommendation_page():
    st.title("Personalized Health Plan")
    st.write("Based on your input, here are some recommendations to lower your stroke risk.")
    user_data = st.session_state.user_data

    st.subheader("Lifestyle Recommendations")
    if user_data['bmi'][0] > 25:
        st.write("Maintain a healthy weight by exercising regularly.")
    if user_data['avg_glucose_level'][0] > 140:
        st.write("Monitor glucose levels and reduce sugar intake.")
    
    st.subheader("Dietary Changes")
    st.write("Adopt a balanced diet with fruits, vegetables, and whole grains.")

    st.subheader("Medical Advice")
    st.write("Consult with a healthcare provider for regular check-ups.")

# Main Application Logic
def main():
    inject_custom_css()
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
    if "user_data" not in st.session_state:
        st.session_state.user_data = None
    
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "input_form":
        input_form_page()
    elif st.session_state.page == "risk_analysis":
        risk_analysis_page()
    elif st.session_state.page == "recommendations":
        recommendation_page()

if __name__ == "__main__":
    main()
