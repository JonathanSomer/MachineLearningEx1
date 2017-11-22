import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy import *
from intervals import *

######################################
# Helper functions
######################################

def generate_m_pairs(m):
    points = []

    for i in range(m):
        points.append(generate_pair())

    return points

'''
Draws a pair of points (x,y) according to the required distribution
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
Returns X and Y sorted by Xs value
'''
def X_Y_from_points(points):
    # sort by Xs
    sorted_points = sorted(points, key=lambda pair: pair[0])
    X = [point[0] for point in sorted_points]
    Y = [point[1] for point in sorted_points]
    return X, Y

'''
Receives an array of (x,y) and plots!
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
        plt.plot(interval, [0.5,0.5], 'm', linewidth=10, c=current_color)

    plt.show()

'''
Calculates the true error for the distribution in the exercise
given a hypothesis (as a set of intervals)

The algorithm:
1. Split all segments that cross 0.25, 0.5, 0.75
2. Sum segments length of each type:
    a. [0, 0.25] or x in [0.5, 0.75]: these are 0.8 chance to be 1 segmemts
    b. [0.25, 0.5] or x in [0.75, 1]: these are 0.1 chance to be 1 segments

3. Sum: (error chance per each segment type * segment length)
    note: the segment length is also the chance of a point to be in the segment
    (since X is uniformally distributed and the whole domain's length is 1)
'''
def true_error(intervals):
    # 1. split all segments that cross 0.25, 0.5, 0.75
    crossing_intervals = [interval for interval in intervals if is_crossing(interval)]
    non_crossing_intervals = [interval for interval in intervals if not is_crossing(interval)]

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

'''
Returns true iff the interval is crossing either one of 0.25, 0.5, 0.75
'''
def is_crossing(interval):
    return interval_crosses_x(interval, 0.25) or interval_crosses_x(interval, 0.5) or interval_crosses_x(interval, 0.75)

'''
Returns true iff the interval is crossing a certain value x
'''
def interval_crosses_x(interval, x):
    return interval[0] <= x <= interval[1]

'''
Splits intervals that cross into 2 separated intervals
'''
def split_crossing_interval(interval):
    if interval_crosses_x(interval, 0.25):
        return [(interval[0], 0.25), (0.25, interval[1])]
    elif interval_crosses_x(interval, 0.5):
        return [(interval[0], 0.5), (0.5, interval[1])]
    else:
        return [(interval[0], 0.75), (0.75, interval[1])]

'''
Calculates the empirical error given the intervals and points 
'''
def empirical_error(intervals, points):
    error = 0.0
    for point in points:
        is_in_interval = False
        for interval in intervals:
            if interval[0] <= point[0] <= interval[1]:
                is_in_interval = True
        if (point[1] == 0 and is_in_interval) or (point[1] == 1 and not is_in_interval):
            error += 1
    return error / len(points)

######################################
# Below are the subquestions functions
######################################

def part_A():
    plot_points(generate_m_pairs(100))

def part_C():
    k = 2 # number of intervals
    T = 100 # times
    Ms = []
    true_errors = []
    empirical_errors = []

    for m in range(10, 50, 5):
        true_errors_sum = 0
        empirical_errors_sum = 0

        for i in range(T):
            points = generate_m_pairs(m)
            X, Y = X_Y_from_points(points)
            intervals, besterror = find_best_interval(X, Y, k) # not really going to use this besterror
            empirical_errors_sum += empirical_error(intervals, points=points)
            print("empirical error for " + str(m) + " is: " + str(empirical_error(intervals, points=points)))
            true_errors_sum += true_error(intervals)

        Ms.append(m)
        true_errors.append(true_errors_sum/T)
        empirical_errors.append(empirical_errors_sum/T)

    # plot m against true error
    plt.plot(Ms, true_errors)
    plt.show()

    # plot m against empirical error
    plt.plot(Ms, empirical_errors)
    plt.show()

def part_D():
    points = generate_m_pairs(50)
    X, Y = X_Y_from_points(points)
    empirical_errors = []
    true_errors = []
    Ks = []

    for k in range(1,20):
        intervals, besterror = find_best_interval(X, Y, k)
        empirical_errors.append(empirical_error(intervals, points))
        true_errors.append(true_error(intervals))
        Ks.append(k)

    # plot k against true error
    plt.plot(Ks, true_errors)
    plt.xlabel("k (intervals)")
    plt.ylabel("True Error")
    plt.show()

    # plot k against empirical error
    plt.plot(Ks, empirical_errors)
    plt.ylabel("Empirical Error")
    plt.show()

def part_E():
    # generate additional holdout validation samples
    holdout_samples = generate_m_pairs(50)
    holdX, holdY = X_Y_from_points(holdout_samples)

    # perform holdout validation

######################################
# Input arguments handling
######################################

if len(sys.argv) != 2:
    print "Please specify the part you wish to initiate.\nValid arguments: -a, -c, -d, -e"

else:
    input = sys.argv[1]
    parts = {
        '-a' : part_A,
        '-c' : part_C,
        '-d' : part_D,
        '-e' : part_E
    }

    if input not in parts:
        print "Invalid argument"
    else:
        parts[input]()
