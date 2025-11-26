import streamlit as st
import pandas as pd
from prediction_helper import predict

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Health Insurance Predictor",
    layout="centered"
)

# -------------------- GLOBAL CSS --------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.main {
    background: linear-gradient(135deg, #d4fc79, #96e6a1);
}

.card {
    background: rgba(255,255,255,0.15);
    padding: 30px 25px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.title {
    font-size: 42px;
    font-weight: 600;
    color: #003f2b;
    text-align: center;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 18px;
    text-align: center;
    color: #074d36;
}

/* Button */
.stButton > button {
    background: #0f9d58;
    color: white;
    padding: 14px 30px;
    border-radius: 12px;
    border: none;
    font-size: 20px;
    font-weight: 600;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.06);
    background: #0a7f45;
    cursor: pointer;
}

</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="title">🩺 Health Insurance Cost Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Provide your information for quick prediction</div>', unsafe_allow_html=True)
st.write("")

# -------------------- CARD UI --------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # -------- INPUT FIELDS WITH SPACING --------
    col1, col2 = st.columns(2, gap="large")
    with col1:
        age = st.slider("Age", 18, 100, 25)
    with col2:
        gender = st.selectbox("Gender", ['Male', 'Female'])

    col3, col4 = st.columns(2, gap="large")
    with col3:
        region = st.selectbox("Region", ['Northeast', 'Northwest', 'Southeast', 'Southwest'])
    with col4:
        marital_status = st.selectbox("Marital Status", ['Unmarried', 'Married'])

    col5, col6 = st.columns(2, gap="large")
    with col5:
        bmi_category = st.selectbox("BMI Category", ['Overweight', 'Underweight', 'Normal', 'Obesity'])
    with col6:
        smoking_status = st.selectbox("Smoking Status", ['No Smoking', 'Regular', 'Occasional'])

    col7, col8 = st.columns(2, gap="large")
    with col7:
        employment_status = st.selectbox("Employment Status", ['Self-Employed', 'Freelancer', 'Salaried'])
    with col8:
        income_lakhs = st.number_input("Annual Income (Lakhs)", 0, 100, 0)

    col9, col10 = st.columns(2, gap="large")
    with col9:
        medical_history = st.selectbox("Medical History", [
            'High blood pressure', 'No Disease', 'Diabetes & High blood pressure',
            'Diabetes & Heart disease', 'Diabetes', 'Diabetes & Thyroid',
            'Heart disease', 'Thyroid', 'High blood pressure & Heart disease'
        ])
    with col10:
        insurance_plan = st.selectbox("Insurance Plan", ['Silver', 'Bronze', 'Gold'])

    col11, col12 = st.columns(2, gap="large")
    with col11:
        number_of_dependants = st.number_input("Dependants", 0, 10, 0)
    with col12:
        genetical_risk = st.selectbox("Genetic Risk", ['No Risk', 'Low', 'Medium', 'High'])

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- INPUT DATA --------------------
input_data = {
    "age": age,
    "gender": gender,
    "region": region,
    "marital_status": marital_status,
    "bmi_category": bmi_category,
    "smoking_status": smoking_status,
    "employment_status": employment_status,
    "income_lakhs": income_lakhs,
    "medical_history": medical_history,
    "insurance_plan": insurance_plan,
    "number_of_dependants": number_of_dependants,
    "genetical_risk": genetical_risk
}

# -------------------- BUTTON --------------------
st.write("")
center_btn = st.columns([3, 2, 3])[1]

with center_btn:
    predict_btn = st.button("Predict Cost")

# -------------------- RESULT --------------------
if predict_btn:
    with st.spinner("⏳ Calculating your insurance cost..."):
        result = predict(input_data)

    st.success(f"### 💵 Predicted Insurance Cost: **₹{result:.2f}**")
    st.markdown("<hr>", unsafe_allow_html=True)


