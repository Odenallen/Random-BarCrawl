import numpy as np
import os
def check_bar_distribution(people, bar_dict):
    # Count how many times each bar is visited
    bar_counts = {}
    for row in people:
        for bar in row:
            bar_name = bar_dict.get(bar, f"Unknown Bar {bar}")
            bar_counts[bar_name] = bar_counts.get(bar_name, 0) + 1
    
    # Check for bars with only one person
    solitary_bars = [bar for bar, count in bar_counts.items() if count == 1]
    
    print("\nBar Distribution Analysis:")
    for bar, count in bar_counts.items():
        print(f"{bar}: {count} people")
    
    print("\nSolitary Bars:")
    for bar in solitary_bars:
        print(bar)
    
    return len(solitary_bars)
def save_round_information(eventList: list[dict[str, list[str]]], filename: str = "round_information.txt"):
    """
    Save all round information to a text file with formatted output
    """
    with open(filename, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("BAR CRAWL EVENT - ROUND ASSIGNMENTS\n")
        f.write("=" * 60 + "\n\n")
        
        for idx, round_dict in enumerate(eventList):
            f.write(f"\n{'=' * 60}\n")
            f.write(f"ROUND {idx + 1}\n")
            f.write(f"{'=' * 60}\n\n")
            
            for bar_name, participants in round_dict.items():
                f.write(f"{bar_name}:\n")
                f.write(f"  Capacity: {len(participants)} people\n")
                f.write(f"  Participants:\n")
                
                if participants:
                    for participant in participants:
                        f.write(f"    - {participant}\n")
                else:
                    f.write(f"    (No participants assigned)\n")
                
                f.write("\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("END OF ROUND INFORMATION\n")
        f.write("=" * 60 + "\n")
    
    print(f"\nRound information saved to {filename}")

def pretty_printing(eventList: list[dict[str, list[str]]]):
    """
    Print round information to console (original function preserved)
    """
    for idx, round_dict in enumerate(eventList):
        print(f"\nRound {idx+1}:")
        print("-" * 40)
        for bar_name, participants in round_dict.items():
            print(f"{bar_name}: {len(participants)} people")
            print(f"  {participants}")




def main():
    # Create lists folder if it doesn't exist
    lists_folder = 'lists'
    os.makedirs(lists_folder, exist_ok=True)
    
    f = open("barlist.txt", "r")
    bar_list = f.read().splitlines()
    f.close()

    f = open("people.txt", "r")
    names = f.read().splitlines()
    numb_names = len(names)
    f.close()

    # Create bar dictionary with offset
    bar_dict = {i+1: bar for i, bar in enumerate(bar_list)}
    bar_par_dict_round = {bar: [] for i, bar in enumerate(bar_list)}
    list = np.array([1,2,3,4,5,6])
    # bar_par_dict_event =  [bar_par_dict_round for num in list]
    bar_par_dict_event = [{bar: [] for bar in bar_list} for _ in range(6)]
    people = np.zeros([numb_names,6], dtype=int)
    people[0,:] = list
    
    unique_rows = set([tuple(list)])
    
    for i in range(1, numb_names):
        while True:
            shuffled = np.random.permutation(list)
            shuffled_tuple = tuple(shuffled)

        
            if shuffled_tuple not in unique_rows:
                people[i,:] = shuffled
                unique_rows.add(shuffled_tuple)
                break
    
    print("Unique rows confirmed:", len(unique_rows) == numb_names)
    # Save bar lists for each name
    barDict = {}

    for i, name in enumerate(names):
        # Map bar numbers to bar names
        bar_names = [bar_dict.get(bar, f"Unknown Bar {bar}") for bar in people[i,:]]
        [ bar_par_dict_event[idx][bar].append(name) for idx,bar in enumerate(bar_names)]
        
        
        # Create filename
        filename = os.path.join(lists_folder, f"{name}.txt")
        
        # Write bar names to file
        with open(filename, 'w') as f:
            for bar in bar_names:
                f.write(f"{bar}\n")
        
        print(f"Created {filename}")

    solitary_bar_count = check_bar_distribution(people, bar_dict)
    
    if solitary_bar_count > 0:
        print(f"\nWarning: {solitary_bar_count} bars have only one person!")
    else:
        print("\nGood distribution: No solitary bars found.")
    
    # pretty_printing(bar_par_dict_event)
    save_round_information(bar_par_dict_event)



main()