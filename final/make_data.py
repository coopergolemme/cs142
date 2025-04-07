import pandas as pd
import networkx as nx

DATA_DIR = 'processed_data'
bus_data = 'bus_data'




bus_data = pd.read_csv(f'{DATA_DIR}/bus_data.csv').applymap(lambda x: x.strip() if isinstance(x, str) else x)
load_data = pd.read_csv(f'{DATA_DIR}/load_data.csv').applymap(lambda x: x.strip() if isinstance(x, str) else x)
branch_data = pd.read_csv(f'{DATA_DIR}/branch_data.csv').applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Cast the 'I' and 'J' fields to integers

# Clean column names by stripping whitespace
bus_data.columns = bus_data.columns.str.strip()
branch_data.columns = branch_data.columns.str.strip()

bus_data['I'] = bus_data['I'].astype(int)
branch_data['I'] = branch_data['I'].astype(int)
branch_data['J'] = branch_data['J'].astype(int)

# Rename columns to remove invalid characters (e.g., spaces)
bus_data.rename(columns=lambda x: x.replace(" ", "_").replace("'", ""), inplace=True)
branch_data.rename(columns=lambda x: x.replace(" ", "_").replace("'", ""), inplace=True)



# Create a directed graph from the bus data
G = nx.DiGraph()


# Add nodes to the graph
for index, row in bus_data.iterrows():
    G.add_node(row['I'], **row.to_dict())

assert len(bus_data) == len(G.nodes), "Mismatch between bus data and graph nodes"

# Add edges to the graph
for index, row in branch_data.iterrows():
    # print(f"Adding edge from {row['I']} to {row['J']}")
    if row['I'] not in G.nodes:
        print(f"Node {row['I']} is not in the graph")
    if row['J'] not in G.nodes:
        print(f"Node {row['J']} is not in the graph")
    if row['I'] != row['J']:
        G.add_edge(row['I'], row['J'], **row.to_dict())
    else:
        print(f"Skipping self-loop for bus {row['I']}")

print(G.number_of_nodes())

# Export graph as GML
nx.write_gml(G, f'{DATA_DIR}/graph.gml')