import pulp
from milo_input_data import get_staff_rows_as_dict, get_patient_rows_as_dict
from result_viewer import print_results

# Define input data
staff = get_staff_rows_as_dict()
observations = get_patient_rows_as_dict()

# Create a new optimization problem
problem = pulp.LpProblem("Staff_Observation_Assignment_Problem", pulp.LpMinimize)

# Define the decision variables
assignments = pulp.LpVariable.dicts("Assignments",
                                    ((s["id"], o["id"], t) for s in staff for o in observations for t in range(12)),
                                    cat="Binary")

# Patients whose observation level == 0 may be ignored
for o in observations:
    if o["observation_level"] == 0:
        for s in staff:
            for t in range(12):
                problem += assignments[(s["id"], o["id"],
                                        t)] == 0, f"Ignore Observation (observation {o['id']}, staff {s['id']}, time {t}) Constraint"

# Patients whose observation level == 1 must be assigned 1 staff for each time
for o in observations:
    if o["observation_level"] == 1:
        for t in range(12):
            problem += pulp.lpSum([assignments[(s["id"], o["id"], t)] for s in
                                   staff]) == 1, f"Observation Level 1 (observation {o['id']}, time {t}) Constraint"

# Patients whose observation level == 2 must be assigned 2 staff for each time
for o in observations:
    if o["observation_level"] == 2:
        for t in range(12):
            problem += pulp.lpSum([assignments[(s["id"], o["id"], t)] for s in
                                   staff]) == 2, f"Observation Level 2 (observation {o['id']}, time {t}) Constraint"

# Patients whose observation level == 3 must be assigned 3 staff for each time
for o in observations:
    if o["observation_level"] == 3:
        for t in range(12):
            problem += pulp.lpSum([assignments[(s["id"], o["id"], t)] for s in
                                   staff]) == 3, f"Observation Level 3 (observation {o['id']}, time {t}) Constraint"

# Patients whose observation level == 4 must be assigned 4 staff for each time
for o in observations:
    if o["observation_level"] == 4:
        for t in range(12):
            problem += pulp.lpSum([assignments[(s["id"], o["id"], t)] for s in
                                   staff]) == 4, f"Observation Level 4 (observation {o['id']}, time {t}) Constraint"

# If gender_req == M staff whose gender == F must not be assigned any time for that patient
# If gender_req == F staff whose gender == M must not be assigned any time for that patient
for o in observations:
    for s in staff:
        if (o["gender_req"] == "M" and s["gender"] == "F") or (o["gender_req"] == "F" and s["gender"] == "M"):
            for t in range(12):
                problem += assignments[(s["id"], o["id"],
                                        t)] == 0, f"Gender Constraint (observation {o['id']}, staff {s['id']}, time {t}) Constraint"

# Ignore staff with assigned=False
for s in staff:
    if not s["assigned"]:
        for t in range(12):
            for o in observations:
                problem += assignments[(
                    s["id"], o["id"], t)] == 0, f"Unassigned_Staff_(staff_{s['id']})_Constraint_o={o['id']}_t={t}"

# Staff must only be assigned from their start_time to end_time
for s in staff:
    for t in range(12):
        if t < s["start_time"] or t >= s["end_time"]:
            for o in observations:
                problem += assignments[(s["id"], o["id"],
                                        t)] == 0, f"Staff_Time_Availability_(staff_{s['id']},_observation_{o['id']},_time_{t})_Constraint"

# Ensure each staff member is not assigned to an observation for more than 2 consecutive hours
for s in staff:
    for t in range(11):
        if s["assigned"] and s["start_time"] <= t < s["end_time"] - 1:
            problem += pulp.lpSum([assignments[(s["id"], o["id"], t_prime)] for o in observations for t_prime in
                                   range(max(0, t - 1),
                                         t + 2)]) <= 2, f"Consecutive Hours (staff {s['id']}, time {t}) Constraint"

# Staff whose duration is < 12 must have >= 1 unassigned time slot between their start_time + 4 and end_time
for s in staff:
    if s["duration"] < 12:
        for t in range(s["start_time"] + 4, s["end_time"]):
            problem += pulp.lpSum([assignments[(s["id"], o["id"], t_prime)] for o in observations for t_prime in
                                   range(t - 1, t + 1)]) <= 1, f"Minimum Break (staff {s['id']}, time {t}) Constraint"

# Staff whose duration is >= 12 must have >= 2 unassigned time slots between 5 and 11
for s in staff:
    if s["duration"] >= 12:
        problem += pulp.lpSum([assignments[(s["id"], o["id"], t)] for o in observations for t in range(5, 12)]) <= 5, \
            f"Break Constraint (staff {s['id']}) Constraint"

# Add the objective function to the problem
problem += pulp.lpSum([1 - assignments[(s["id"], o["id"], t)] for o in observations for t in range(12) for s in staff if
                       s["assigned"] and s["start_time"] <= t < s[
                           "end_time"]]), "Minimize Unassigned Observations"

# Solve the problem
problem.solve()

# Print the status of the solution
print("Status:", pulp.LpStatus[problem.status])
if pulp.LpStatus[problem.status] == 'Infeasible':
    exit('You need more staff!')

shift = input('\nCreate allocations for d/n shift: \n')

# Call the print_results function to print the table of staff assignments
print_results(staff, observations, assignments, shift)
