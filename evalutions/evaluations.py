from __future__ import division

import sys, time, getopt
import numpy as np

sys.path.append('../')
from algo import george, chernoff


def george_inlined_all(taskset, failure_rate):
    start_time = time.time()
    for i in range(1, len(taskset)):
        probs, states, pruned = [], [], []
        results_george = george.calculate_prune(taskset[:i], failure_rate, probs, states, pruned)
    elapsed_time = (time.time() - start_time)
    return {'ErrProb' : results_george, 'ms' : elapsed_time}

def george_inlined_lowest(taskset, failure_rate):
    start_time = time.time()
    probs, states, pruned = [], [], []
    results_george = george.calculate_prune(taskset, failure_rate, probs, states, pruned)
    elapsed_time = (time.time() - start_time)
    return {'ErrProb' : results_george, 'ms' : elapsed_time}

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:n:s:m:f:h:rq", ["ident=", "num_tasks=", "num_sets=", "max_fault_rate=", "fault_rate_step_size=", "hard_task_factor=", "rounded", "quick"])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    num_tasks, num_sets, max_fault_rate, step_size_fault_rate, hard_task_factor = 0, 0, 0, 0, 0
    ident = None
    rounded = False
    quick = False

    for opt, arg in opts:
        if opt in ('-i', '--ident'):
            ident = str(arg)
        if opt in ('-n', '--num_tasks'):
            num_tasks = int(arg)
        if opt in ('-s', '--num_sets'):
            num_sets = int(arg)
        if opt in ('-m', '--max_fault_rate'):
            max_fault_rate = min(1.0, float(arg))
        if opt in ('-f', '--fault_rate_step_size'):
            step_size_fault_rate = min(1.0, float(arg))
        if opt in ('-h', '--hard_task_factor'):
            hard_task_factor = float(arg)
        if opt in ('-r', '--rounded'):
            rounded = True
        if opt in ('-q', '--quick'):
            quick = True

    if quick is False:
        for fault_rate in np.arange(step_size_fault_rate, max_fault_rate + step_size_fault_rate, step_size_fault_rate):
            print 'Evaluating: %d tasksets, %d tasks, fault probability: %f, rounded: %r' % (num_sets, num_tasks, fault_rate, rounded)
            for utilization in np.arange(5, 100, 5):
                try:
                    if ident is not None:
                        filename = 'tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + str('r' if rounded else '')
                        try:
                            tasksets = np.load('../tasksets/' + filename + '.npy')
                        except:
                            raise Exception, "Could not read"
                        results_chernoff = []
                        results_george = []
                        for taskset in tasksets:
                            results_chernoff.append(chernoff.optimal_chernoff_taskset_all(taskset))
                            results_george.append(george_inlined_all(taskset, max_fault_rate))
                        np.save('../results/res_chernoff_' + filename + '.npy', results_chernoff)
                        np.save('../results/res_george_' + filename + '.npy', results_george)
                    else:
                        raise Exception, "Please specify an identifier!"
                except IOError:
                    print 'Could not write filename %s' % filename
    else:
        for fault_rate in np.arange(step_size_fault_rate, max_fault_rate + step_size_fault_rate, step_size_fault_rate):
            print 'Evaluating: %d tasksets, %d tasks, fault probability: %f, rounded: %r' % (num_sets, num_tasks, fault_rate, rounded)
            #for utilization in np.arange(5, 100, 5):
            #for utilization in np.arange(50, 55, 20):
            for utilization in np.arange(70, 75, 20):
                try:
                    if ident is not None:
                        filename = 'tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + str('r' if rounded else '')
                        try:
                            tasksets = np.load('../tasksets_short/' + filename + '.npy')
                        except:
                            raise Exception, "Could not read"
                        results_chernoff = []
                        results_george = []
                        for taskset in tasksets:
                            print 'Computing chernoff bounds'
                            results_chernoff.append(chernoff.optimal_chernoff_taskset_lowest(taskset))
                            print 'Computing George'
                            # results_george.append(george_inlined_lowest(taskset, max_fault_rate))
                            results_george.append(1)
                        np.save('../results_short/res_chernoff_' + filename + '.npy', results_chernoff)
                        np.save('../results_short/res_george_' + filename + '.npy', results_george)
                    else:
                        raise Exception, "Please specify an identifier!"
                except IOError:
                    print 'Could not write filename %s' % filename

if __name__=="__main__":
    main()
    print "DONE!"
