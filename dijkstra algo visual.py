import tkinter as tk
import turtle
import heapq

# Set up the Tkinter window
root = tk.Tk()
root.title("Dijkstra's Algorithm Visualization")
root.geometry("400x200")

# Define the graph
graph = {
    'A': {'B': 2, 'C': 1},
    'B': {'A': 2, 'D': 3, 'E': 4},
    'C': {'A': 1, 'D': 2},
    'D': {'B': 3, 'C': 2, 'E': 1},
    'E': {'B': 4, 'D': 1}
}

# Define node positions manually for visual representation
positions = {
    'A': (-100, 100),
    'B': (100, 100),
    'C': (-100, -100),
    'D': (100, -100),
    'E': (250, -100)
}

# Create a turtle screen for drawing the graph
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Graph Visualization")

# Create a turtle for drawing the graph
graph_turtle = turtle.Turtle()
graph_turtle.speed(10)
graph_turtle.hideturtle()


# Function to draw nodes
def draw_node(node, position, color="black"):
    graph_turtle.penup()
    graph_turtle.goto(position)
    graph_turtle.pendown()
    graph_turtle.color(color)
    graph_turtle.begin_fill()
    graph_turtle.circle(20)
    graph_turtle.end_fill()
    graph_turtle.penup()
    graph_turtle.goto(position[0], position[1] + 25)
    graph_turtle.write(node, align="center", font=("Arial", 12, "normal"))


# Function to draw edges with weights
def draw_edge(start, end, weight):
    start_pos = positions[start]
    end_pos = positions[end]
    graph_turtle.penup()
    graph_turtle.goto(start_pos)
    graph_turtle.pendown()
    graph_turtle.goto(end_pos)

    # Midpoint for the weight label
    midpoint = ((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2)
    graph_turtle.penup()
    graph_turtle.goto(midpoint[0], midpoint[1] - 10)
    graph_turtle.write(weight, align="center", font=("Arial", 10, "normal"))


# Function to implement Dijkstra's algorithm
def shortest_path(graph, start, end):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous_nodes = {node: None for node in graph}
    visited_nodes = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited_nodes:
            continue

        visited_nodes.add(current_node)

        # Highlight the current node
        highlight_node(current_node)

        for neighbour_node, weight in graph[current_node].items():
            if neighbour_node in visited_nodes:
                continue

            distance = current_distance + weight
            if distance < distances[neighbour_node]:
                distances[neighbour_node] = distance
                previous_nodes[neighbour_node] = current_node
                heapq.heappush(priority_queue, (distance, neighbour_node))

                # Highlight the edge
                highlight_edge(current_node, neighbour_node, weight)

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path = path[::-1]

    return path, distances[end]


# Function to highlight a node (change color)
def highlight_node(node):
    graph_turtle.penup()
    graph_turtle.goto(positions[node])
    graph_turtle.pendown()
    graph_turtle.color("red")
    graph_turtle.begin_fill()
    graph_turtle.circle(20)
    graph_turtle.end_fill()
    graph_turtle.penup()


# Function to highlight an edge (change color)
def highlight_edge(start, end, weight):
    start_pos = positions[start]
    end_pos = positions[end]
    graph_turtle.penup()
    graph_turtle.goto(start_pos)
    graph_turtle.pendown()
    graph_turtle.color("blue")
    graph_turtle.goto(end_pos)

    midpoint = ((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2)
    graph_turtle.penup()
    graph_turtle.goto(midpoint[0], midpoint[1] - 10)
    graph_turtle.write(weight, align="center", font=("Arial", 10, "normal"))


# Function to run Dijkstra and update the GUI
def run_dijkstra():
    start_node = start_entry.get().strip().upper()
    end_node = end_entry.get().strip().upper()

    if start_node not in graph or end_node not in graph:
        result_label.config(text="ERROR: Invalid nodes")
        return

    result_label.config(text="Running Dijkstra...")
    root.update()

    # Run the Dijkstra algorithm
    path, distance = shortest_path(graph, start_node, end_node)

    # Display the result
    path_label.config(text=f"Shortest Path: {' -> '.join(path)}")
    distance_label.config(text=f"Distance: {distance}")
    result_label.config(text="Algorithm Complete")

    # Reset all node colors to black after completion
    reset_node_colors()


# Function to reset all node colors to black
def reset_node_colors():
    for node, position in positions.items():
        draw_node(node, position, color="black")


# GUI Setup
start_label = tk.Label(root, text="Start Node:")
start_label.pack()

start_entry = tk.Entry(root)
start_entry.pack()

end_label = tk.Label(root, text="End Node:")
end_label.pack()

end_entry = tk.Entry(root)
end_entry.pack()

run_button = tk.Button(root, text="Run Dijkstra", command=run_dijkstra)
run_button.pack()

path_label = tk.Label(root, text="Shortest Path: ")
path_label.pack()

distance_label = tk.Label(root, text="Distance: ")
distance_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Draw initial graph (nodes and edges)
for node, position in positions.items():
    draw_node(node, position)

for node, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
        if node < neighbor:
            draw_edge(node, neighbor, weight)

# Start the Tkinter main loop
root.mainloop()
