import astar
import data_pre_processing
import djikstra


def main():
    start_stop = "Kościuszki"
    start_time = "07:15:00"
    end_stop = "Magellana"

    graph = data_pre_processing.create_graph('../connection_graph.csv')

    ends = astar.get_nodes_by_name(graph, end_stop, start_time)
    start = astar.get_start_node(graph,start_stop,start_time,ends[0])
    print("start searching")
    path_astar,cost_astar = astar.astar(start,ends,astar.cost_combined,astar.geo_distance)
    print("------------------------ astar combined")
    print(f"From {start_stop} To {end_stop} at {start_time} in {cost_astar} minutes by:")
    for node in path_astar:
        print(node)

    path_astar, cost_astar = astar.astar(start, ends, astar.cost_time, astar.geo_distance)
    print("------------------------astar time")
    print(f"From {start_stop} To {end_stop} at {start_time} in {cost_astar} minutes by:")
    for node in path_astar:
        print(node)

    path_astar, cost_astar = astar.astar(start, ends, astar.cost_switch_line, astar.geo_distance)
    print("------------------------ astra line")
    print(f"From {start_stop} To {end_stop} at {start_time} in {cost_astar} minutes by:")
    for node in path_astar:
        print(node)
    print("------------------------ djikstra combined")
    path_dijkstra, cost_dijkstra = djikstra.dijkstra(graph, start, ends, astar.cost_combined)
    print(f"From {start_stop} To {end_stop} at {start_time} in {cost_dijkstra} minutes by:")
    for node in path_dijkstra:
        print(node)
    print("------------------------djikstra time")
    path_dijkstra, cost_dijkstra = djikstra.dijkstra(graph, start, ends, astar.cost_time)
    print(f"From {start_stop} To {end_stop} at {start_time} in {cost_dijkstra} minutes by:")
    for node in path_dijkstra:
        print(node)
    print("------------------------djikstra line")
    path_dijkstra, cost_dijkstra = djikstra.dijkstra(graph, start, ends, astar.cost_switch_line)
    print(f"From {start_stop} To {end_stop} at {start_time} in {cost_dijkstra} minutes by:")
    for node in path_dijkstra:
        print(node)

if __name__ == "__main__":
    main()