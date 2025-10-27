import os
import numpy as np
import math
from typing import Tuple, List, Set


def calculate_entropy(matrices: List[np.ndarray]) -> Tuple[float, float]:
    n = matrices[0].shape[0]
    total_entropy = 0.0

    for matrix in matrices:
        for i in range(n):
            for j in range(n):
                if i != j:
                    probability = matrix[i, j] / (n - 1)
                    if probability > 0:
                        total_entropy += probability * math.log2(probability)

    entropy_H = -total_entropy
    max_entropy = (1 / math.e) * n * len(matrices)
    normalized_h = entropy_H / max_entropy if max_entropy > 0 else 0

    return entropy_H, normalized_h


def create_edge_permutations(original_edges: List[Tuple[str, str]], vertices: List[str]) -> List[List[Tuple[str, str]]]:
    n = len(vertices)
    all_possible_edges = []

    # Generate all possible directed edges
    for source_idx in range(n):
        for target_idx in range(n):
            if source_idx != target_idx:
                all_possible_edges.append((vertices[source_idx], vertices[target_idx]))

    original_edges_set = set(original_edges)
    available_new_edges = [edge for edge in all_possible_edges if edge not in original_edges_set]

    permutations_list = []

    # Generate permutations by replacing each original edge with a new one
    for edge_to_replace_idx in range(len(original_edges)):
        for new_edge in available_new_edges:
            modified_edges = original_edges.copy()
            modified_edges[edge_to_replace_idx] = new_edge
            permutations_list.append(modified_edges)

    return permutations_list


def process_input_data(input_string: str, root_vertex: str) -> Tuple[float, float]:
    lines = input_string.strip().split('\n')
    edge_list = []
    vertex_set = set()

    # Parse input data
    for line in lines:
        if line.strip():
            vertex1, vertex2 = line.split(',')
            vertex1 = vertex1.strip()
            vertex2 = vertex2.strip()
            vertex_set.add(vertex1)
            vertex_set.add(vertex2)
            edge_list.append((vertex1, vertex2))

    # Organize vertices with root first
    other_vertices = sorted(vertex for vertex in vertex_set if vertex != root_vertex)
    ordered_vertices = [root_vertex] + other_vertices
    vertex_count = len(ordered_vertices)
    vertex_to_index = {vertex: idx for idx, vertex in enumerate(ordered_vertices)}

    # Generate all edge permutations
    all_edge_permutations = create_edge_permutations(edge_list, ordered_vertices)

    best_entropy = -float('inf')
    best_normalized_entropy = 0
    optimal_edges = None

    # Evaluate each permutation
    for edge_permutation in all_edge_permutations:
        # Create adjacency matrix
        adjacency_matrix = np.zeros((vertex_count, vertex_count), dtype=bool)
        for source, target in edge_permutation:
            source_idx = vertex_to_index[source]
            target_idx = vertex_to_index[target]
            adjacency_matrix[source_idx, target_idx] = True

        # Define relation matrices
        r1_matrix = adjacency_matrix.astype(int)
        r2_matrix = r1_matrix.T

        # Compute transitive closure
        transitive_closure = adjacency_matrix.copy()
        for _ in range(1, vertex_count):
            transitive_closure = transitive_closure | (transitive_closure @ adjacency_matrix)

        r3_matrix = (transitive_closure & ~adjacency_matrix).astype(int)
        r4_matrix = r3_matrix.T

        # Compute common predecessors matrix
        r2_bool = r2_matrix.astype(bool)
        r5_matrix = np.zeros((vertex_count, vertex_count), dtype=int)
        for i in range(vertex_count):
            for j in range(i + 1, vertex_count):
                if np.any(r2_bool[i] & r2_bool[j]):
                    r5_matrix[i, j] = 1
                    r5_matrix[j, i] = 1

        matrix_collection = [r1_matrix, r2_matrix, r3_matrix, r4_matrix, r5_matrix]

        current_entropy, current_normalized = calculate_entropy(matrix_collection)

        if current_entropy > best_entropy:
            best_entropy = current_entropy
            best_normalized_entropy = current_normalized
            optimal_edges = edge_permutation.copy()

    if optimal_edges:
        print(f"\nOptimal edge permutation found:")
        print(f"Original edges: {edge_list}")
        print(f"Modified edges: {optimal_edges}")

    return best_entropy, best_normalized_entropy


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_directory, "task2.csv")

    with open(csv_file_path, "r") as input_file:
        csv_content = input_file.read()

    root_node = input("Enter root vertex: ").strip()
    entropy_H, normalized_h = process_input_data(csv_content, root_node)

    print(f"\nResults:")
    print(f"H(M,R) = {entropy_H:.4f}")
    print(f"h(M,R) = {normalized_h:.4f}")