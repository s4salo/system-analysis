import json
import numpy as np


def load_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read().strip()
        return data


def compute_kernel(ranking_a, ranking_b):
    list_a = json.loads(ranking_a)
    list_b = json.loads(ranking_b)

    objects_set = set()
    for ranking in [list_a, list_b]:
        for cluster in ranking:
            if not isinstance(cluster, list):
                cluster = [cluster]
            objects_set.update(cluster)

    if not objects_set:
        return []
    max_obj = max(objects_set)

    def create_position_matrix(ranking):
        positions = [0] * max_obj
        pos_counter = 0
        for cluster in ranking:
            if not isinstance(cluster, list):
                cluster = [cluster]
            for obj in cluster:
                positions[obj - 1] = pos_counter
            pos_counter += 1

        matrix = np.zeros((max_obj, max_obj), dtype=int)
        for i in range(max_obj):
            for j in range(max_obj):
                if positions[i] >= positions[j]:
                    matrix[i, j] = 1
        return matrix

    matrix_a = create_position_matrix(list_a)
    matrix_b = create_position_matrix(list_b)

    product_matrix = matrix_a * matrix_b

    transposed_a = matrix_a.T
    transposed_b = matrix_b.T
    transposed_product = transposed_a * transposed_b

    kernel_pairs = []
    for i in range(max_obj):
        for j in range(i + 1, max_obj):
            if product_matrix[i, j] == 0 and transposed_product[i, j] == 0:
                kernel_pairs.append([i + 1, j + 1])

    return kernel_pairs


data_a = load_json_data('range_a.json')
data_b = load_json_data('range_b.json')
data_c = load_json_data('range_c.json')

print("СРАВНЕНИЕ РАНЖИРОВОК")
print("range_a.json vs range_b.json")
kernel_ab = compute_kernel(data_a, data_b)
print(f"Ядро противоречий: {kernel_ab}")

print("\nrange_a.json vs range_c.json")
kernel_ac = compute_kernel(data_a, data_c)
print(f"Ядро противоречий: {kernel_ac}")

print("\nrange_b.json vs range_c.json")
kernel_bc = compute_kernel(data_b, data_c)
print(f"Ядро противоречий: {kernel_bc}")