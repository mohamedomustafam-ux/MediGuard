
import streamlit as st
import sqlite3

from database.database import (
    init_db,
    create_patient,
    get_all_patients,
    get_patient,
    get_patient_history,
    create_medication,
    get_all_medications,
)

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="MediGuard",
    page_icon="🩺",
    layout="wide"
)

st.title("MediGuard")
st.caption("Clinical Decision Support — Educational Prototype")

st.info(
    "Synthetic data only. Not intended for clinical "
    "use or prescribing decisions."
)

# Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Patient Profile",
        "Medication Management",
        "Prescription Review"
    ]
)


# ---------------------------------
# DASHBOARD
# ---------------------------------

if page == "Dashboard":

    st.header("System Dashboard")

    patients = get_all_patients()

    col1, col2, col3 = st.columns(3)

    col1.metric("Demo Patients", len(patients))
    col2.metric("Prescriptions", 0)
    col3.metric("Safety Alerts", 0)

    st.subheader("Recent Patients")

    if patients:
        st.dataframe(
            patients,
            use_container_width=True
        )
    else:
        st.info("No demo patients registered yet.")


# ---------------------------------
# PATIENT PROFILE
# ---------------------------------

elif page == "Patient Profile":

    st.header("Patient Management")

    st.subheader("Register a Demo Patient")

    with st.form("patient_form"):

        patient_code = st.text_input(
            "Patient Code",
            placeholder="DEMO-001"
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=25
        )

        condition = st.text_input(
            "Fictional Medical Condition",
            placeholder="Example: Demo Condition A"
        )

        notes = st.text_area(
            "Additional Synthetic Notes"
        )

        submitted = st.form_submit_button(
            "Save Patient"
        )

        if submitted:

            if not patient_code.strip():
                st.error("Patient code is required.")

            else:
                try:
                    patient_id = create_patient(
                        patient_code.strip(),
                        int(age),
                        condition,
                        notes
                    )

                    st.success(
                        f"Patient saved successfully. "
                        f"Database ID: {patient_id}"
                    )

                except sqlite3.IntegrityError:
                    st.error(
                        "This patient code already exists."
                    )

                except sqlite3.Error as error:
                    st.error(f"Database error: {error}")


    st.divider()

    st.subheader("Retrieve Patient Profile")

    patients = get_all_patients()

    if patients:

        patient_options = {
            f"{p['patient_code']} (ID: {p['id']})": p['id']
            for p in patients
        }

        selected_patient = st.selectbox(
            "Select a patient",
            options=list(patient_options.keys())
        )

        if st.button("Load Patient Profile"):

            patient_id = patient_options[selected_patient]

            patient = get_patient(patient_id)

            history = get_patient_history(patient_id)

            if patient:

                st.success("Patient retrieved successfully.")

                col1, col2 = st.columns(2)

                col1.metric(
                    "Patient Code",
                    patient["patient_code"]
                )

                col2.metric(
                    "Age",
                    patient["age"]
                )

                st.subheader("Synthetic Medical History")

                if history:

                    for item in history:

                        st.write(
                            "**Condition:**",
                            item["condition_name"]
                        )

                        st.write(
                            "**Notes:**",
                            item["notes"] or "No notes"
                        )

                        st.divider()

                else:
                    st.info(
                        "No medical history recorded."
                    )

    else:
        st.info("Register a demo patient first.")


# ---------------------------------
# PRESCRIPTION REVIEW
# ---------------------------------


elif page == "Medication Management":
    st.header("Medication Management")

    st.caption("Synthetic medication catalog")

    with st.form("medication_form"):
        generic_name = st.text_input("Generic Name")
        display_name = st.text_input("Display Name")

        submitted = st.form_submit_button("Add Medication")

        if submitted:
            if not generic_name.strip() or not display_name.strip():
                st.error("Both fields are required.")

            else:
                existing_medications = get_all_medications()

                duplicate = any(
                    medication[1].casefold() == generic_name.strip().casefold()
                    for medication in existing_medications
                )

                if duplicate:
                    st.warning("This medication already exists.")

                else:
                    try:
                        create_medication(
                            generic_name.strip(),
                            display_name.strip(),
                            "synthetic"
                        )

                        st.success("Synthetic medication added.")
                        st.rerun()

                    except Exception as error:
                        st.error(f"Error: {error}")

    st.divider()

    st.subheader("Medication Catalog")

    medications = get_all_medications()

    if medications:
        for medication in medications:
            with st.container(border=True):
                st.write(f"**{medication[2]}**")
                st.caption(f"Code: {medication[1]}")
                st.caption(f"Source: {medication[3]}")
    else:
        st.info("No medications registered yet.")


elif page == "Prescription Review":

    st.header("Prescription Review")

    st.warning(
        "The experimental review engine "
        "has not been implemented yet."
    )
