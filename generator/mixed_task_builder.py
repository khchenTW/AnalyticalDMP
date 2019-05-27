'''
Author: Georg von der Brueggen, Kuan-Hsun Chen
'''

from __future__ import division
import random
import math
import numpy
import sort_task_set

def pdfForm(tasks):
    allTasks=[]
    for task in tasks:
        task['pdf'] = [(task['execution'], 1-task['prob']), (task['abnormal_exe'], task['prob'])]
        allTasks.append(task)
    return sort_task_set.sort(allTasks, 'period');

def mixed_task_set(tasks, factor, rate):
    allTasks=[]
    for task in tasks:
        task['abnormal_exe']=task['execution']*factor
        task['prob']=rate
        allTasks.append(task)
    return sort_task_set.sort(allTasks, 'period');


def hardtaskWCET(tasks, hardTaskWCETFactor, rate):
    allTasks=[]
    for i in range(len(tasks)):
        pos=random.randint(0, len(tasks)-1)
        task=tasks[pos]
        task['abnormal_exe']=task['execution']*hardTaskWCETFactor
        task['type']='hard'
        task['prob']=rate
        allTasks.append(task)
        del tasks[pos]
    return sort_task_set.sort(allTasks, 'period');

def taskGeneration(tasks, hardTasks, softTasks, hardTaskPercentage, hardTaskWCETFactor, softTaskWCETFactor):
    #print len(tasks)
    numberOfHardTasks = (hardTaskPercentage / 100 * len(tasks))
    #print numberOfHardTasks
    allTasks=[]
    for i in range(int(numberOfHardTasks)):
        pos=random.randint(0, len(tasks)-1)
        task=tasks[pos]
        task['abnormal_exe']=task['execution']*hardTaskWCETFactor
        task['type']='hard'
        hardTasks.append(task)
        allTasks.append(task)
        del tasks[pos]
    for task in tasks:
        task['abnormal_exe']=task['execution']*softTaskWCETFactor
        task['type']='soft'
        softTasks.append(task)
        allTasks.append(task)
    allTasks=hardTasks+softTasks
    hardTasks=sort_task_set.sort(hardTasks, 'period')
    softTasks=sort_task_set.sort(softTasks, 'period')
    return sort_task_set.sort(allTasks, 'period')
