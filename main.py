import astar
import data_pre_processing


def main():
    start_stop = "Kościuszki"
    start_time = "19:59:00"
    end_stop = "Magellana"

    graph = data_pre_processing.create_graph('connection_graph.csv')
    start = astar.get_start_node(graph,start_stop,start_time)
    ends = astar.get_end_nodes(graph,end_stop,start_time)
    print("start searching")
    path,cost = astar.astar(start,ends,astar.cost_time,astar.geo_distance)
    print("------------------------")
    print(f"From {start_stop} To {end_stop} at {start_time} in {cost} minutes by:")
    for node in path:
        print(node)
if __name__ == "__main__":
    main()