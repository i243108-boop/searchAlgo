import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math

coords = {
    "Baggage_Area": (0, 0),
    "Security": (3, 2),
    "Check_In": (2, 5),
    "Food_Court": (5, 4),
    "Gate_A": (7, 3),
    "Departure_Gate": (10, 6)
}

edges = [
    ("Baggage_Area", "Security", 4),
    ("Baggage_Area", "Check_In", 6),
    ("Security", "Food_Court", 3),
    ("Check_In", "Food_Court", 2),
    ("Food_Court", "Gate_A", 3),
    ("Gate_A", "Departure_Gate", 4),
    ("Food_Court", "Departure_Gate", 5)
]

def h(node, goal):
    x1, y1 = coords[node]
    x2, y2 = coords[goal]
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def search(algo, start, goal):
    if algo == "GBFS":
        pq = [(h(start, goal), 0, start, None)]
    else:
        pq = [(h(start, goal), 0, start, None)]
    
    visited = {}
    parent = {}
    
    while pq:
        f, g, current, came_from = heapq.heappop(pq)
        if current in visited:
            continue
        visited[current] = g
        parent[current] = came_from
        
        if current == goal:
            break
        
        for u, v, cost in edges:
            if u == current and v not in visited:
                new_g = g + cost
                new_h = h(v, goal)
                new_f = new_h if algo == "GBFS" else new_g + new_h
                heapq.heappush(pq, (new_f, new_g, v, current))
    
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent.get(node)
    path.reverse()
    return path, visited.get(goal, 0)

st.title("Search Visualizer")

start = st.selectbox("Start Node", list(coords.keys()))
goal = st.selectbox("Goal Node", list(coords.keys()))
algo = st.selectbox("Algorithm", ["GBFS", "A*"])

if st.button("Run"):
    path, cost = search(algo, start, goal)
    
    G = nx.DiGraph()
    for u, v, c in edges:
        G.add_edge(u, v, weight=c)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw(G, coords, with_labels=True, ax=ax,
            node_color="lightblue", node_size=2000, arrows=True)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, coords, edge_labels=labels, ax=ax)
    
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, coords, edgelist=path_edges,
                            edge_color="red", width=3, arrows=True, ax=ax)
    st.pyplot(fig)
    
    st.write("Algorithm:", algo)
    st.write("Path:", " -> ".join(path))
    st.write("Cost:", cost)