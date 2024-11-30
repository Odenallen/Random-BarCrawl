import numpy as np
import os

def check_bar_co_presence(people, names, bar_dict):
    # Create a dictionary to track who is at each bar at each time step
    bar_presence = {}
    
    # Open a log file to write bar presence details
    with open('bar_presence_log.txt', 'w') as log_file:
        # Write header
        log_file.write("Bar Presence Log\n")
        log_file.write("================\n\n")
        
        # Iterate through each time step (0 to 5)
        for time_step in range(6):
            bar_presence[time_step] = {}
            
            log_file.write(f"Time Step {time_step + 1}:\n")
            
            # Check which bars people are at for this time step
            for i, person_bars in enumerate(people):
                current_bar = bar_dict.get(person_bars[time_step], f"Unknown Bar {person_bars[time_step]}")
                
                if current_bar not in bar_presence[time_step]:
                    bar_presence[time_step][current_bar] = []
                
                bar_presence[time_step][current_bar].append(names[i])
            
            # Write bar occupancy for this time step
            for bar, occupants in bar_presence[time_step].items():
                log_file.write(f"{bar}: {', '.join(occupants)} ({len(occupants)} people)\n")
            
            log_file.write("\n")
        
        # Check for bars with only one person at each time step
        solitary_bars = []
        for time_step, bars in bar_presence.items():
            for bar, occupants in bars.items():
                if len(occupants) == 1:
                    solitary_bars.append((time_step, bar, occupants[0]))
        
        # Log solitary bars
        if solitary_bars:
            log_file.write("Solitary Bars (only one person):\n")
            for time_step, bar, person in solitary_bars:
                log_file.write(f"Time Step {time_step + 1}: {bar} - only {person}\n")
        else:
            log_file.write("No solitary bars found!\n")
    
    return bar_presence

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

    # Check bar co-presence and log details
    bar_presence = check_bar_co_presence(people, names, bar_dict)

    # Save bar lists for each name
    for i, name in enumerate(names):
        # Map bar numbers to bar names
        bar_names = [bar_dict.get(bar, f"Unknown Bar {bar}") for bar in people[i,:]]
        
        # Create filename
        filename = os.path.join(lists_folder, f"{name}.txt")
        
        # Write bar names to file
        with open(filename, 'w') as f:
            for bar in bar_names:
                f.write(f"{bar}\n")
        
        # print(f"Created {filename}")

    print("\nBar presence log has been written to 'bar_presence_log.txt'")

main()