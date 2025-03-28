import random
import time
import networkx as nx
import matplotlib.pyplot as plt


def create_graph(nodes):
    graph = nx.complete_graph(nodes)
    return graph


def dijkstra(graph, startNode, endNode):
    try:
        result = nx.dijkstra_path(graph, source=startNode, target=endNode)
    except nx.NetworkXNoPath:
        print(f"No path found for the route of node {startNode} to {endNode}")


def bellmanFord(graph, startNode, endNode):
    try:
        result = nx.bellman_ford_path(graph, source=startNode, target=endNode)
    except nx.NetworkXNoPath:
        print(f"No path found for the route of node {startNode} to {endNode}")


class GraphPlotter:
    def plot_performance_stats(self, node_sizes, dijkstra_stats, bellmanford_stats, use_avg_only=False):

        dijkstra_avg_times = [stat['avg'] for stat in dijkstra_stats]
        bellmanford_avg_times = [stat['avg'] for stat in bellmanford_stats]

        plt.figure(figsize=(10, 6))
        plt.plot(dijkstra_avg_times, node_sizes, marker='o', label='Dijkstra')
        plt.plot(bellmanford_avg_times, node_sizes, marker='s', label='Bellman-Ford')

        plt.title('Number of Nodes vs Average Execution Time')
        plt.ylabel('Number of Nodes')
        plt.xlabel('Average Execution Time (ms)')
        plt.yscale('log')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def calculate_stats(times):
    avg = sum(times) / len(times)
    std_dev = (sum((x - avg) ** 2 for x in times) / len(times)) ** 0.5
    return {
        'min': min(times),
        'max': max(times),
        'avg': avg,
        'std': std_dev
    }


def main():
    node_sizes = [10, 100, 200, 500, 1000, 1500]
    iterations = 20

    dijkstra_stats = []
    bellmanford_stats = []

    for nodes in node_sizes:
        graph = create_graph(nodes)

        print(f"Graph size: {graph.number_of_nodes()} nodes")
        print(f"Graph size: {graph.number_of_edges()} edges")

        for j in range(nodes):
            graph.add_node(j, value=random.randint(1, 20))

        dijkstra_times = []
        bellmanford_times = []

        # Run performance tests
        for _ in range(iterations):
            start_point = random.randint(0, nodes - 1)
            end_point = random.randint(0, nodes - 1)

            # Measure Dijkstra time
            start_time = time.time()
            dijkstra(graph, start_point, end_point)
            end_time = time.time()
            dijkstra_times.append((end_time - start_time) * 1000)

            # Measure Bellman-Ford time
            start_time = time.time()
            bellmanFord(graph, start_point, end_point)
            end_time = time.time()
            bellmanford_times.append((end_time - start_time) * 1000)

        # Calculate and store stats
        dijkstra_stat = calculate_stats(dijkstra_times)
        bellmanford_stat = calculate_stats(bellmanford_times)

        dijkstra_stats.append(dijkstra_stat)
        bellmanford_stats.append(bellmanford_stat)

        # Print individual test results
        print(
            f"Dijkstra: Min={dijkstra_stat['min']:.2f}ms, Max={dijkstra_stat['max']:.2f}ms, Avg={dijkstra_stat['avg']:.2f}ms, Std={dijkstra_stat['std']:.2f}ms")
        print(
            f"Bellman-Ford: Min={bellmanford_stat['min']:.2f}ms, Max={bellmanford_stat['max']:.2f}ms, Avg={bellmanford_stat['avg']:.2f}ms, Std={bellmanford_stat['std']:.2f}ms")
        print()

    # Create plotter and plot results
    plotter = GraphPlotter()
    plotter.plot_performance_stats(node_sizes, dijkstra_stats, bellmanford_stats)


if __name__ == "__main__":
    main()