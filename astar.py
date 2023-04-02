import heapq
import math
from datetime import datetime, date, time
from typing import Callable

import geopy.distance

import data_pre_processing
from data_pre_processing import Node

from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

@timeit
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


def get_start_node(graph: dict, start_dest: str, start_time: str, end_node: Node):
    """gets start node based on start_dest string and start_time string
        start node is the node with ride_info.start_stop = start_dest and ride_info.departure_time > start_time
        we are looking for node with earliest ride_info.departure_time
    """
    start_time = data_pre_processing.parse_time(start_time)
    earliest_start_node = None
    for node in graph.keys():
        if node.ride_info.start_stop == start_dest and node.ride_info.departure_time > start_time:
            #print(f'{earliest_start_node},   {node}')
            if earliest_start_node is None:
                earliest_start_node = node
            elif node.ride_info.departure_time < earliest_start_node.ride_info.departure_time and \
                    geo_distance(earliest_start_node, end_node) >= geo_distance(node, end_node):
                print(f'{earliest_start_node},   {node}')
                earliest_start_node = node
    return earliest_start_node


# TODO think about moving this and function above somewhere else
def get_nodes_by_name(graph: dict, stop: str, time: str):
    """:return list of possible end nodes, list because we dont know by which line we will get to the destination"""
    candidates = []
    time = data_pre_processing.parse_time(time)
    for node in graph.keys():
        if node.ride_info.end_stop == stop and node.ride_info.arrival_time > time:
            candidates.append(node)
    return candidates

#
# def geo_distance(a: Node, b: Node) -> float:
#     return geopy.distance.geodesic((a.geo_info.start_lat, a.geo_info.start_long),
#                                    (b.geo_info.start_lat, b.geo_info.start_long)).km

def geo_distance(a: Node, b: Node) -> float:
    return abs(a.geo_info.start_lat - b.geo_info.start_lat) + abs(a.geo_info.start_long - b.geo_info.start_long) * 111.1



def cost_time(a: Node, b: Node):
    """returns difference between ride_info.departure_time of nodes in minutes as cost function of time"""
    return int((datetime.combine(date.min, b.ride_info.departure_time) -
                datetime.combine(date.min, a.ride_info.departure_time)).total_seconds() // 60)


def cost_switch_line(a: Node, b: Node):
    if a.ride_info.line != b.ride_info.line or a.ride_info.arrival_time != b.ride_info.departure_time:
        return 5
    return 0


def cost_combined(a, b):
    return cost_time(a, b) + cost_switch_line(a, b) * 2
