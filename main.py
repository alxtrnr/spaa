from database_operations import add_patient, add_staff, assign_on_obs, update_patient, update_staff, delete_patient, \
    delete_staff
from database_viewer import display_patients, display_staff

print('Welcome to the Staff / Patient Allocation App (SPAA)')


def menu():
    print("""
    1. Add Patient
    2. Add Staff

    3. Update Patient
    4. Update Staff

    5. Delete Patient
    6. Delete Staff

    7. Display Patient
    8. Display Staff
    
    9.  Select staff to put on obs
    10. Allocate patient obs
    """)

    choice = input('Selection: ')

    if choice == '1':
        add_patient()
    elif choice == '2':
        add_staff()
    elif choice == '3':
        update_patient()
    elif choice == '4':
        update_staff()
    elif choice == '5':
        delete_patient()
    elif choice == '6':
        delete_staff()
    elif choice == '7':
        display_patients()
    elif choice == '8':
        display_staff()
    elif choice == '9':
        assign_on_obs()
    elif choice == '10':
        import milo_solve


if __name__ == "__main__":
    while True:
        menu()
