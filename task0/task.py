def main(csv_graph: str) -> list[list[int]]:
    lines = csv_graph.strip().split('\n')
    edges = []
    vertices = set()

    for line in lines:
        if line.strip():
            start, end = line.strip().split(',')
            start_vertex = int(start)
            end_vertex = int(end)
            edges.append((start_vertex, end_vertex))
            vertices.add(start_vertex)
            vertices.add(end_vertex)

    vertex_list = sorted(list(vertices))
    n = len(vertex_list)
    vertex_to_index = {vertex: i for i, vertex in enumerate(vertex_list)}

    matrix = [[0 for _ in range(n)] for _ in range(n)]

    for start_vertex, end_vertex in edges:
        i = vertex_to_index[start_vertex]
        j = vertex_to_index[end_vertex]
        matrix[i][j] = 1

    return matrix


test_csv = """1,2
1,3
3,4
3,5"""

result = main(test_csv)
for row in result:
    print(row)
