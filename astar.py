import heapq
import math
from datetime import datetime, date, time
from typing import Callable

import geopy.distance

import data_pre_processing
from data_pre_processing import Node


def astar(start: Node, goal: list[Node], cost_fn: Callable[[Node, Node], int],
          heuristic_fn: Callable[[Node, Node], float]):
    front = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    end_node = None
    while front:
        _, current = heapq.heappop(front)

        if current in goal:
            end_node = current
            break

        for neighbor in current.neighbours:
            new_cost = cost_so_far[current] + cost_fn(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                # all of them SHOULD have the same coordinates because they have the same end_stop so we take first
                # of them
                priority = new_cost + heuristic_fn(goal[0], neighbor)
                heapq.heappush(front, (priority, neighbor))
                came_from[neighbor] = current

    path = []
    current = end_node
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path, cost_so_far[end_node]


def get_start_node(graph: dict, start_dest: str, start_time: str):
    """gets start node based on start_dest string and start_time string
        start node is the node with ride_info.start_stop = start_dest and ride_info.departure_time > start_time
        we are looking for node with earliest ride_info.departure_time
    """
    start_time = data_pre_processing.parse_time(start_time)
    earliest_start_node = None
    for node in graph.keys():
        if node.ride_info.start_stop == start_dest and node.ride_info.departure_time > start_time:
            if earliest_start_node is None:
                earliest_start_node = node
            elif node.ride_info.departure_time < earliest_start_node.ride_info.departure_time:
                earliest_start_node = node
    return earliest_start_node


# TODO think about moving this and function above somewhere else
def get_end_nodes(graph: dict, stop: str, time: str):
    """:return list of possible end nodes, list because we dont know by which line we will get to the destination"""
    candidates = []
    time = data_pre_processing.parse_time(time)
    for node in graph.keys():
        if node.ride_info.end_stop == stop and node.ride_info.arrival_time > time:
            candidates.append(node)
    return candidates


def geo_distance(a: Node, b: Node) -> float:
    return geopy.distance.geodesic((a.geo_info.start_lat, a.geo_info.start_long),
                                   (b.geo_info.start_lat, b.geo_info.start_long)).km


def cost_time(a: Node, b: Node):
    """returns difference between ride_info.departure_time of nodes in minutes as cost function of time"""
    return int((datetime.combine(date.min, b.ride_info.departure_time) -
                datetime.combine(date.min,a.ride_info.departure_time)).total_seconds() // 60)




