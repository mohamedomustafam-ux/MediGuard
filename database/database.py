
import sqlite3
from pathlib import Path

# Database location
DB_PATH = Path(__file__).resolve().parent / "mediguard.db"


def get_connection():
    """Create a database connection."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    """Create all MediGuard database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # 1. Patients
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_code TEXT UNIQUE NOT NULL,
            age INTEGER CHECK(age BETWEEN 0 AND 120),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Medical History
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            condition_name TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (patient_id)
                REFERENCES patients(id)
        )
    """)

    # 3. Medications
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generic_name TEXT NOT NULL,
            display_name TEXT,
            data_source TEXT
        )
    """)

    # 4. Prescriptions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id)
                REFERENCES patients(id)
        )
    """)

    # 5. Prescription Items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescription_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prescription_id INTEGER NOT NULL,
            medication_id INTEGER NOT NULL,
            dose_text TEXT,
            frequency TEXT,
            duration_days INTEGER,
            FOREIGN KEY (prescription_id)
                REFERENCES prescriptions(id),
            FOREIGN KEY (medication_id)
                REFERENCES medications(id)
        )
    """)

    # 6. Safety Alerts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS safety_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prescription_item_id INTEGER,
            severity TEXT CHECK(
                severity IN ('yellow', 'red')
            ),
            alert_message TEXT NOT NULL,
            explanation TEXT,
            source_reference TEXT,
            review_status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prescription_item_id)
                REFERENCES prescription_items(id)
        )
    """)

    connection.commit()
    connection.close()

    print("MediGuard database initialized successfully!")


if __name__ == "__main__":
    init_db()


def create_patient(patient_code, age, condition_name=None, notes=None):
    """Save a synthetic patient and optional medical history."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO patients (patient_code, age)
            VALUES (?, ?)
        """, (patient_code, age))

        patient_id = cursor.lastrowid

        if condition_name and condition_name.strip():
            cursor.execute("""
                INSERT INTO medical_history
                (patient_id, condition_name, notes)
                VALUES (?, ?, ?)
            """, (
                patient_id,
                condition_name.strip(),
                notes
            ))

        connection.commit()
        return patient_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_all_patients():
    """Retrieve all synthetic patients."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, patient_code, age, created_at
            FROM patients
            ORDER BY id DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_patient(patient_id):
    """Retrieve one patient by database ID."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, patient_code, age, created_at
            FROM patients
            WHERE id = ?
        """, (patient_id,))

        result = cursor.fetchone()

        return dict(result) if result else None

    finally:
        connection.close()


def get_patient_history(patient_id):
    """Retrieve the patient's synthetic medical history."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT condition_name, notes
            FROM medical_history
            WHERE patient_id = ?
            ORDER BY id DESC
        """, (patient_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()
