import heapq

import astar
import data_pre_processing


def dijkstra(graph, start, end,cost_fn):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Create a dictionary to keep track of the previous node in the shortest path to each node
    previous_nodes = {node: None for node in graph}

    # Create a priority queue to hold nodes to visit, with the start node having the highest priority (i.e., the lowest distance)
    priority_queue = [(0, start)]

    while priority_queue:
        # Pop the node with the lowest distance from the priority queue
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we have reached the end node, we're done
        if current_node in end:
            # Build the shortest path by following the previous_nodes dictionary backwards
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            path.reverse()
            # Return the shortest path and its distance
            return path, current_distance

        # Otherwise, for each neighbor of the current node, calculate its tentative distance through the current node
        for neighbor in graph[current_node]:
            tentative_distance = current_distance + cost_fn(current_node,neighbor)

            # If the tentative distance is lower than the current distance to the neighbor, update its distance and previous node
            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                previous_nodes[neighbor] = current_node
                # Add the neighbor to the priority queue with its new distance as its priority
                heapq.heappush(priority_queue, (tentative_distance, neighbor))

    # If we get here, there is no path from start to end
    return None, None
