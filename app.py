import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="MediGuard",
    page_icon="🩺",
    layout="wide"
)

# Application title
st.title("MediGuard")
st.caption("Clinical Decision Support — Educational Prototype")

st.divider()

st.info(
    "This application uses synthetic data only. "
    "It is not intended for clinical use or prescribing decisions."
)

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a page",
    [
        "Dashboard",
        "Patient Profile",
        "Prescription Review"
    ]
)

if page == "Dashboard":

    st.header("System Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Demo Patients", "0")
    col2.metric("Prescriptions", "0")
    col3.metric("Safety Alerts", "0")

    st.subheader("Welcome to MediGuard")

    st.write(
        "A prototype exploring how software can "
        "support medication safety through structured "
        "data and transparent decision rules."
    )

elif page == "Patient Profile":

    st.header("Patient Profile")

    patient_id = st.text_input(
        "Demo Patient ID",
        placeholder="DEMO-001"
    )

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=25
    )

    notes = st.text_area(
        "Synthetic Medical History",
        placeholder="Enter fictional test information..."
    )

    if st.button("Save Demo Profile"):
        if patient_id.strip():
            st.success("Demo profile entered successfully.")
        else:
            st.warning("Please enter a demo patient ID.")

elif page == "Prescription Review":

    st.header("Prescription Review")

    st.write(
        "This section will later contain "
        "the experimental prescription review engine."
    )

    st.warning("The safety checking engine is not implemented yet.")