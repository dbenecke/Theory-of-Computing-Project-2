import csv
from collections import deque

class NondeterministicTuringMachine:
    def __init__(self, file_path):
        self.name = None
        self.states = []
        self.alphabetI = []
        self.alphabetT = []
        self.startq = None
        self.accq = None
        self.rejq = None
        self.transitions = []

        #read the .csv file
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        
        #assign values according to csv
        self.name = rows[0][0]
        self.states = rows[1]
        self.alphabetI = rows[2]
        self.alphabetT = rows[3]
        self.startq = rows[4][0]
        self.accq = rows[5][0]
        self.rejq = rows[6][0]

        #Transitions
        self.transitions = [
            {
                "nowstate": row[0],
                "inputS": row[1],
                "newState": row[2],
                "replace": row[3],
                "leftright": row[4]
            }
            for row in rows[7:]
        ]

#run the NTM on a given input
    def run(self, whatInput, maxD):
        #configuration: (tape left of head, current state, tape right of head)
        startConfig = ("", self.startq, whatInput)
        queue = deque([[startConfig]])  #queue to store paths of configurations
        steps = 0  #number of transitions made
        longest_reject_path = []
        maxDreached = 0  
        totaltransitions = 0
        nonleafnodes = 0
        allpaths = []

        while queue:
            path = queue.popleft()  #get the next path
            #print("Path",path)
            nowConfig = path[-1]  #current configuration is the last in the path
            left, state, right = nowConfig

            #update
            maxDreached = max(maxDreached, len(path) - 1)
            allpaths.append(nowConfig)

            #check if accept state
            if state == self.accq:
                print(f"Machine name: {self.name}")
                print(f"Intial string: {whatInput}")
                print(f"Accepted in this many transitions: {steps}")
                print(f"Depth of tree: {maxDreached}")
                self.print_path(path)  #print the trace
                self.print_nondeterminism(totaltransitions, nonleafnodes)
                for trace1 in allpaths:
                    print(trace1)
                return

            if len(path) > len(longest_reject_path):
                longest_reject_path = path  #update the longest reject path

            #if exceeds the depth limit stop process of this path
            if steps >= maxD:
                continue

            #get head or blank if tape is empty
            head = right[0] if right else "_"

            #check for valid transitions from the current configuration
            validtransitions = [
                t for t in self.transitions
                if t["nowstate"] == state and t["inputS"] == head
            ]

            if validtransitions:
                nonleafnodes += 1

                for transition in validtransitions:
                    newState = transition["newState"]
                    replace = transition["replace"]
                    leftright = transition["leftright"]

                    #create a new configuration based on the transition
                    changedleft = left
                    changedright = right

                    if leftright == "L":  #move head left
                        changedleft = left[:-1] if left else ""
                        changedright = left[-1] + replace + right[1:] if left else "_" + right[1:]
                    elif leftright == "R":  #move head right
                        changedleft = left + replace
                        changedright = right[1:] if len(right) > 1 else ""
                    else:  #stay
                        changedright = replace + right[1:]

                    changedconfig = (changedleft, newState, changedright)  #new configuration
                    queue.append(path + [changedconfig])  #add new path to the queue
                    totaltransitions += 1

            steps += 1

        #if no accepting path is found print rejection message
        print(f"Machine name: {self.name}")
        print(f"String rejected after this many transitions: {steps}")
        print(f"Depth of tree: {maxDreached}")
        self.print_path(longest_reject_path)
        self.print_nondeterminism(totaltransitions, nonleafnodes)

    #print the degree of nondeterminism
    def print_nondeterminism(self, totaltransitions, nonleafnodes):
        if nonleafnodes == 0:
            print("Degree of nondeterminism: 0")
        else:
            degree = totaltransitions / nonleafnodes  #round up to the nearest integer
            print(f"Degree of nondeterminism: {degree:.2f}")    

    #print the sequence of configurations from start to the final state
    def print_path(self, path):
        print("Trace:")
        for config in path:
            left, state, right = config
            print(f"{left}[{state}]{right}")

    

# Example usage
file_path = "check4_DaniaBenecke.csv"
whatInput = "abc"
maxD = 100

ntm = NondeterministicTuringMachine(file_path)
ntm.run(whatInput, maxD)