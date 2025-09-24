import os
import numpy as np

def parse_edges(data):
    lines = data.strip().split('\n')
    edges = []
    verts = set()
    for line in lines:
        if line.strip():
            v1, v2 = line.split(',')
            v1 = v1.strip()
            v2 = v2.strip()
            verts.add(v1)
            verts.add(v2)
            edges.append((v1, v2))
    return edges, verts

def build_adjacency_matrix(edges, verts, eroot):
    other_verts = sorted(v for v in verts if v != eroot)
    ordered_verts = [eroot] + other_verts
    n = len(ordered_verts)
    vert_index = {v: i for i, v in enumerate(ordered_verts)}

    adj = np.zeros((n, n), dtype=bool)
    for v1, v2 in edges:
        i = vert_index[v1]
        j = vert_index[v2]
        adj[i, j] = True

    return adj, n

def compute_transitive_closure(adj, n):
    tranzitive_r = adj.copy()
    for _ in range(1, n):
        tranzitive_r = tranzitive_r | (tranzitive_r @ adj)
    return tranzitive_r

def create_relation_matrices(adj, transitive, n):
    r1_np = adj.astype(int)
    r2_np = r1_np.T
    r3_np = (transitive & ~adj).astype(int)
    r4_np = r3_np.T

    r2_bool = r2_np.astype(bool)
    r5_np = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if np.any(r2_bool[i] & r2_bool[j]):
                r5_np[i, j] = 1
                r5_np[j, i] = 1

    return r1_np, r2_np, r3_np, r4_np, r5_np

def main(v: str, eroot: str) -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]], list[list[int]]]:
    edges, verts = parse_edges(v)
    adj, n = build_adjacency_matrix(edges, verts, eroot)
    transitive = compute_transitive_closure(adj, n)
    matrices = create_relation_matrices(adj, transitive, n)

    return tuple(matrix.tolist() for matrix in matrices)

def read_input_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "task1.csv")
    with open(csv_path, "r") as file:
        return file.read()

def print_matrices(matrices):
    relations = ["r1 (управление)", "r2 (подчинение)", "r3 (опосредованное управление)",
                 "r4 (опосредованное подчинение)", "r5 (соподчинение)"]

    for rel_name, matrix in zip(relations, matrices):
        print(f"\nМатрица для отношения {rel_name}:")
        for row in matrix:
            print(row)

if __name__ == "__main__":
    input_data = read_input_file()
    eroot = input("Введите значение корневой вершины: ").strip()
    matrices = main(input_data, eroot)
    print_matrices(matrices)