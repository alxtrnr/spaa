# result_viewer.py

import pulp
from tabulate import tabulate
import csv


def get_staff_assignments(staff, observations, assignments):
    assignments_dict = {}
    for o in observations:
        for t in range(12):
            staff_assigned = [s["name"] for s in staff if assignments[(s["id"], o["id"], t)].value() == 1]
            assignments_dict[(o["name"], t)] = staff_assigned
    return assignments_dict


def export_to_csv(data, headers, filename, index=None):
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        if index:
            writer.writerow([""] + index)
        for i, row in enumerate(data):
            if index:
                writer.writerow([i] + row)
            else:
                writer.writerow(row)


def print_results(staff, observations, assignments, shift):
    index = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
             '19:00'] if shift == 'd' else ['20:00', '21:00', '22:00', '23:00', '00:00', '01:00', '02:00', '03:00',
                                            '04:00', '05:00', '06:00', '07:00']
    observations_names = [o["name"] for o in observations]
    assignments_dict = get_staff_assignments(staff, observations, assignments)
    headers = ["OBS"] + observations_names
    data = [[", ".join(assignments_dict[(o_name, t)]) for o_name in observations_names] for t in range(12)]
    filename = "table.csv"
    export_to_csv(data, headers, filename, index=index)
    print(tabulate(data, headers=headers, showindex=index, tablefmt="fancy_grid"))

    # Print the assignments
    schedule = [["OFF" for _ in staff] for _ in range(12)]
    assignments_count = [0] * len(staff)  # initialize a list to store the number of assignments for each staff member

    for t in range(12):
        for i, s in enumerate(staff):
            for o in observations:
                if assignments[(s["id"], o["id"], t)].value() == 1:
                    schedule[t][i] = o["name"]
                    assignments_count[
                        i] += 1  # increment the assignment count for the staff member whose column the cell is in

    # Add a row at the bottom of the schedule matrix to display the assignment count for each staff member
    assignments_row = [str(count) for count in assignments_count]
    schedule.append(assignments_row)
    index.append("TOTAL")

    headers = ["TIME"] + [s["name"] for s in staff]
    print(tabulate(schedule, headers=headers, showindex=index, tablefmt="fancy_grid"))

    # Print the assignments
    for s in staff:
        print(f"\nAllocations for {s['name']}:")
        for o in observations:
            for t in range(12):
                if assignments[(s["id"], o["id"], t)].value() == 1:
                    print(f"{s['name']} allocated to {o['name']} at time {t}")
