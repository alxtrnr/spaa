import pulp
from tabulate import tabulate

def print_results(staff, observations, assignments, shift):
    # Create an empty dictionary to store the staff assignments
    assignments_dict = {}

    index = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'] if shift == 'd' else ['20:00', '21:00', '22:00', '23:00', '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00']

    # Loop over each observation
    for o in observations:
        # Loop over each time slot
        for t in range(12):
            # Get the staff assigned to this observation and time slot
            staff_assigned = [s["name"] for s in staff if assignments[(s["id"], o["id"], t)].value() == 1]
            # Add the staff assignments to the dictionary
            assignments_dict[(o["name"], t)] = staff_assigned

    # Create a list of headers for the table
    headers = ["OBS ==>"] + [o["name"] for o in observations]

    # Create a list of rows for the table
    rows = []
    for t in range(12):
        # Create a list of cells for this row
        row = [", ".join(assignments_dict[(o["name"], t)]) for o in observations]
        # Add the row to the list of rows
        rows.append(row)

    # Print the table
    print(tabulate(rows, headers=headers, showindex=index, tablefmt="fancy_grid"))

    # Get a list of assigned patients for each staff member at each time slot
    schedule = [["OFF" for s in staff] for t in range(12)]
    for s in staff:
        for t in range(12):
            for o in observations:
                if assignments[(s["id"], o["id"], t)].value() == 1:
                    schedule[t][s["id"] - 1] = o["name"]

    # Display the schedule
    print(tabulate(schedule, headers=["STAFF ==>"] + [s["name"] for s in staff], showindex=[t for t in index], tablefmt="fancy_grid"))

    # Print the assignments
    for s in staff:
        for o in observations:
            for t in range(12):
                if assignments[(s["id"], o["id"], t)].value() == 1:
                    print(f"Staff {s['name']} assigned to Observation {o['name']} at time {t}")