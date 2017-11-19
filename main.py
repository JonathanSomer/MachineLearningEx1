import random
import numpy as np
import matplotlib.pyplot as plt


def generate_m_pairs(m):
    points = []

    for i in range(m):
        points.append(generate_pair())

    return points




'''
draw a pair of points x,y according to the required distribution
'''
def generate_pair():
    x = generate_x()
    y = generate_y_given_x(x)
    return x, y


'''
X is distributed uniformally on [0,1]
'''
def generate_x():

    return random.uniform(0,1)


''' 
Y is distributed: 
0.8 if x in [0, 0.25] or x in [0.5, 0.75]
0.1 if x in [0.25, 0.5] or x in [0.75, 1]
'''
def generate_y_given_x(x):

    # a temporary number used to decide which value to give y
    p = random.uniform(0, 1)

    if (0 <= x and x <= 0.25) or ( 0.5 <= x and x <= 0.75):
        if p <= 0.8:
            y = 1
        else:
            y = 0
    else:
        if p <= 0.1:
            y = 1
        else:
            y = 0
    return y


'''
receives an array of (x,y)
and plots!
'''
def plot_points(points):
    X = [point[0] for point in points]
    Y = [point[1] for point in points]
    plt.plot(X, Y, 'ro')
    plt.axis([-0.1, 1.1, -0.1, 1.1])
    plt.show()

plot_points(generate_m_pairs(100))