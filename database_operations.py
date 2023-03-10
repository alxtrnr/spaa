# database_operations.py

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_creation import StaffTable, ObservationsTable

# Create an engine to carry on with the table. This is the SQLite engine.
engine = create_engine('sqlite:///allocations_db/test.db')

# Construct a sessionmaker object and bind it to the engine
Session = sessionmaker(bind=engine)
session = Session()


@click.group()
def cli():
    pass


@click.command()
def add_staff():
    name = input("Enter staff name: ").title()
    role = input("Enter staff role: ").upper()
    gender = input("Enter staff gender (m/f): ").upper()

    staff = StaffTable(
        name=name,
        role=role,
        gender=gender,
        assigned=False,
        start_time=0,
        end_time=12,
        duration=12
    )

    session.add(staff)
    session.commit()
    click.echo("Staff added successfully.")


@click.command()
def add_patient():
    name = input("Enter patient name: ").title()
    observation_level = int(input("Enter patient observation level: "))
    room_number = input("Enter patient room number: ")
    gender_req = input("Enter staff gender required for obs m/f (press enter for any gender): ").upper()

    patient = ObservationsTable(
        name=name,
        observation_level=observation_level,
        room_number=room_number,
        gender_req=gender_req
    )

    session.add(patient)
    session.commit()
    click.echo("Patient added successfully.")


@click.command()
def update_staff():
    staff_id = input("Enter staff ID to update: ")
    staff = session.query(StaffTable).filter_by(id=staff_id).first()

    if staff is not None:
        staff.name = input("Enter staff name (press enter to keep existing name): ").upper() or staff.name
        staff.role = input("Enter staff role (press enter to keep existing role): ") or staff.role
        staff.gender = input("Enter staff gender (press enter to keep existing gender): ").upper() or staff.gender

        obs_assign = input("Enter any key to assign for obs (press enter for no obs): ")
        staff.assigned = bool(obs_assign) or staff.assigned is False

        st = input("Enter staff start time (HH:MM) (press enter for a full shift): ")
        et = input("Enter staff end time (HH:MM) (press enter for a full shift): ")
        day_converter = {'08:00': 0,
                         '09:00': 1,
                         '10:00': 2,
                         '11:00': 3,
                         '12:00': 4,
                         '13:00': 5,
                         '14:00': 6,
                         '15:00': 7,
                         '16:00': 8,
                         '17:00': 9,
                         '18:00': 10,
                         '19:00': 11
                         }
        night_converter = {'20:00': 0,
                           '21:00': 1,
                           '22:00': 2,
                           '23:00': 3,
                           '00:00': 4,
                           '01:00': 5,
                           '02:00': 6,
                           '03:00': 7,
                           '04:00': 8,
                           '05:00': 9,
                           '06:00': 10,
                           '07:00': 11
                           }
        if st in day_converter.keys():
            staff.start_time = day_converter[st]
            staff.end_time = day_converter[et]
        elif st in night_converter.keys():
            staff.start_time = night_converter[st]
            staff.end_time = night_converter[et]
        else:
            staff.start_time = 0
            staff.end_time = 12
        staff.duration = staff.end_time - staff.start_time

        session.commit()
        click.echo("Staff updated successfully.")
    else:
        click.echo("Staff not found.")


@click.command()
def update_patient():
    # Prompt user to enter the patient ID to update
    patient_id = input("Enter patient ID to update: ")

    # Retrieve the patient with the given ID from the database
    patient = session.query(ObservationsTable).filter_by(id=patient_id).first()

    # If the patient is found in the database
    if patient:
        # Prompt user to enter the patient name, observation level, and room number
        patient.name = input(f"Enter patient name (press enter to keep as {patient.name}): ").title() or patient.name
        patient.observation_level = int(input(
            f"Enter patient obs level (press enter to keep as {patient.observation_level}): "))
        patient.room_number = input(
            "Enter patient room number (press enter to keep existing number): ") or patient.room_number
        patient.gender_req = input(
            "Enter any gender req m/f (press enter to clear all req): ").upper()
        # Prompt user to enter the staff ID to add or remove from the patient's omit list
        staff_id = input("Enter staff ID to add or remove from omit list (press enter to keep existing status): ")

        # If the staff ID is provided
        if staff_id:
            # Retrieve the staff with the given ID from the database
            staff = session.query(StaffTable).filter_by(id=staff_id).first()

            # If the staff is found in the database
            if staff:
                # If the staff name is already in the omit list, remove it
                if staff.name in patient.omit_staff:
                    patient.omit_staff.remove(staff.name)
                    click.echo(f"Staff {staff.name} removed from omit list for patient {patient.name}.")
                else:
                    # Otherwise, add the staff name to the omit list
                    patient.omit_staff.append(staff.name)
                    click.echo(f"Staff {staff.name} added to omit list for patient {patient.name}.")

                session.commit()  # Save the changes to the database
            else:
                click.echo("Staff not found.")
        else:
            session.commit()  # Save the changes to the database
            click.echo("Patient updated successfully.")
    else:
        click.echo("Patient not found.")


@click.command()
def delete_staff():
    staff_id = input("Enter staff ID to delete: ")
    staff = session.query(StaffTable).filter_by(id=staff_id).first()

    if staff is not None:
        session.delete(staff)
        session.commit()
        click.echo("Staff deleted successfully.")
    else:
        click.echo("Staff not found.")


@click.command()
def delete_patient():
    patient_id = input("Enter patient ID to delete: ")
    patient = session.query(ObservationsTable).filter_by(id=patient_id).first()

    if patient is not None:
        session.delete(patient)
        session.commit()
        click.echo("Patient deleted successfully.")
    else:
        click.echo("Patient not found.")


@click.command()
def assign_on_obs():
    staff_id = input("Enter staff ID to assign on obs: ")
    staff = session.query(StaffTable).filter_by(id=staff_id).first()

    if staff is not None:
        obs_assign = input(f"Enter any key to assign to obs (press enter to keep existing status): ")
        staff.assigned = bool(obs_assign) or staff.assigned
        session.commit()
        click.echo(f"{staff.name} assigned to obs successfully.")
    else:
        click.echo("Staff not found.")


@click.command()
def view_staff():
    staff_list = session.query(StaffTable).all()
    if staff_list:
        click.echo("\n".join([f"{staff.id} {staff.name} ({staff.role})" for staff in staff_list]))
    else:
        click.echo("No staff found.")


@click.command()
def view_patients():
    patient_list = session.query(ObservationsTable).all()
    if patient_list:
        for patient in patient_list:
            omit_staff_str = ", ".join(patient.omit_staff) or "None"
            click.echo(
                f"{patient.id} {patient.name} (Observation level: {patient.observation_level}, Room number: {patient.room_number}, Gender requirement: {patient.gender_req}, Staff to omit: {omit_staff_str})")
    else:
        click.echo("No patients found.")


cli.add_command(add_staff)
cli.add_command(add_patient)
cli.add_command(update_staff)
cli.add_command(update_patient)
cli.add_command(delete_staff)
cli.add_command(delete_patient)
cli.add_command(assign_on_obs)
cli.add_command(view_staff)
cli.add_command(view_patients)
