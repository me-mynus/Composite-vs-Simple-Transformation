import numpy as np

c_matrix = ([[1,0,200],[0,1,200],[0,0,1]])

polygon_vertices = np.array([
    [400, 400],
    [800, 400],
    [800, 800],
    [400, 800]
])

def transformed_matrix_calculation(polygon, composite_matrix):
    dummy = polygon.copy()
    for points in dummy:
        print(points)
        o_vertex = np.array([points[0], points[1], 1])
        transformed = np.dot(composite_matrix, o_vertex)
        points[0], points[1] = transformed[0], transformed[1]
        print("Here", transformed)
    return dummy

output = transformed_matrix_calculation(polygon_vertices, c_matrix) 
print(output)