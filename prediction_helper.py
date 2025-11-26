import pandas as pd
from joblib import load

model_rest = load("artifacts/model_rest.joblib")
model_young = load("artifacts/model_young.joblib")

scaler_rest = load("artifacts/scaler_rest.joblib")
scaler_young = load("artifacts/scaler_young.joblib")


# ----------------------------------------
#  MEDICAL RISK NORMALIZATION
# ----------------------------------------
def calculate_normalized_risk(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    diseases = medical_history.lower().split(" & ")
    total_risk_score = sum(risk_scores.get(disease.strip(), 0) for disease in diseases)

    max_score = 14
    min_score = 0
    return (total_risk_score - min_score) / (max_score - min_score)


# ----------------------------------------
#  PREPROCESS PIPELINE
# ----------------------------------------
def preprocess_input(input_data):

    expected_cols = [
        'age', 'number_of_dependants', 'income_lakhs', 'insurance_plan',
        'genetical_risk', 'normalized_risk_score',

        'gender_Male',
        'region_Northwest', 'region_Southeast', 'region_Southwest',
        'marital_status_Unmarried',

        'bmi_category_Obesity', 'bmi_category_Overweight', 'bmi_category_Underweight',

        'smoking_status_Occasional', 'smoking_status_Regular',

        'employment_status_Salaried', 'employment_status_Self-Employed'
    ]

    df = pd.DataFrame(0, columns=expected_cols, index=[0])

    # -----------------------------
    # Continuous inputs
    # -----------------------------
    df["age"] = input_data["age"]
    df["number_of_dependants"] = input_data["number_of_dependants"]
    df["income_lakhs"] = input_data["income_lakhs"]

    # -----------------------------
    # Insurance plan
    # -----------------------------
    plan_map = {"Bronze": 1, "Silver": 2, "Gold": 3}
    df["insurance_plan"] = plan_map[input_data["insurance_plan"]]

    # -----------------------------
    # Genetical risk
    # -----------------------------
    genetical_map = {"No Risk": 0, "Low": 1, "Medium": 2, "High": 3}
    df["genetical_risk"] = genetical_map[input_data["genetical_risk"]]

    # -----------------------------
    # Medical history → normalized score
    # -----------------------------
    df["normalized_risk_score"] = calculate_normalized_risk(input_data["medical_history"])

    # -----------------------------
    # Gender
    # -----------------------------
    if input_data["gender"] == "Male":
        df["gender_Male"] = 1

    # -----------------------------
    # Region
    # -----------------------------
    region_col = f"region_{input_data['region']}"
    if region_col in df.columns:
        df[region_col] = 1

    # -----------------------------
    # Marital status
    # -----------------------------
    if input_data["marital_status"] == "Unmarried":
        df["marital_status_Unmarried"] = 1

    # -----------------------------
    # BMI
    # -----------------------------
    bmi_map = {
        "Obesity": "bmi_category_Obesity",
        "Overweight": "bmi_category_Overweight",
        "Underweight": "bmi_category_Underweight"
    }
    if input_data["bmi_category"] in bmi_map:
        df[bmi_map[input_data["bmi_category"]]] = 1

    # -----------------------------
    # Smoking
    # -----------------------------
    if input_data["smoking_status"] == "Occasional":
        df["smoking_status_Occasional"] = 1
    if input_data["smoking_status"] in ["Regular", "Smoking=0"]:
        df["smoking_status_Regular"] = 1

    # -----------------------------
    # Employment
    # -----------------------------
    if input_data["employment_status"] == "Salaried":
        df["employment_status_Salaried"] = 1
    if input_data["employment_status"] == "Self-Employed":
        df["employment_status_Self-Employed"] = 1

    # -----------------------------
    # Scaling
    # -----------------------------
    df = handle_scaling(input_data["age"], df)

    return df


# ----------------------------------------
#  SCALING BASED ON AGE
# ----------------------------------------
def handle_scaling(age, df):
    scaler_object = scaler_young if age <= 25 else scaler_rest

    cols_to_scale = scaler_object["cols_to_scale"]
    scaler = scaler_object["scaler"]

    df['income_level'] = None
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df.drop('income_level', axis=1, inplace=True)

    return df


# ----------------------------------------
#  FINAL PREDICT FUNCTION
# ----------------------------------------
def predict(input_data):
    processed = preprocess_input(input_data)

    model = model_young if input_data["age"] <= 25 else model_rest

    prediction = model.predict(processed)[0]
    return int(prediction)
