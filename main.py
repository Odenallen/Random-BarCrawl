import numpy as np


class attendee:
    def __init__(self,name) -> None:
        self.name = name
        self.prev_bar = []
        self.chosen = False

    
        
    def __repr__(self) -> str:
        # return f"{self.name} has been to {self.prev_bar}"
        return f"{self.name}"
        
    def beenAtBar(self, bar):
        # if not bar in self.prev_bar or not self.chosen:
        if not bar in self.prev_bar:
            return True
        else:
            return False

    def addToBar(self,bar)-> None:
        self.prev_bar.append(bar)
        
    def barList(self):
        return self.prev_bar
class bar:
    def __init__(self,name,occupancy=6) -> None:
        self.name = name
        self.occupancy = occupancy
        self.org_occupancy = occupancy

    def __repr__(self)-> str:
        return f"Name:{self.name}"
    
    def get_name(self)-> str:
        return self.name
    
    def get_barList(self)-> str:
        return self.get_barList
    
    def reset_occupancy(self)-> None:
        self.occupancy = self.org_occupancy

    def update_occupancy(self)-> None:
        self.occupancy = self.occupancy - 1

    def get_occupancy(self)-> int:
        return self.occupancy

class barSort:
    def __init__(self) -> None:
        self.bar_list = []
        
        f = open("barlist.txt", "r")
        self.bar_list = f.read().splitlines()
        self.bar_list = [bar(i) for i in self.bar_list]
        # print(self.bar_list)
        f.close()

        f = open("people.txt", "r")
        self.people = f.read().splitlines()

        # init self.people element as attendee object with list comprehension
        self.people = [attendee(i) for i in self.people]
        f.close()

        self.bar_dict = {}

    def assignBar(self):
        # for bar in self.bar_list:
        # Iterate through all bars in the bar list
        [i.reset_occupancy() for i in self.bar_list]
        bar_people= np.copy(self.people)
        # for bar in np.random.shuffle(self.bar_list):
        for bar in self.bar_list:
            print(f"Bar: \n{bar.name}\n")
            print(f"Start: {bar_people.shape[0]}")

            # Get the current bar's occupancy
            while(bar.get_occupancy() > 0 and bar_people.shape[0]>0):

                # Create a list of potential attendees
                p_list = []
                np.random.shuffle(bar_people)
                for people in bar_people:
                    # If the person hasn't been to this bar before, add them to potential list
                    if people.beenAtBar(bar) and bar.get_occupancy() > 0:
                        p_list.append(people)
                        # people.chosen = True
                        bar.update_occupancy()
                        people.addToBar(bar)
                        bar_people = bar_people[bar_people != people]
                        print(f"Removed: {people}")
                        print(f"number of people; {bar_people.shape[0]}")
                        print("\n")
                

    
        print(f"Last person on list: {bar_people}")
                
                
                    
                    
        # for i in self.people:
        #     print(f"\n Name: {i.name} \n Going to bar: {i.barList()}\n\n")



def main():
    temp = barSort()
    print(temp.bar_list)
    temp.assignBar()
    for i in temp.people:
            print(f"\n Name: {i.name} \n Going to bar: {i.barList()}\n\n")
    
    temp.assignBar()
    temp.assignBar()
    temp.assignBar()
    for i in temp.people:
            print(f"\n Name: {i.name} \n Going to bar: {i.barList()}\n\n")
    



if __name__ == "__main__":
    main()


'''
Notes:

    5 People is good!
    30 / total people (30)



'''