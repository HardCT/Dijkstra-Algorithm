import numpy as np

'''
Create dictionary to store edge information. Since this is an undirected graph, each edge records once.
'''
Edges = {("Paddington", "Notting Hill Gate"): 4, ("Paddington", "Baker Street"): 6,
         ("Notting Hill Gate", "Bond Street"): 7,
         ("Notting Hill Gate", "South Kensington"): 7, ("Baker Street", "Bond Street"): 2,
         ("Baker Street", "Oxford Circus"): 4,
         ("Baker Street", "Kings Cross"): 7, ("Bond Street", "Green Park"): 2, ("Bond Street", "Oxford Circus"): 1,
         ("Green Park", "South Kensington"): 7, ("Green Park", "Victoria"): 2, ("Green Park", "Oxford Circus"): 2,
         ("Green Park", "Westminster"): 3, ("Green Park", "Piccadilly Circus"): 1, ("South Kensington", "Victoria"): 4,
         ("Victoria", "Westminster"): 4, ("Oxford Circus", "Piccadilly Circus"): 2,
         ("Oxford Circus", "Warren Street"): 2,
         ("Oxford Circus", "Tottenham Court Road"): 2, ("Westminster", "Embankment"): 2, ("Westminster", "Waterloo"): 2,
         ("Piccadilly Circus", "Leicester Square"): 2, ("Piccadilly Circus", "Charing Cross"): 2,
         ("Warren Street", "Tottenham Court Road"): 3,
         ("Warren Street", "Kings Cross"): 3, ("Tottenham Court Road", "Leicester Square"): 1,
         ("Tottenham Court Road", "Holborn"): 2,
         ("Leicester Square", "Charing Cross"): 2, ("Leicester Square", "Holborn"): 2,
         ("Charing Cross", "Embankment"): 1,
         ("Embankment", "Waterloo"): 2, ("Embankment", "Blackfriars"): 4, ("Waterloo", "Elephant and Castle"): 4,
         ("Waterloo", "London Bridge"): 3, ("Elephant and Castle", "London Bridge"): 3, ("Holborn", "Kings Cross"): 4,
         ("Holborn", "Bank"): 5, ("Blackfriars", "Bank"): 4, ("Kings Cross", "Old Street"): 6,
         ("Kings Cross", "Moorgate"): 6,
         ("Old Street", "Moorgate"): 1, ("Moorgate", "Bank"): 3, ("Moorgate", "Liverpool Street"): 2,
         ("Bank", "London Bridge"): 2,
         ("Bank", "Liverpool Street"): 2, ("Bank", "Tower Hill"): 2, ("Liverpool Street", "Tower Hill"): 6,
         ("Liverpool Street", "Aldgate East"): 4, ("Tower Hill", "Aldgate East"): 2}

"""
# Test case of smaller network.
Edges = {("W", "E"): 8, ("E", "K"): 4, ("E", "P"): 6, ("K", "P"): 1}
"""


# It can be more convenient using matrix to access edges values, reducing assignment workload of undirected graph.
def ConstructMatrix():
    """
    This function takes global variables StationIndex and Edges, converting dictionary into matrix.
    :return: matrix storing all edges information
    """
    # Get all station names from Edges.
    all_stations = set()
    for (station1, station2), time in Edges.items():
        all_stations.add(station1)
        all_stations.add(station2)

    # Assign stations with indices.
    Stations = sorted(all_stations)
    Indices = {station: index for index, station in enumerate(Stations)}

    StationNum = len(Stations)  # Initialize size of matrix.
    Matric = np.full((StationNum, StationNum), np.inf)  # Set infinite value to all unknown routes.
    # It spends 0 minutes travelling to itself.
    for i in range(StationNum):
        for j in range(StationNum):
            if i == j:
                Matric[i][j] = 0
    # Assign values from keys in dictionary Edges to matrix.
    for (edge1, edge2), val in Edges.items():
        i = Indices[edge1]  # From this Station ....
        j = Indices[edge2]  # to next Station;
        Matric[i][j] = val  # value assignment for known value in dictionary Edges.
        Matric[j][i] = val  # Symmetric value assignment for an undirected graph.

    return Matric, Stations, Indices


Matrix, Indices, StationsIndex = ConstructMatrix()  # Call function to store information into global variables.


# This function is called from function ShortestPath(Start, End).
def Dijkstra(S, Extra, time, path, visited):
    """
    This function recursively updates 4 dictionaries when more efficient route appears.
    :param S: Index of current location.
    :param Extra: Dictionary storing all currently unvisited routes.
    :param time: Dictionary storing current minimal time to each station.
    :param path: Dictionary storing current route of minimal time to each station.
    :param visited: Dictionary storing stations visited or not, avoiding duplicated operation.
    :return: If all stations visited: Completed dictionaries time and path; else: updated location and dictionaries.
    """
    visited[S] = True  # Set current location as visited slot.

    for j in range(len(Matrix[S])):  # For all stations in S, we select all current edges.
        if Matrix[S][j] != np.inf and S != j and not visited[j]:  # If this available path has not been visited:
            Extra[(S, j)] = Matrix[S][j] + time[S]  # update Extra so that this new path is to be compared.
            if Extra[(S, j)] < time[j]:  # If any path value is shorter than previous...
                time[j] = Extra[(S, j)]  # update time by current path value...
                path[j] = path[S] + [j]  # and update its path by joining path of last station.

    # If all paths operated, return completed dictionaries.
    if not Extra:
        return time, path
    # Else update dictionaries and location for next recursive operation.
    else:
        min_value = min(Extra.values())  # Select station set of min value...
        min_key = [key for key, value in Extra.items() if value == min_value][0]  # its first element is start location
        new = min_key[1]  # its second element is next location
        Extra.pop(min_key, None)  # delete minimal start location since it will be operated at next loop.
        return Dijkstra(new, Extra, time, path, visited)


# This function works as main function and prints outcome.
def ShortestPath(Start, End):
    """
    This function provides initial values and calls up recursive function.
    :param Start: Name of start station.
    :param End: Name of end station.
    :return: None. It prints output.
    """
    S = StationsIndex[Start]  # Get index of starting station.
    E = StationsIndex[End]  # Get index of end station.

    Extra = {}  # Each turn, we compare some edges and store value in it.
    time = {i: np.inf for i in range(len(StationsIndex))}  # Each station's time initialized as infinitely large.
    time[S] = 0  # Station to itself is 0 minutes.
    path = {S: [S]}  # Each station's current path, in which starting station as the starting of the path.
    visited = {i: False for i in range(len(StationsIndex))}  # All nodes initialized as unvisited.
    time, path = Dijkstra(S, Extra, time, path, visited)  # Uses previous function to get set of time and path.
    TIME = int(time[E])  # Get time of end location
    path0 = path[E]  # Get path of end location
    route = []  # Initialize a new list....
    for i in path0:
        route += [k for k, v in StationsIndex.items() if v == i]  # And store names of stations of index.
    PATH = " -> ".join(route)  # Add -> to each section.
    print("Starting station : ", Start)
    print("Destination station : ", End)
    print("Time : ", TIME, "minutes")
    print("Route : ", PATH)

    return False


"""
# Test input of smaller network.
StartLocation = "W"
EndLocation = "P"
ShortestPath(StartLocation, EndLocation)
"""

# Four example inputs.
StartLocation0 = "Aldgate East"
EndLocation0 = "Paddington"
StartLocation1 = "Kings Cross"
EndLocation1 = "Waterloo"
StartLocation2 = "Notting Hill Gate"
EndLocation2 = "Bank"
StartLocation3 = "Bond Street"
EndLocation3 = "Westminster"
StartLocation4 = "Elephant and Castle"
EndLocation4 = "Baker Street"

ShortestPath(StartLocation0, EndLocation0)
ShortestPath(StartLocation1, EndLocation1)
ShortestPath(StartLocation2, EndLocation2)
ShortestPath(StartLocation3, EndLocation3)
ShortestPath(StartLocation4, EndLocation4)

# We also added extra user interface to support more searching.
print("\n")
print("The examples above show 4 different routes.")
act = input("Would you like to search more routes?[Y/N] ")
if act.lower() == 'n':
    print("Execution completes.")
else:
    # List all stations for input convenience.
    for n, station in enumerate(Indices):
        print(f"{n}. {station}")

    # Loop until getting valid start-station input.
    while True:
        while True:
            try:
                Start = int(input("Choose from above, where do you set off:(Index only) "))
                if 0 <= Start < len(Indices):  # If valid input, then end loop.
                    StartLocation = Indices[Start]
                    break
                else:  # If input out of bound:
                    print("Number out of bound. Please re-enter input;")
            except ValueError:  # If input is not a number:
                print("Incorrect input. Please re-enter a valid number;")

        # Loop until getting valid end-station input.
        while True:
            try:
                End = int(input("Choose from above, where are you heading to:(Index only) "))
                if 0 <= End < len(Indices):  # If valid input, then end loop.
                    EndLocation = Indices[End]
                    break
                else:  # If input out of bound:
                    print("Number out of bound. Please re-enter input;")
            except ValueError:  # If input is not a number:
                print("Incorrect input. Please re-enter a valid number;")

        # It starts with correct parameter value only.
        ShortestPath(StartLocation, EndLocation)
        # User can choose to either start a new search or exit.
        Next = input("Do you request another search:[Y/N] ")
        if Next.lower() == 'n':
            break
        else:
            print("\n")
