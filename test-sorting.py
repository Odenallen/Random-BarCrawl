from collections import defaultdict
import pulp

def solve_with_pulp(participants, venues, venue_constraints):
    """
    Use PuLP (integer programming) to solve this properly.
    """
    
    
    num_rounds = len(venues)
    
    # Create the problem
    prob = pulp.LpProblem("PubCrawl", pulp.LpMinimize)
    
    # Decision variables: x[p][v][r] = 1 if participant p visits venue v in round r
    x = {}
    for p in participants:
        for v in venues:
            for r in range(1, num_rounds + 1):
                x[(p, v, r)] = pulp.LpVariable(f"x_{p}_{v}_{r}", cat='Binary')
    
    # Objective: doesn't matter, just find feasible solution
    prob += 0
    
    # Constraint 1: Each participant visits each venue exactly once
    for p in participants:
        for v in venues:
            prob += pulp.lpSum([x[(p, v, r)] for r in range(1, num_rounds + 1)]) == 1
    
    # Constraint 2: Each participant visits exactly one venue per round
    for p in participants:
        for r in range(1, num_rounds + 1):
            prob += pulp.lpSum([x[(p, v, r)] for v in venues]) == 1
    
    # Constraint 3: Venue capacity constraints per round
    for v in venues:
        min_cap = venue_constraints[v]['min']
        max_cap = venue_constraints[v]['max']
        
        for r in range(1, num_rounds + 1):
            count = pulp.lpSum([x[(p, v, r)] for p in participants])
            prob += count >= min_cap
            prob += count <= max_cap
    
    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    # Check if solution found
    if prob.status != pulp.LpStatusOptimal:
        return None, f"No feasible solution found. Status: {pulp.LpStatus[prob.status]}"
    
    # Extract solution
    assignments = {}
    for p in participants:
        crawl = [None] * num_rounds
        for v in venues:
            for r in range(1, num_rounds + 1):
                if pulp.value(x[(p, v, r)]) > 0.5:  # Binary variable is 1
                    crawl[r - 1] = v
        assignments[p] = crawl
    
    return assignments, "Success"


def validate_solution(assignments, venue_constraints):
    """Validates the solution"""
    if not assignments:
        return False, "No assignments"
    
    num_rounds = len(list(assignments.values())[0])
    
    # Check each round
    for round_num in range(num_rounds):
        venue_counts = defaultdict(int)
        
        for participant, crawl in assignments.items():
            venue = crawl[round_num]
            venue_counts[venue] += 1
        
        # Check constraints
        for venue, count in venue_counts.items():
            min_cap = venue_constraints[venue]['min']
            max_cap = venue_constraints[venue]['max']
            
            if count < min_cap:
                return False, f"Round {round_num + 1}: {venue} has {count} (min {min_cap})"
            if count > max_cap:
                return False, f"Round {round_num + 1}: {venue} has {count} (max {max_cap})"
    
    # Check each participant
    for participant, crawl in assignments.items():
        if len(crawl) != len(set(crawl)):
            return False, f"{participant} visits venue twice"
        if set(crawl) != set(venue_constraints.keys()):
            return False, f"{participant} doesn't visit all venues"
    
    return True, "Valid"


def print_solution(assignments, venue_constraints):
    """Pretty print the solution"""
    if not assignments:
        return
    
    num_rounds = len(list(assignments.values())[0])
    
    print("\nPub Crawl Assignments:")
    print("-" * 60)
    for participant, crawl in sorted(assignments.items()):
        print(f"{participant:12s}: {' → '.join(crawl)}")
    
    print("\nRound-by-Round View:")
    print("-" * 60)
    for round_num in range(num_rounds):
        print(f"\nRound {round_num + 1}:")
        venue_assignments = defaultdict(list)
        
        for participant, crawl in assignments.items():
            venue_assignments[crawl[round_num]].append(participant)
        
        for venue in sorted(venue_assignments.keys()):
            people = venue_assignments[venue]
            constraints = venue_constraints[venue]
            print(f"  {venue:12s}: {', '.join(sorted(people)):30s} "
                  f"({len(people)} people, min={constraints['min']}, max={constraints['max']})")


if __name__ == "__main__":
    # print("=" * 60)
    # print("Test 1: Simple 3x3 case")
    # print("=" * 60)
    
    # participants = ["Alice", "Bob", "Charlie"]
    # venues = ["Bar", "Pub", "Club"]
    # venue_constraints = {
    #     "Bar": {"min": 1, "max": 2},
    #     "Pub": {"min": 1, "max": 2},
    #     "Club": {"min": 1, "max": 2}
    # }
    
    # # assignments, status = solve_pubcrawl(participants, venues, venue_constraints)
    # assignments, status = solve_with_pulp(participants, venues, venue_constraints)
    # print(f"\nStatus: {status}")
    
    # if assignments:
    #     print_solution(assignments, venue_constraints)
    #     is_valid, msg = validate_solution(assignments, venue_constraints)
    #     print(f"\nValidation: {msg}")
    
    # print("\n" + "=" * 60)
    # print("Test 2: Larger case")
    # print("=" * 60)
    
    # participants2 = ["Alice", "Bob", "Charlie", "David", "Eve"]
    # venues2 = ["Bar", "Pub", "Club", "Lounge"]
    # venue_constraints2 = {
    #     "Bar": {"min": 1, "max": 3},
    #     "Pub": {"min": 1, "max": 2},
    #     "Club": {"min": 1, "max": 2},
    #     "Lounge": {"min": 1, "max": 3}
    # }
    
    # assignments2, status2 = solve_with_pulp(participants2, venues2, venue_constraints2)
    # print(f"\nStatus: {status2}")
    
    # if assignments2:
    #     print_solution(assignments2, venue_constraints2)
    #     is_valid, msg = validate_solution(assignments2, venue_constraints2)
    #     print(f"\nValidation: {msg}")
    
    # print("\n" + "=" * 60)
    # print("Test 3: Impossible constraints")
    # print("=" * 60)
    
    # participants3 = ["Alice", "Bob"]
    # venues3 = ["Bar", "Pub", "Club"]
    # venue_constraints3 = {
    #     "Bar": {"min": 2, "max": 2},
    #     "Pub": {"min": 2, "max": 2},
    #     "Club": {"min": 2, "max": 2}
    # }
    
    # assignments3, status3 = solve_with_pulp(participants3, venues3, venue_constraints3)
    # print(f"\nStatus: {status3}")


    print("\n" + "=" * 60)
    print("Test 4: Old Barcrawl")
    print("=" * 60)
    
    import os


    cwd = os.getcwd()
    path1= os.path.join(cwd,"people.txt")
    parti = []
    with open(path1,'r') as f:
        for row in f.readlines():
            parti.append(row.strip())

    path2 = os.path.join(cwd,"barlist.txt")
    venus = []
    with open(path2,'r') as f:
        for row in f.readlines():
            venus.append(row.strip())



    constraints  = {v: {"min": 2, "max": 8} for v in venus}
    

    assignments4, status4 = solve_with_pulp(parti,venus,constraints)
    print(f"\nStatus: {status4}")

    if assignments4:
        print_solution(assignments4, constraints)
        is_valid, msg = validate_solution(assignments4, constraints)
        print(f"\nValidation: {msg}")
    

