import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
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
returns X and Y sorted by Xs value
'''
def X_Y_from_points(points):
    # sort by Xs
    sorted_points = sorted(points, key=lambda tup: tup[0])
    X = [point[0] for point in sorted_points]
    Y = [point[1] for point in sorted_points]
    return X, Y


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



'''
(a)

receives an array of (x,y)
and plots!
'''
def plot_points(points):
    X, Y = X_Y_from_points(points)

    plt.plot(X, Y, 'ro')
    plt.axis([-0.1, 1.1, -0.1, 1.1])
    plt.axvline(x=0.25)
    plt.axvline(x=0.5)
    plt.axvline(x=0.75)

    #plot segmemts:
    intervals, best_error = find_best_interval(X, Y, 2)

    for interval in intervals:
        current_color = np.random.rand(3,1)
        plt.axvline(x=interval[0], c=current_color, linewidth=5)
        plt.axvline(x=interval[1], c=current_color, linewidth=5)
        # plt.plot(interval, [0.5,0.5], 'm', linewidth=10, c=current_color)

    plt.show()


'''
WRITE THIS IN LATEX!!!

(b)
The best hypothesis gives:
    x in [0, 0.25] or x in [0.5, 0.75] -> 1
    x in [0.25, 0.5] or x in [0.75, 1] -> 0
'''


'''
calculates the true error for the distribution in the exercise
given a hypothesis (as a set of intervals)

the algorithm:
1. split all segments that cross 0.25, 0.5, 0.75
2. sum segments length of each type:
    a. [0, 0.25] or x in [0.5, 0.75]: these are 0.8 chance to be 1 segmemts
    b. [0.25, 0.5] or x in [0.75, 1]: these are 0.1 chance to be 1 segments

3. sum: (error chance per each segment type * segment length)
    note: the segment length is also the chance of a point to be in the segment 
    (since X is uniformally distributed and the whole domain's length is 1)  
'''
def true_error(intervals):

    # 1. split all segments that cross 0.25, 0.5, 0.75
    crossing_intervals = [ interval for interval in intervals if is_crossing(interval)]
    non_crossing_intervals = [ interval for interval in intervals if not is_crossing(interval)]

    for interval in crossing_intervals:
        non_crossing_intervals.extend(split_crossing_interval(interval))

    # 2. sum segments length by type
    total_08_intervals_length = total_01_intervals_length = 0
    for interval in intervals:
        current_interval_length = interval[1] - interval[0]
        if (interval[0] >= 0 and interval[1] <= 0.25) or (interval[0] >= 0.5 and interval[1] <= 0.75):
            total_08_intervals_length += current_interval_length
        else:
            total_01_intervals_length += current_interval_length

    # sum error over segment types:
    error = 0
    error += 0.2 * total_08_intervals_length
    error += 0.8 * (0.5 - total_08_intervals_length)
    error += 0.9 * total_01_intervals_length
    error += 0.1 * (0.5 - total_01_intervals_length)

    return error




def is_crossing(interval):
    return interval_crosses_x(interval, 0.25) or interval_crosses_x(interval, 0.5) or interval_crosses_x(interval, 0.75)


def interval_crosses_x(interval, x):
    return interval[0] <= x and interval[1] >= x


def split_crossing_interval(interval):
    if interval_crosses_x(interval, 0.25):
        return [(interval[0], 0.25), (0.25, interval[1])]
    elif interval_crosses_x(interval, 0.5):
        return [(interval[0], 0.5), (0.5, interval[1])]
    else:
        return [(interval[0], 0.75), (0.75, interval[1])]




plot_points(generate_m_pairs(100))

