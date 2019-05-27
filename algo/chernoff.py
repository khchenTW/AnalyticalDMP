from __future__ import division
import scipy
from scipy.optimize import bisect
from scipy.optimize import newton
from scipy.optimize import minimize_scalar
from scipy.optimize import minimize
from scipy.optimize import root
from scipy.optimize import fsolve
from numpy import *
from sympy import symbols, sympify, lambdify, plot, limit, oo, diff, simplify

import mpmath as mp
from functools import wraps
import time
import random
import numpy as np
import sys, getopt
import os
import math

def findpoints(task, higher_priority_tasks, mode = 0):
    points = []
    if mode == 0: #kpoints
        # pick up k testing points here
        for i in higher_priority_tasks:
            point = math.floor(task['deadline']/i['deadline'])*i['deadline']
            if point > 0:
                points.append(point)
        points.append(task['deadline'])
    else: #allpoints
        for i in higher_priority_tasks:
            for r in range(1, int(math.floor(task['period']/i['period']))+1):
                point = r*i['period']
            if point > 0:
                points.append(point)
        points.append(task['deadline'])
    return points

'''
@method: Generates the log-moment generating function.
@param task: Task under analysis
@param other: Higher-priority tasks
@param interval: Time interval t under analysis
'''
def logmgf_tasks(task, other, interval):
    def logmgf_task(task, interval):
        num_jobs_realeased = int(math.ceil(float(interval)/task['period']))
        return str(num_jobs_realeased) + '*ln(' + '+'.join(('exp(' + str(event) + '*' + 's' + ')*' + str(probability)) for (event, probability) in task['pdf']) + ')'
    s = symbols('s')
    func = '(' + '+'.join(logmgf_task(tsk, interval) for tsk in (np.concatenate(([task], other)) if other is not None else [task])) + ') -' + 's*' + str(interval)
    func = lambdify(s, sympify(func), 'mpmath')
    return func

'''
@method: Finds argmin function within tolerance.
@param function: Convex function to be minimized.
@param a: Beginning of the interval under analysis.
@param b: Ending of the interval under analysis.
@param tolerance: Resolution of solution
'''
def goldensectionsearch(function, a, b, tolerance=1e-5):
    invphi = (math.sqrt(5) - 1)/2                                                                                                                   
    invphi2 = (3 - math.sqrt(5))/2
    (a,b) = (min(a,b), max(a,b))
    h = b - a
    if h <= tolerance:
        return (a,b)                                                                                                                  
    n = int(math.ceil(math.log(tolerance/h)/math.log(invphi)))
    c = a + invphi2 * h
    d = a + invphi * h
    yc = function(c)
    yd = function(d)
    for k in xrange(n-1):
        if yc < yd:
            b = d
            d = c
            yd = yc
            h = invphi*h
            c = a + invphi2 * h
            yc = function(c)
        else:
            a = c
            c = d
            yc = yd
            h = invphi*h
            d = a + invphi * h
            yd = function(d)
    if yc < yd:
        return d
    else:
        return b

'''
@method: Computes the minimal chernoff bound.
@param taskset: Taskset under analysis.
@param s_min: Beginning of interval under analysis.
@param s_max: Ending of interval under analysis.
@return list of deadline miss probabilities for each task in the task set and computation time
'''
def optimal_chernoff_taskset_all(taskset, s_min = 0, s_max = 10e100):
    results = []
    for i, task in enumerate(taskset):
        start_time = time.time()
        times = findpoints(task, taskset[:i])
        functions = (logmgf_tasks(task, taskset[:i], time) for time in times)
        candidates = []
        for function in functions:
            optimal = goldensectionsearch(function, s_min, s_max)   
            candidates.append((optimal, function(optimal)))
        optimal = candidates[np.argmin([x[1] for x in candidates])]
        elapsed_time = time.time() - start_time
        results.append({'s_opt' : optimal[0], 'ErrProb' : min(1.0, mp.exp(str(optimal[1]))), 'ms' : elapsed_time})
    return results

def optimal_chernoff_taskset_lowest(taskset, s_min = 0, s_max = 10e100):
    start_time = time.time()
    times = findpoints(taskset[-1], taskset[:-1])
    functions = (logmgf_tasks(taskset[-1], taskset[:-1], time) for time in times)
    candidates = []
    for function in functions:
        optimal = goldensectionsearch(function, s_min, s_max)   
        candidates.append((optimal, function(optimal)))
    optimal = candidates[np.argmin([x[1] for x in candidates])]
    elapsed_time = time.time() - start_time
    return {'s_opt' : optimal[0], 'ErrProb' : min(1.0, mp.exp(str(optimal[1]))), 'ms' : elapsed_time}
