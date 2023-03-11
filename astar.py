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
                # all of them SHOULD have the same coordinates because they have the same end_stop so we take first of them
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


# there could be many of them because we dont know when we will arive
def get_end_nodes(graph: dict, stop: str, time: str):
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
    return int((datetime.combine(date.min, b.ride_info.departure_time) - datetime.combine(date.min,
                                                                                          a.ride_info.departure_time)).total_seconds() // 60)


def manhattan_distance(a, b):
    return sum([abs(x - y) for x, y in zip(a, b)])


def euclidean_distance(a, b):
    return math.sqrt(sum([(x - y) ** 2 for x, y in zip(a, b)]))


def towncenter_distance(a, b):
    return euclidean_distance(a, (0, 0, 0, 0, 0, 0, 0)) + euclidean_distance((0, 0, 0, 0, 0, 0, 0), b)


def unidimensional_distance(a, b):
    return max([abs(x - y) for x, y in zip(a, b)])


def cosine_distance(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x ** 2 for x in a))
    magnitude_b = math.sqrt(sum(x ** 2 for x in b))
    return 1 - (dot_product / (magnitude_a * magnitude_b))


def chebyshev_distance(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


if __name__ == '__main__':
    # node is {(posions)}
    # graph is {node:[neighbours]}

    graph = {
        (0, 0, 0, 0, 0, 0, 0): [(1, 1, 1, 1, 1, 1, 1), (1, 2, 3, 4, 5, 6, 7), (4, 5, 6, 7, 8, 9, 10),
                                (5, 6, 7, 8, 6, 5, 1)],
        (1, 2, 3, 4, 5, 6, 7): [(2, 3, 4, 5, 6, 7, 8), (1, 1, 1, 1, 1, 1, 1), (5, 2, 1, 4, 1, 3, 1)],
        (2, 3, 4, 5, 6, 7, 8): [(3, 4, 5, 6, 7, 8, 9), (2, 4, 2, 1, 4, 1, 8), (1, 2, 3, 4, 5, 6, 7),
                                (5, 6, 7, 8, 6, 5, 1), (6, 6, 10, 2, 2, 5, 10), (9, 3, 2, 7, 0, 0, 1),
                                (9, 9, 2, 0, 2, 1, 9)],
        (3, 4, 5, 6, 7, 8, 9): [(4, 5, 6, 7, 8, 9, 10)],
        (4, 5, 6, 7, 8, 9, 10): [],
        (1, 1, 1, 1, 1, 1, 1): [(2, 2, 2, 2, 2, 2, 2), (5, 2, 1, 4, 1, 3, 1), (6, 6, 10, 2, 2, 5, 10),
                                (10, 10, 10, 10, 10, 10, 10)],
        (2, 2, 2, 2, 2, 2, 2): [],
        (5, 2, 1, 4, 1, 3, 1): [(2, 2, 2, 2, 2, 2, 2), (2, 0, 2, 0, 2, 0, 2), (2, 4, 2, 1, 4, 1, 8),
                                (3, 4, 5, 6, 7, 8, 9), (9, 9, 2, 0, 2, 1, 9)],
        (2, 0, 2, 0, 2, 0, 2): [],
        (2, 2, 2, 2, 2, 2, 2): [(2, 3, 4, 5, 6, 7, 8), (2, 2, 2, 2, 2, 2, 2), (4, 5, 6, 7, 8, 9, 10),
                                (5, 6, 7, 8, 6, 5, 1), (10, 10, 10, 10, 10, 10, 10)],
        (3, 3, 2, 0, 1, 0, 1): [(1, 2, 3, 4, 5, 6, 7), (2, 2, 2, 2, 2, 2, 2), (2, 3, 4, 5, 6, 7, 8),
                                (5, 2, 1, 4, 1, 3, 1), (2, 0, 2, 0, 2, 0, 2), (6, 6, 10, 2, 2, 5, 10),
                                (2, 2, 2, 2, 2, 2, 2)],
        (5, 6, 7, 8, 6, 5, 1): [(2, 0, 2, 0, 2, 0, 2), (3, 4, 5, 6, 7, 8, 9)],
        (6, 6, 10, 2, 2, 5, 10): [(2, 0, 2, 0, 2, 0, 2), (1, 1, 1, 1, 1, 1, 1)],
        (2, 4, 2, 1, 4, 1, 8): [(1, 2, 3, 4, 5, 6, 7), (5, 2, 1, 4, 1, 3, 1), (2, 0, 2, 0, 2, 0, 2)],
        (9, 3, 2, 7, 0, 0, 1): [(5, 2, 1, 4, 1, 3, 1), (10, 10, 10, 10, 10, 10, 10)],
        (9, 9, 2, 0, 2, 1, 9): [(2, 0, 2, 0, 2, 0, 2), (10, 10, 10, 10, 10, 10, 10)],
        (10, 10, 10, 10, 10, 10, 10): [(2, 0, 2, 0, 2, 0, 2), (3, 4, 5, 6, 7, 8, 9)]
    }

    start = (1, 2, 3, 4, 5, 6, 7)
    goal = (10, 10, 10, 10, 10, 10, 10)

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: manhattan_distance(a, b))
    print(f"Path using Manhattan distance heuristic: {path}")
    print(f"Cost using Manhattan distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: euclidean_distance(a, b))
    print(f"Path using Euclid's distance heuristic: {path}")
    print(f"Cost using Euclid's distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: towncenter_distance(a, b))
    print(f"Path using Towncenter distance heuristic: {path}")
    print(f"Cost using Towncenter distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: unidimensional_distance(a, b))
    print(f"Path using unidimensional distance heuristic: {path}")
    print(f"Cost using unidimensional distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: cosine_distance(a, b))
    print(f"Path using cosine distance heuristic: {path}")
    print(f"Cost using cosine distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: chebyshev_distance(a, b))
    print(f"Path using Chebyshev distance heuristic: {path}")
    print(f"Cost using Chebyshev distance heuristic: {cost}")
