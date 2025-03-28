import networkx as nx
from conver_hollins import read_hollins_data, create_network, node_to_label_mapping
from blog import create_blogs_network
def nx_page_rank(G: nx.Graph):
    """
    Calculate PageRank using NetworkX.
    """

    pr = nx.pagerank(G, alpha=0.85)


    return pr


def top_k_page_rank(pr: dict, k: int):
    """
    Get the top k PageRank values.
    """

    return sorted(pr.items(), key=lambda x: x[1], reverse=True)[:k]

def bottom_k_page_rank(pr:dict, k:int):
    return sorted(pr.items(), key=lambda x : x[1], reverse=False)[:k]


def my_page_rank(G: nx.Graph, alpha: float = 0.85, max_iter: int = 100, tol: float = 1.0e-6):
    """
    Calculate PageRank using the power iteration method.
    """
    # Initialize PageRank values
    pr = {node: 1.0 / len(G) for node in G.nodes()}
    N = len(G)
    dangling_nodes = [node for node in G.nodes() if G.out_degree(node) == 0]
    print(len(dangling_nodes), "dangling nodes")

    # Power iteration
    for _ in range(max_iter):
        new_ranks = {}
        for node in G.nodes():
            rank_sum = sum(pr[neighbor] / G.out_degree(neighbor) for neighbor in G.predecessors(node))
            new_ranks[node] = (1 - alpha) / N + alpha * rank_sum
        # Handle dangling nodes
        dangling_sum = alpha * sum(pr[node] for node in dangling_nodes) / N
        for node in G.nodes():
            new_ranks[node] += dangling_sum
        # Check for convergence
        if all(abs(new_ranks[node] - pr[node]) < tol for node in G.nodes()):
            break
        pr = new_ranks

    return pr

def personalized_page_rank(G: nx.Graph, personal_node, alpha: float = 0.85, steps: int = 20):
    """
    Calculate personalized PageRank with random restarts.
    """

    pr = {node: 0.0 for node in G.nodes()}
    pr[personal_node] = 1.0
    N = len(G)
    dangling_nodes = [node for node in G.nodes() if G.out_degree(node) == 0]

    for _ in range(steps):
        new_ranks = {node: 0.0 for node in G.nodes()}
        for node in G.nodes():
            rank_sum = sum(pr[neighbor] / G.out_degree(neighbor) for neighbor in G.predecessors(node))
            new_ranks[node] = alpha * rank_sum
        # Handle dangling nodes
        dangling_sum = alpha * sum(pr[node] for node in dangling_nodes) / N
        for node in G.nodes():
            new_ranks[node] += dangling_sum
        # Random restart to personal_node with 20% probability
        for node in G.nodes():
            new_ranks[node] = 0.9 * new_ranks[node] + 0.1 * (1 if node == personal_node else 0)
        pr = new_ranks

    return pr

def hollins_page_rank():

    labels, edges = read_hollins_data();

    G = create_network(labels, edges)

    ntl = node_to_label_mapping(G)


    print("Calculating PageRank...")
    # Calculate PageRank
    pr = nx_page_rank(G)
    my_pr = my_page_rank(G, max_iter=1000)
    # print(pr)
    print("PageRank calculated.")
    print("Top 10 PageRank values:")
    # Get the top 10 PageRank values
    top_10_pr = top_k_page_rank(pr, 10)
    for node, value in top_10_pr:
        print(f"Node: {node}, PageRank: {value}, Label: {ntl[node]}")

    print("Top 10 PageRank values using my implementation:")
    # Get the top 10 PageRank values
    top_10_my_pr = top_k_page_rank(my_pr, 10)
    for node, value in top_10_my_pr:
        print(f"Node: {node}, PageRank: {value}, Label: {ntl[node]}")

    # # print(my_pr)
    # with open('p1.txt', "w") as f:
    #     f.writelines([f'{ntl[node]} \t {pr}\n' for node, pr  in my_pr.items()])


    print("Bottom 10 page rank")


    bottom_10_my_pr = bottom_k_page_rank(my_pr, 10)
    for node, value in bottom_10_my_pr:
        print(f"Node: {node}, PageRank: {value}, Label: {ntl[node]}")

def political_page_rank():
    G = create_blogs_network()
    page_rank = nx_page_rank(G)
    my_page_ran = my_page_rank(G)

    top_5 = top_k_page_rank(page_rank, 5)
    top_5_my = top_k_page_rank(my_page_ran, 5)
    print("Top 5 PageRank values:")
    for node, value in top_5:
        print(f"Node: {node}, PageRank: {value}")

    print("Top 5 PageRank values using my implementation:")
    for node, value in top_5_my:
        print(f"Node: {node}, PageRank: {value}")

    bottom_5 = bottom_k_page_rank(my_page_ran, 5)
    print("Bottom 5 PageRank values using my implementation:")
    for node, value in bottom_5:
        print(f"Node: {node}, PageRank: {value}")
        


    with open('p2.txt', "w") as f:
        f.writelines([f'{node} \t {pr}\n' for node, pr  in page_rank.items()])

def political_personalized_page_rank():
    nodes_start = ["dailykosc",  "atriosblo", "wonkettec", "talkleftc", "juancolec", "powerlineb", "realclearp", "blogsforbu", "instapundi", "michellema"]
    G = create_blogs_network()
    personalized_pr = {}
    for node in nodes_start:
        pr = nx.pagerank(G, alpha=0.85, personalization={node: 1.0})
        personalized_pr[node] = pr

    with open('p3.txt', 'w') as f:
        header = "\t" + "\t".join(nodes_start) + "\n"
        f.write(header)
        for node in nodes_start:
            row = node + "\t" + "\t".join(str(personalized_pr[start_node].get(node, 0.0)) for start_node in nodes_start) + "\n"
            f.write(row)
        # print(f"Top 5 PageRank values for {node}:")
        # for node, value in top_5:
            # print(f"Node: {node}, PageRank: {value}")
    


if __name__ == "__main__":
    # hollins_page_rank()
    political_page_rank()
    # political_personalized_page_rank()
    # political_page_rank()
