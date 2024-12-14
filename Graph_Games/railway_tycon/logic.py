import math
import random
 
num_nodes = 7
num_edges = 10
radius = 300
 
center_x, center_y = 600, 400
nodes = []

for i in range(num_nodes):
    angle = 2 * math.pi * i / num_nodes
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    nodes.append((x, y))
 
edges = set()
weights = {}

while len(edges) < num_edges:
    u, v = random.sample(range(num_nodes), 2)
    edge = tuple(sorted([u, v]))
    if edge not in edges:
        edges.add(edge) 
        weight = round(random.uniform(1, 10), 2)
        weights[edge] = weight
 
def get_edge_weight(u, v):
    edge = tuple(sorted([u, v]))
    return weights.get(edge, None)
 
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u]) 
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
            return True
        return False
 
def kruskal(): 
    
    edge_list = [(u, v, weights[(u, v)]) for u, v in edges]
     
    edge_list.sort(key=lambda x: x[2])

    uf = UnionFind(num_nodes)
    mst = []
    total_cost = 0
 
    for u, v, weight in edge_list:
        if uf.union(u, v):
            mst.append((u, v, weight))
            total_cost += weight

        if len(mst) == num_nodes - 1:
            break

    return mst, total_cost

def is_valid_mst(selected_edges, mst_cost): 
    total_cost = sum(weights[edge] for edge in selected_edges)
     
    if total_cost != mst_cost:
        return False, "Invalid MST! Cost mismatch!"
 
    parent = list(range(len(nodes)))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
 
    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            parent[rootY] = rootX
            return True
        return False
 
    for edge in selected_edges:
        u, v = edge
        if not union(u, v):
            return False, "Cycle detected! Invalid MST."

    return True, "Valid MST!"

