import numpy as np
import opt_einsum as oe
import networkx as nx
import matplotlib.pyplot as plt
import cotengra as ctg

def solve_problem_15(N):
    """
    Solution by tensor network: The number of paths
    is expressed as the contraction value of a
    tensor network, where the edges take on binary
    values depending on whether an edge is
    contained in a path or not.
    """
    # Tensor shape: (North, East, South, West)
    T = np.zeros((2, 2, 2, 2))
    
    # Flow conservation: inflow = outflow (at most 1)
    T[0, 0, 0, 0] = 1.0
    T[1, 0, 1, 0] = 1.0  # N -> S
    T[1, 1, 0, 0] = 1.0  # N -> E
    T[0, 0, 1, 1] = 1.0  # W -> S
    T[0, 1, 0, 1] = 1.0  # W -> E

    # Boundary vectors
    v_zero = np.array([1.0, 0.0])  # State 0 (not traversed)
    v_one = np.array([0.0, 1.0])   # State 1 (traversed)

    G = nx.Graph()
    
    edge_counter = 1
    def new_edge():
        nonlocal edge_counter
        val = edge_counter
        edge_counter += 1
        return val

    horiz_edges = {}
    for i in range(N + 1):
        for j in range(N):
            horiz_edges[(i, j)] = new_edge()
            G.add_edge(f"T_{i}_{j}", f"T_{i}_{j+1}")

    vert_edges = {}
    for i in range(N):
        for j in range(N + 1):
            vert_edges[(i, j)] = new_edge()
            G.add_edge(f"T_{i}_{j}", f"T_{i+1}_{j}")

    operands = []

    for i in range(N + 1):
        for j in range(N + 1):
            tensor_name = f"T_{i}_{j}"
            G.add_node(tensor_name, pos=(j, -i), color='blue')

            # North
            if i == 0:
                n_edge = new_edge()
                is_start = (j == 0)
                vec = v_one if is_start else v_zero
                color = 'red' if is_start else 'yellow'
                bnd_name = f"B_N_{j}"
                G.add_node(bnd_name, pos=(j, 1), color=color)
                G.add_edge(tensor_name, bnd_name)
                operands.extend([vec, [n_edge]])
            else:
                n_edge = vert_edges[(i-1, j)]

            # East
            if j == N:
                e_edge = new_edge()
                bnd_name = f"B_E_{i}"
                G.add_node(bnd_name, pos=(N+1, -i), color='yellow')
                G.add_edge(tensor_name, bnd_name)
                operands.extend([v_zero, [e_edge]])
            else:
                e_edge = horiz_edges[(i, j)]

            # South
            if i == N:
                s_edge = new_edge()
                is_end = (j == N)
                vec = v_one if is_end else v_zero
                color = 'red' if is_end else 'yellow'
                bnd_name = f"B_S_{j}"
                G.add_node(bnd_name, pos=(j, -N-1), color=color)
                G.add_edge(tensor_name, bnd_name)
                operands.extend([vec, [s_edge]])
            else:
                s_edge = vert_edges[(i, j)]

            # West
            if j == 0:
                w_edge = new_edge()
                bnd_name = f"B_W_{i}"
                G.add_node(bnd_name, pos=(-1, -i), color='yellow')
                G.add_edge(tensor_name, bnd_name)
                operands.extend([v_zero, [w_edge]])
            else:
                w_edge = horiz_edges[(i, j-1)]

            operands.extend([T, [n_edge, e_edge, s_edge, w_edge]])

    # Contraction
    opt = ctg.ReusableHyperOptimizer(max_repeats=16, max_time=10, progbar=False)
    ans = oe.contract(*operands, optimize=opt)

    return int(round(float(ans))), G


def plot_tensor_network(G, N):
    pos = nx.get_node_attributes(G, 'pos')
    colors = [G.nodes[n]['color'] for n in G.nodes()]
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, node_color=colors, node_size=300, with_labels=False)

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Internal Tensor'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Path Start/End'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=10, label='Zero Boundary')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    plt.title(f"Project Euler 15 - Tensor Network Layout (N={N})")
    plt.axis('equal')
    plt.savefig('tn_plot.png')
    print("Saved tensor network plot to 'tn_plot.png'.")


if __name__ == "__main__":
    N = 20
    paths, G = solve_problem_15(N)
    print(f"Number of paths for a {N}x{N} grid: {paths}")
    plot_tensor_network(G, N)

