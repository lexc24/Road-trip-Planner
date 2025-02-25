"""
Module for managing a travel trip and computing an optimal route using the TSP solution.

The Trip class encapsulates the journey details, constructs a graph of locations,
computes the optimal route, and formats the travel information.
"""

from itertools import permutations
from model.Objects.Path import *
from model.TSP.DGraph import *
from model.TSP.tspAnswer import runNewSolution


class Trip:
    """Represents a trip itinerary and computes the optimal travel route using TSP.

    This class encapsulates trip data including the starting location, destinations,
    and computes the optimal travel route using a TSP solution. It also provides methods
    to build a graph, convert travel times, and generate summary information.
    """

    def __init__(self, start, destinations):
        """Initialize a Trip instance.

        Args:
            start (str): The starting location.
            destinations (list): A list of destination locations.
        """

        self.destinations = destinations[:]  # Create a copy to avoid modifying the original list
        self.start = start
        self.end = None
        self.time = None
        self.cost = None
        self.path = None
        self.graph = None
        self.dest_dict = None       # Mapping from index to destination name.
        self.index_by_dest = None   # Reverse mapping from destination name to index.

    def build_obj(self):
        """
        Build the trip object by constructing the graph
        """
        self.build_graph()

    def get_travel_data(self):
        """
        Convert the computed TSP path into a list of dictionaries representing each journey leg.

        Each dictionary contains:
            - "Start City": starting location,
            - "Destination City": destination location,
            - "Distance/Time": formatted travel duration.

        Returns:
            list: A list of dictionaries representing each leg of the journey.
        """
        travel_data = []

        # Ensure that a path exists and that the destination dictionary is built.
        if not self.path or not self.dest_dict:
            return travel_data

        # Iterate over each consecutive pair in the TSP path.
        for i in range(len(self.path) - 1):
            start_index = self.path[i]
            dest_index = self.path[i + 1]
            start_city = self.dest_dict[start_index]
            dest_city = self.dest_dict[dest_index]

            # Retrieve the corresponding edge from the graph.
            # The find_node method returns a tuple (weight, vertex, path_obj)
            weight, vertex, path_obj = self.graph.find_node(start_index, dest_index)

            # Check if the edge is valid and has a time_str attribute.
            if path_obj is not None and hasattr(path_obj, "time_str"):
                travel_time = path_obj.time_str
            else:
                travel_time = "N/A"

            # Append the leg as a dictionary.
            travel_data.append({
                "Start City": start_city,
                "Destination City": dest_city,
                "Distance/Time": travel_time
            })

        return travel_data

    def build_graph(self):
        """
        Construct the graph of locations and compute the optimal TSP path.

        Steps:
            1. Create a list of locations (start followed by destinations).
            2. Build mapping dictionaries between location names and indices.
            3. Initialize a directed graph (DGraph) with the appropriate number of vertices.
            4. Add directed edges between every pair of locations using Path objects.
            5. Run the TSP solution starting from the start location.
            6. Determine the final destination based on the computed path.
        """

        # Build a list of all locations with the start as the first element.
        all_locations = [self.start] + self.destinations

        # Create mappings between indices and destination names.
        self.dest_dict = {i: loc for i, loc in enumerate(all_locations)}
        self.index_by_dest = {loc: i for i, loc in self.dest_dict.items()}

        # Initialize the directed graph with the appropriate number of vertices.
        self.graph = DGraph(len(all_locations))

        # Generate all ordered pairs of locations to represent all possible directed edges.
        # Assume that Path is a class which takes (origin, destination) and has an attribute time_num.
        paths = [Path(origin, destination) for origin, destination in permutations(all_locations, 2)]

        # Add each edge to the graph using the precomputed index mappings.
        for p in paths:
            origin_index = self.index_by_dest[p.start]
            destination_index = self.index_by_dest[p.end]
            self.graph.add_edge(origin_index, destination_index, p.time_num, p)

        # Run the TSP solution starting at the index corresponding to the start location.
        start_index = self.index_by_dest[self.start]
        self.cost, self.path = runNewSolution(self.graph, start_index)

        # Set the end location as the destination of the final vertex in the computed path.
        self.end = self.dest_dict[self.path[-1]]

        # Optional: Print the graph structure for debugging.
        self.graph.print_graph()


#
# t = Trip("Orlando,FL", ["Dallas,TX", "Baltimore,MD", "Chicago,IL" ])
# t.build_obj()
# print(t.str)
#
# print(t.get_travel_data())
