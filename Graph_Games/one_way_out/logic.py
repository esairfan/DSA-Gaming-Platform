import math
import random

# Define number of nodes and edges
num_nodes = 7
num_edges = 10
radius = 200  # Radius of the circle on which nodes will be placed

# Calculate positions for nodes in a circular layout
center_x, center_y = 600, 400
nodes = []

for i in range(num_nodes):
    angle = 2 * math.pi * i / num_nodes
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    nodes.append((x, y))

# Generate random edges ensuring no duplicate edges
edges = set()

while len(edges) < num_edges:
    u, v = random.sample(range(num_nodes), 2)
    edge = tuple(sorted([u, v]))  # Avoid duplicate edges (e.g., (1,2) and (2,1))
    edges.add(edge)

# Function to check the win condition
def check_win(used_edges):
    return len(used_edges) == len(edges)

# Function to check the lose condition
def check_lose(clicked_nodes, edges, used_edges):
    if clicked_nodes:
        current_node = clicked_nodes[-1]
        connected_edges = [edge for edge in edges if current_node in edge and edge not in used_edges]
        return not connected_edges  # No untraversed edges available
    return False

# Function to handle node clicks and mark edges as used
def handle_node_click(clicked_nodes, used_edges, edges, i):
    if not clicked_nodes or i != clicked_nodes[-1]:  # Avoid double-click on same node
        if not clicked_nodes:  # First node selected
            clicked_nodes.append(i)
        else:
            # Check if there is an untraversed edge between the last node and this node
            last_node = clicked_nodes[-1]
            edge = tuple(sorted([last_node, i]))
            if edge in edges and edge not in used_edges:
                clicked_nodes.append(i)
                used_edges.add(edge)
                print(f"Edge {edge} marked as used.")

    return clicked_nodes, used_edges
