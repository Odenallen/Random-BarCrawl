import numpy as np
import os
from collections import defaultdict

def check_bar_co_occupancy(people, names, bar_dict):
    # Create a dictionary to track who is at each bar
    bar_occupancy = defaultdict(list)
    
    # Iterate through each person's bar list
    for i, row in enumerate(people):
        # For each bar in the person's list
        for bar_num in row:
            bar_name = bar_dict.get(bar_num, f"Unknown Bar {bar_num}")
            bar_occupancy[bar_name].append(names[i])
    
    # Check and print co-occupancy
    co_occupied_bars = {}
    for bar, occupants in bar_occupancy.items():
        if len(occupants) > 1:
            co_occupied_bars[bar] = occupants
    
    # Print results
    print("\nBar Co-Occupancy Analysis:")
    if co_occupied_bars:
        print("Bars with multiple people:")
        for bar, occupants in co_occupied_bars.items():
            print(f"{bar}: {', '.join(occupants)}")
        print(f"\nTotal bars with multiple people: {len(co_occupied_bars)}")
    else:
        print("No bars have multiple people at the same time.")
    
    return co_occupied_bars

def main():
    # Create lists folder if it doesn't exist
    lists_folder = 'lists'
    os.makedirs(lists_folder, exist_ok=True)
    
    # Read bar list
    with open("barlist.txt", "r") as f:
        bar_list = f.read().splitlines()

    # Read names
    with open("people.txt", "r") as f:
        names = f.read().splitlines()
    numb_names = len(names)

    # Create bar dictionary with offset
    bar_dict = {i+1: bar for i, bar in enumerate(bar_list)}

    # Initial bar distribution setup
    list_base = np.array([1,2,3,4,5,6])

    people = np.zeros([numb_names,6], dtype=int)
    people[0,:] = list_base
    
    unique_rows = set([tuple(list_base)])
    
    # Generate unique bar distributions
    for i in range(1, numb_names):
        while True:
            shuffled = np.random.permutation(list_base)
            shuffled_tuple = tuple(shuffled)
            
            if shuffled_tuple not in unique_rows:
                people[i,:] = shuffled
                unique_rows.add(shuffled_tuple)
                break
    
    print("Unique rows confirmed:", len(unique_rows) == numb_names)

    # Check bar co-occupancy
    co_occupied_bars = check_bar_co_occupancy(people, names, bar_dict)
    # print(co_occupied_bars)
    # Save bar lists for each name
    for i, name in enumerate(names):
        # Map bar numbers to bar names
        bar_names = [bar_dict.get(bar, f"Unknown Bar {bar}") for bar in people[i,:]]
        
        # Create filename
        filename = os.path.join(lists_folder, f"{name}.txt")
        
        # # Write bar names to file
        # with open(filename, 'w') as f:
        #     for bar in bar_names:
        #         f.write(f"{bar}\n")
        
        # print(f"Created {filename}")

main()