import streamlit as st
import pandas as pd


# Set page config
st.set_page_config(
    page_title="Stroke Risk Assessment",
    page_icon="🩺",
    layout="centered"
)

# Inject Custom CSS
def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Global styles */
        body {
            background-color: #f9f9f9;
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
        }

        /* Welcome page background */
        .welcome-page {
            background-image: url('https://imgur.com/a/dTlqCP1'); /* Replace with your image URL */
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: red;
        }

        /* Custom heading colors */
        h1, h2, h3 {
            color: #4CAF50; /* Green color for headings */
        }

        /* Custom button styling */
        .stButton > button {
            font-size: 18px;
            background-color: #007BFF;
            color: white;
            border: none;
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

# welcome page
def welcome_page():
    st.markdown('<div class="welcome-page">', unsafe_allow_html=True)
    st.title(":blue[Stroke Risk Assessment and Personalized Health Plan]")
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
    
    gender_option = st.radio("Gender", ["Male", "Female"])
    gender = 0 if gender_option == "Male" else 1
    
    age = st.number_input("Age", min_value=0, max_value=120, value=20, step=1)
    bmi = st.number_input("Body Mass Index (BMI)", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
    avg_glucose = st.number_input("Average Glucose Level (mg/dL)", min_value=0.0, max_value=500.0, value=100.0, step=0.1)
    
    hypertension_option = st.selectbox("Hypertension (High Blood Pressure)", ["No", "Yes"])
    hypertension = 0 if hypertension_option == "No" else 1
    
    heart_disease_option = st.selectbox("Heart Disease", ["No", "Yes"])
    heart_disease = 0 if heart_disease_option == "No" else 1
    
    smoking_status_option = st.selectbox("Smoking Status", ["Never smoked", "Formerly smoked", "Smokes", "Unknown"])
    smoking_status = {
        "Never smoked": 0,
        "Formerly smoked": 1,
        "Smokes": 2,
        "Unknown": 3
    }[smoking_status_option]

    if st.button("Submit"):
        # Save the data to session state for next page
        st.session_state.health_data = {
            "Age": age,
            "BMI": bmi,
            "Average Glucose Level": avg_glucose,
            "Hypertension": hypertension,
            "Heart Disease": heart_disease,
            "Smoking Status": smoking_status
        }
        st.session_state.page = "risk_analysis"


# risk analysis page
def risk_analysis_page():
    st.title("Stroke Risk Analysis")
    st.write("Based on your input, here is your stroke risk assessment.")

    # Fetch the saved data
    data = st.session_state.get("health_data", {})
    
    # Dummy calculation for stroke risk (replace with actual model)
    risk_score = (data["BMI"] + data["Average Glucose Level"]) * 0.1
    risk_score = min(max(risk_score, 0), 100)  # Ensure risk_score is between 0-100

    # Display risk
    risk_color = "green" if risk_score < 33 else "yellow" if risk_score < 66 else "red"
    st.write(f"Your stroke risk is {risk_score:.1f}%.")
    st.markdown(
    """
    <style>
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #11ff00, #ff0000);
        }
    </style>""",
    unsafe_allow_html=True,
)
    st.progress(0.9)

    # Contributing factors
    st.subheader("Top Contributing Factors")
    factors = []
    if data["BMI"] > 25:
        factors.append(f"High BMI ({data['BMI']})")
    if data["Average Glucose Level"] > 140:
        factors.append(f"Elevated Glucose Levels ({data['Average Glucose Level']} mg/dL)")
    if data["Hypertension"] == "Yes":
        factors.append("Hypertension")
    if data["Heart Disease"] == "Yes":
        factors.append("Heart Disease")

    if factors:
        st.write(", ".join(factors))
    else:
        st.write("No major contributing factors detected.")

    if st.button("View Recommendations"):
        st.session_state.page = "recommendations"

# Recommendation Page
def recommendation_page():
    st.title("Personalized Health Plan")
    st.write("Here are some recommendations tailored to your health data:")

    # Fetch the saved data
    data = st.session_state.get("health_data", {})

    # Recommendations
    st.subheader("Lifestyle Recommendations")
    if data["BMI"] > 25:
        st.write("Incorporate 30 minutes of moderate exercise, 5 days a week.")
    if data["Average Glucose Level"] > 140:
        st.write("Reduce sugar intake and monitor glucose levels weekly.")
    
    st.subheader("Medical Advice")
    if data["Hypertension"] == "Yes":
        st.write("Consider consulting a doctor to manage hypertension.")
    if data["Heart Disease"] == "Yes":
        st.write("Regularly monitor your heart health with a healthcare provider.")

    st.subheader("Dietary Changes")
    st.write("Adopt a low-sodium, high-fiber diet. Include fruits, vegetables, and whole grains.")
    
    # Visualization (Example pie chart)
    st.subheader("Diet Breakdown")
    diet_data = pd.DataFrame({
        "Category": ["Fruits & Vegetables", "Proteins", "Carbs", "Fats"],
        "Percentage": [50, 25, 15, 10]
    })
    st.bar_chart(diet_data.set_index("Category"))

    if st.button("Download Plan"):
        st.write("Download functionality coming soon.")

# Main Application Logic
def main():
    inject_custom_css()
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
    if "health_data" not in st.session_state:
        st.session_state.health_data = {}
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