import random
import numpy as np
import matplotlib.pyplot as plt
from numpy import *

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
    plt.axvline(x=0.25)
    plt.axvline(x=0.5)
    plt.axvline(x=0.75)
    plt.show()


'''
the ERM from the course site:
'''
def find_best_interval(xs, ys, k):
    assert all(array(xs) == array(sorted(xs))), "xs must be sorted!"

    xs = array(xs)
    ys = array(ys)
    m = len(xs)
    P = [[None for j in range(k + 1)] for i in range(m + 1)]
    E = zeros((m + 1, k + 1), dtype=int)

    # Calculate the cumulative sum of ys, to be used later
    cy = concatenate([[0], cumsum(ys)])

    # Initialize boundaries:
    # The error of no intervals, for the first i points
    E[:m + 1, 0] = cy

    # The minimal error of j intervals on 0 points - always 0. No update needed.

    # Fill middle
    for i in range(1, m + 1):
        for j in range(1, k + 1):
            # The minimal error of j intervals on the first i points:

            # Exhaust all the options for the last interval. Each interval boundary is marked as either
            # 0 (Before first point), 1 (after first point, before second), ..., m (after last point)
            options = []
            for l in range(0, i + 1):
                next_errors = E[l, j - 1] + (cy[i] - cy[l]) + concatenate(
                    [[0], cumsum((-1) ** (ys[arange(l, i)] == 1))])
                min_error = argmin(next_errors)
                options.append((next_errors[min_error], (l, arange(l, i + 1)[min_error])))

            E[i, j], P[i][j] = min(options)

    # Extract best interval set and its error count
    best = []
    cur = P[m][k]
    for i in range(k, 0, -1):
        best.append(cur)
        cur = P[cur[0]][i - 1]
        if cur == None:
            break
    best = sorted(best)
    besterror = E[m, k]

    # Convert interval boundaries to numbers in [0,1]
    exs = concatenate([[0], xs, [1]])
    representatives = (exs[1:] + exs[:-1]) / 2.0
    intervals = [(representatives[l], representatives[u]) for l, u in best]

    return intervals, besterror


plot_points(generate_m_pairs(100))