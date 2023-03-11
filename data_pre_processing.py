from datetime import datetime,time
import pprint
from dataclasses import dataclass
import pandas as pd


@dataclass
class RideInformation:
    """ class for keeping info about ride information of the node"""
    line: str
    departure_time: datetime.time  # for easy comparisons
    arrival_time: datetime.time
    start_stop: str
    end_stop: str


@dataclass
class GeoInformation:
    """class for keeping geological info about the node"""
    start_lat: float
    start_long: float
    stop_lat: float
    stop_lon: float

class Node:
    def __init__(self, ride_info: RideInformation, geo_info: GeoInformation):
        self.ride_info = ride_info
        self.geo_info = geo_info
        self.neighbours = []

    def __str__(self):
        return f"Node {self.ride_info.line} start {self.ride_info.start_stop} {self.ride_info.departure_time}" \
               f"end {self.ride_info.end_stop} {self.ride_info.arrival_time}"

    #its required for heappush and it promotes staying on the same line if priority is the same
    def __lt__(self, other):
        return self

    def set_neighbours(self, nodes_by_start_stop: dict):
        """ creates a list of neighbours to the node , neighbour nodes are those that have start_stop equal to
            Node's end_stop and departure time > Node's arrival_time"""
        try:
            self.neighbours = list(filter(lambda node: (node.ride_info.departure_time >= self.ride_info.arrival_time),nodes_by_start_stop[self.ride_info.end_stop]))
        except KeyError:
            self.neighbours = []
            # it seems like for  Żórawina - Niepodległości (Mostek) there are end stops named like that
            # but there are no start stops so i'll skip them
            print(f"{self.ride_info.end_stop} brak takiego przystanku startowego")



def create_graph(filename: str):
    """graph will be stored as {Node: List[Nodes}}, list of nodes are the Node's neighbours"""
    graph = {}

    df = pd.read_csv(filename,
                     dtype={"unnamed": int, "company": str, "line": str, "departure_time": str, "arrival_time": str
                         , "start_stop": str, "end_stop": str, "start_stop_lat": float, "start_stop_lon": float,
                            "end_stop_lat": float, "end_stop_lon": float})
    nodes_list = []

    #to optimize it so we dont have to iterate over all nodes in search of its neighbours
    node_by_start_stop_dict = {}

    #for debug and info on progress
    nodes_created = 0
    neighbours_added=0


    for index, row in df.iterrows():

        r_info = RideInformation(
            row['line'],
            parse_time(row['departure_time']),
            parse_time(row['arrival_time']),
            row['start_stop'],
            row['end_stop'])
        g_info = GeoInformation(
            float(row['start_stop_lat']),
            float(row['start_stop_lon']),
            float(row['end_stop_lat']),
            float(row['end_stop_lon']),
        )
        n = Node(r_info, g_info)

        if (start_stop := n.ride_info.start_stop) not in node_by_start_stop_dict:
            node_by_start_stop_dict[start_stop] = [n]
        else:
            node_by_start_stop_dict[start_stop].append(n)

        nodes_list.append(n)
        nodes_created += 1
        if nodes_created%10000==0:
            print(f"{nodes_created} nodes created")

    for node in nodes_list:
        neighbours_added+=1

        node.set_neighbours(node_by_start_stop_dict)
        graph[node] = node.neighbours
        if neighbours_added % 10000 == 0:
            print(f"{neighbours_added} neighbours added")

    return graph




def parse_time(t: str):
    """ parses string in format HH:MM:SS , there is probably a library for this but i couldn't find it"""
    h, m, s = int(t[0:2]), int(t[3:5]), int(t[6:8])
    return time(h, m, s)

