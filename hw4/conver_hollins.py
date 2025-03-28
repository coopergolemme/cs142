import pandas as pd
import numpy as np
import os
import sys
import networkx as nx
from typing import Dict, List, Tuple


DATA_PATH = "data/hollins/hollins.dat"



def read_hollins_data() -> Tuple[Dict[str, str], List[Tuple[str, str]]]:
    """
    Read Hollins data from a file and convert it to a DataFrame.
    """
    # Check if the file exists
    if not os.path.exists(DATA_PATH):
        print(f"Error: The file {DATA_PATH} does not exist.")
        sys.exit(1)

    # Read the data from the file
    with open(DATA_PATH, 'r') as f:
        header_line = f.readline()
        lines = f.readlines()

    num_labels, num_edges = map(int, header_line.strip().split())
    # Check if the number of lines matches the expected number of edges
    
    assert len(lines) == num_edges + num_labels, f"Expected {num_edges + num_labels} lines, but got {len(lines)}"


    # Read the labels
    labels = {}
    for i in range(num_labels):
        line = lines[i].strip()
        key = line.split()[0]
        value = line.split()[1]
        labels[key] = value

    # Read the edges
    edges = []
    for i in range(num_labels, num_labels + num_edges):
        line = lines[i].strip()
        key = line.split()[0]
        value = line.split()[1]
        edges.append((key, value))
    
    return labels, edges 


def create_network(labels: Dict[str, str], edges: List[Tuple[str, str]]) -> nx.Graph:
    """
    Create a networkx directed graph from the labels and edges.
    """
    G = nx.DiGraph()
    
    # Add nodes with labels
    for key, value in labels.items():
        G.add_node(int(key), label=value)
    
    # Add edges
    for edge in edges:
        G.add_edge(int(edge[0]), int(edge[1]))

    assert G.number_of_nodes() == len(labels), f"Expected {len(labels)} nodes, but got {G.number_of_nodes()}"
    assert G.number_of_edges() == len(edges), f"Expected {len(edges)} edges, but got {G.number_of_edges()}"

    
    return G



def node_to_label_mapping(G: nx.Graph) -> Dict[int, str]:
    """
    Create a mapping from node IDs to labels.
    """
    mapping = {}
    for node in G.nodes(data=True):
        mapping[node[0]] = node[1]['label']
    return mapping


# print("Reading Hollins data...")
# labels, edges = read_hollins_data()
# print("Data read successfully.")


# print("Creating network...")
# G = create_network(labels, edges)
# print("Network created.")

# # Save the graph to a file
# output_file = "hollins_graph.csv"
# nx.write_edgelist(G, output_file, delimiter=',', data=["label"])
# print(f"Graph saved to {output_file}.")

