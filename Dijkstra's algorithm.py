import heapq
graph = {
    'A': {'B': 2, 'C': 1},
    'B': {'A': 2, 'D': 3, 'E': 4, 'F': 2},
    'C': {'A': 1, 'D': 2, 'F': 1},
    'D': {'B': 3, 'C': 2, 'E': 1},
    'E': {'B': 4, 'D': 1},
    'F': {'B': 2, 'C': 1}
}

def shortest_path(graph, start, end):
        # Initialising distances with Infinity so we can consider
        # Different Edge Weights (Distance Values)
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0

        priority_queue = [(0, start)]
        previous_nodes = {node: None for node in graph}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # If popped node distance is greater skip it
            if current_distance > distances[current_node]:
                continue
            for neighbour_node, weight in graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbour_node]:
                    distances[neighbour_node] = distance
                    previous_nodes[neighbour_node] = current_node
                    heapq.heappush(priority_queue, (distance, neighbour_node))
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path = path[::-1]

        if distances[end] == float('infinity'):
            return None, float('infinity')
        else:
            return path, distances[end]

def print_graph(graph):
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
             # To avoid printing the same edge twice, only print once per edge
            if node < neighbor:
                print(f"     {node} --{weight}-- {neighbor}")



while True:

    print("\t\tNODES")
    print("\t\t-----")
    # for node in graph:
    #     print(node, end="\n")

    print(print_graph(graph))
    print("")
    try:
        start_node = str(input("Where are you starting?: ")).strip().capitalize()
        end_node = str(input("Where do you want to end?: ")).strip().capitalize()
        if start_node not in graph or end_node not in graph:
            print("ERROR: Please enter a NODE in the graph: ")
            continue
        print(shortest_path(graph, start_node, end_node))
        break

    except ValueError:
        print("ERROR: Invalid Input, Please try again.")
        continue

