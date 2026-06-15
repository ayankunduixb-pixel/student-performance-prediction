import streamlit as st
import pandas as pd
import joblib

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ==========================
# LOAD MODEL
# ==========================

model = joblib.load("models/student_score_predictor.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

# ==========================
# HEADER
# ==========================

st.title("🎓 Student Performance Prediction Dashboard")

st.markdown("""
Predict a student's **Math Score** using Machine Learning.

This project uses a trained model built with:
- Python
- Pandas
- Scikit-Learn
- Streamlit
""")

st.markdown("---")

# ==========================
# SIDEBAR INPUTS
# ==========================

st.sidebar.title("📋 Student Information")

gender = st.sidebar.selectbox(
    "Gender",
    ["female", "male"]
)

race_ethnicity = st.sidebar.selectbox(
    "Race / Ethnicity",
    [
        "group A",
        "group B",
        "group C",
        "group D",
        "group E"
    ]
)

parental_education = st.sidebar.selectbox(
    "Parental Level of Education",
    [
        "some high school",
        "high school",
        "some college",
        "associate's degree",
        "bachelor's degree",
        "master's degree"
    ]
)

lunch = st.sidebar.selectbox(
    "Lunch Type",
    [
        "standard",
        "free/reduced"
    ]
)

test_preparation_course = st.sidebar.selectbox(
    "Test Preparation Course",
    [
        "none",
        "completed"
    ]
)

reading_score = st.sidebar.slider(
    "Reading Score",
    0,
    100,
    50
)

writing_score = st.sidebar.slider(
    "Writing Score",
    0,
    100,
    50
)

# ==========================
# CREATE INPUT DATAFRAME
# ==========================

input_df = pd.DataFrame(
    columns=feature_columns
)

input_df.loc[0] = 0

# Numerical Features

if "reading score" in input_df.columns:
    input_df["reading score"] = reading_score

if "writing score" in input_df.columns:
    input_df["writing score"] = writing_score

# Gender

if gender == "male":
    if "gender_male" in input_df.columns:
        input_df["gender_male"] = 1

# Race

race_col = f"race/ethnicity_{race_ethnicity}"

if race_col in input_df.columns:
    input_df[race_col] = 1

# Parent Education

parent_col = (
    f"parental level of education_{parental_education}"
)

if parent_col in input_df.columns:
    input_df[parent_col] = 1

# Lunch

lunch_col = f"lunch_{lunch}"

if lunch_col in input_df.columns:
    input_df[lunch_col] = 1

# Test Preparation

prep_col = (
    f"test preparation course_{test_preparation_course}"
)

if prep_col in input_df.columns:
    input_df[prep_col] = 1

# ==========================
# DASHBOARD LAYOUT
# ==========================

col1, col2 = st.columns([2, 1])

with col1:

    st.subheader("📊 Student Profile")

    profile_df = pd.DataFrame({
        "Feature": [
            "Gender",
            "Race/Ethnicity",
            "Parental Education",
            "Lunch",
            "Test Preparation",
            "Reading Score",
            "Writing Score"
        ],
        "Value": [
            gender,
            race_ethnicity,
            parental_education,
            lunch,
            test_preparation_course,
            reading_score,
            writing_score
        ]
    })

    st.dataframe(
        profile_df,
        use_container_width=True
    )

with col2:

    st.subheader("📈 Current Scores")

    chart_df = pd.DataFrame({
        "Score": [
            reading_score,
            writing_score
        ]
    },
    index=[
        "Reading",
        "Writing"
    ])

    st.bar_chart(chart_df)

st.markdown("---")

# ==========================
# PREDICTION SECTION
# ==========================

if st.button(
    "🚀 Predict Math Score",
    use_container_width=True
):

    prediction = model.predict(input_df)

    predicted_score = float(prediction[0])

    st.success(
        f"Predicted Math Score: {predicted_score:.2f}"
    )

    st.markdown("### 📋 Performance Assessment")

    if predicted_score >= 85:
        st.success(
            "Excellent Performance Expected 🌟"
        )

    elif predicted_score >= 70:
        st.info(
            "Good Performance Expected 👍"
        )

    elif predicted_score >= 50:
        st.warning(
            "Average Performance Expected ⚠️"
        )

    else:
        st.error(
            "Needs Additional Academic Support 📚"
        )

st.markdown("---")

# ==========================
# FOOTER
# ==========================

st.markdown("""
### 🔍 About This Project

This dashboard predicts student math performance
using a Machine Learning model trained on the
Students Performance Dataset.

**Created By:** Ayan Kundu  
**Tech Stack:** Python, Pandas, Scikit-Learn, Streamlit
""")