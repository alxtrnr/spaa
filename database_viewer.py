from sqlalchemy import create_engine
import pandas as pd
from database_creation import StaffTable, ObservationsTable
from sqlalchemy.orm import sessionmaker

# Create an engine to carry on with the table. This is the SQLite engine.
engine = create_engine(f'sqlite:///allocations_db/test.db', echo=False)

# Construct a sessionmaker object and bind it to the engine
Session = sessionmaker(bind=engine)
session = Session()


def display_staff():
    # Query the staff table
    conn = engine.connect()
    staff_data = pd.read_sql_query(session.query(StaffTable).statement, conn)

    # Display the staff data in a tabular format
    print(staff_data)


def display_patients():
    # Query the patient table
    conn = engine.connect()
    patient_data = pd.read_sql_query(session.query(ObservationsTable).statement, conn)

    # Display the patient data in a tabular format
    print(patient_data)


""""
You can create a session and call the display_staff() and display_patients() functions in another module or the main
program. For example:

from database_viewer import display_staff, display_patients

# Create a session and display staff and patient data
session = Session()
display_staff()
display_patients()

# Close the session
session.close()
"""
