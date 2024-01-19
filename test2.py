import numpy as np
def funct():
    a = np.array([400,400,1])
    b = np.array([[1,0,200],
                [0,1,200],
                [0,0,1]])

    c  = np.dot(b,a)
    return c[0], c[1]

a, b = funct()

print(a)