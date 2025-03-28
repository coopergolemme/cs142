import networkx as nx

def create_blogs_network():

    DATA_DIR  = 'data/'


    with open(DATA_DIR + 'blogs.dl', 'r') as f:
        lines = f.readlines()

    num_labels = int(lines[1].split("=")[1])
    node_labels = []
    # print(lines[4])
    for i in range(num_labels):
        node_labels.append(lines[4 + i].replace("\n", "").replace("\"", ""))

    assert len(node_labels) == num_labels

    G = nx.DiGraph()

    G.add_nodes_from(node_labels)

    start_adj = num_labels  * 2 + 6

    curr_line = lines[start_adj]
    i = start_adj


    while curr_line != "!\n":
        if(curr_line.endswith("0\n")):
            i += 1

        else:
            v_1= int(curr_line.split(" ")[1])
            v_2= int(curr_line.split(" ")[2])
            G.add_edge(node_labels[v_1-1], node_labels[v_2-1])
            i+=1

        curr_line = lines[i]
    return G
