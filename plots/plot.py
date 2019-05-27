from __future__ import division

import sys, time, getopt
import numpy as np
import matplotlib.pyplot as plt
import itertools
import matplotlib
# matplotlib.use('Agg')
# plt.switch_backend('Agg')
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
from os import listdir
from os.path import isfile, join
import mpmath as mp

mp.dps = 15

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True
rcParams['text.usetex'] = True
rcParams["figure.figsize"] = (17,15)

def plot_datasets(datasets, view):
    figlabel = itertools.cycle(('a','b','c','d','e','f','g','h','i'))
    marker = itertools.cycle(('o', 'v','*','D','x','+'))
    colors = itertools.cycle(('c','r','b','g','r','y','y','b'))
    names = []
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust (top = 0.5, bottom = 0.2, left = 0.1, right = 0.95, hspace = 0.3, wspace=0.05)
    ax.set_xlabel('Utilization (\%)',size=35)
    ax.set_ylabel('Average runtime (sec)',size=35)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor = 'w', top = 'off', bottom = 'off', left = 'off', right = 'off')

    for dataset in datasets:
        utilization = [val[1] for val in dataset]
        chernoff = [val[2] for val in dataset]
        george = [val[3] for val in dataset]

        if view == 'prob':
            utilization = [val[1] for val in dataset]
            chernoff = [val[2] for val in dataset]
            george = [val[3] for val in dataset]
            ax.axis([-2, 102, -0.02, 1.02])
            ax.set_ylabel('Average DMP',size=35)
        elif view == 'prob_log':
            utilization = [val[1] for val in dataset[-10:]]
            chernoff = [val[2] for val in dataset[-10:]]
            george = [val[3] for val in dataset[-10:]]
            # ax.axis([-2, 102, -0.02, 1.02])
            #ax.set_ylim([10**-400,10**10])
            ax.set_yscale("log")
            ax.set_xlim([-2, 102])
            ax.set_ylabel('Average DMP (log-scale)',size=35)
        else:
            # autoscale
            max_value = max(max(george), max(chernoff))
            ax.axis([-2,102,-2, max_value + 5])
            ax.set_ylabel('Average runtime (sec)',size=35)

        ax.plot(utilization, chernoff, '-', color = colors.next(), marker = marker.next(), markersize = 15, fillstyle = 'none', markevery = 1, label = 'chernoff', linewidth = 2.5)
        names.append('Rescaling ' + '(' + str(float(dataset[0][0])*100) + '\%)')
        ax.plot(utilization, george, '-', color = colors.next(), marker = marker.next(), markersize = 15, fillstyle = 'none', markevery = 1, label = 'prune', linewidth = 2.5)
        names.append('Pruning ' + '(' + str(float(dataset[0][0])*100) + '\%)')
        ax.tick_params(labelcolor='k', top='off', bottom='off', left='off', right='off')

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(25)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(25)

    #plt.title(title)
    ax.grid()
    ax.legend(names, bbox_to_anchor=(0.95, 1.3),
                                loc=5,
                                ncol=3,
                                markerscale = 1.5,
                            borderaxespad=0.,framealpha=1,
                            prop={'size':30})
    #plt.show()
    return fig

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:n:s:m:f:h:rv:", ["ident=", "num_tasks=", "num_sets=", "max_fault_rate=", "fault_rate_step_size=", "hard_task_factor=", "rounded", "view="])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    num_tasks, num_sets, max_fault_rate, step_size_fault_rate, hard_task_factor = 0, 0, 0, 0, 0
    ident, view, title = None, None, None
    rounded = False

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
        if opt in ('-v', '--view'):
            view = str(arg)

    datasets = []
    for fault_rate in np.arange(step_size_fault_rate, max_fault_rate + step_size_fault_rate, step_size_fault_rate):
        dataset = []
        for utilization in np.arange(5, 100, 5):
            if ident is not None:
                filename_chernoff = 'res_chernoff_tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + str('r' if rounded else '')
                filename_george = 'res_george_tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + str('r' if rounded else '')
                try:
                    results_chernoff = np.load('../results/' + filename_chernoff + '.npy')
                    results_george = np.load('../results/' + filename_george + '.npy')
                    if view == 'time':
                        dataset.append([fault_rate, utilization, sum([result['ms'] for result in results_chernoff])/num_sets, sum([result['ms'] for result in results_george])/num_sets])
                    elif view == 'prob':
                        dataset.append([fault_rate, utilization, sum([result['ErrProb'] for result in results_chernoff])/num_sets, sum([result['ErrProb'] for result in results_george])/num_sets])
                    elif view == 'prob_log':
                        dataset.append([fault_rate, utilization, sum([result['ErrProb'] for result in results_chernoff])/num_sets, sum([result['ErrProb'] for result in results_george])/num_sets])
                    elif view == 'diff':
                        cherrnoff_err = [result['ErrProb'] for result in results_chernoff]
                        george_err = [result['ErrProb'] for result in results_george]
                        errors = []
                        for i in range(len(cherrnoff_err)):
                            errors.append(cherrnoff_err[i]-george_err[i])
                        print errors
                        dataset.append([fault_rate, utilization, errors])
                except Exception as e:
                    continue
            else:
                print 'Must specify identifier'
                return
        datasets.append(dataset)
    plot = plot_datasets(datasets, view)
    #save_pdf = PdfPages('/home/khchen/Dropbox/figures/'+ ident  + '_' + str(view) + '.pdf')
    save_pdf = PdfPages(ident  + '_' + str(view) + '.pdf')
    save_pdf.savefig(plot, bbox_inches='tight', pad_inches=0.0)
    save_pdf.close()

if __name__=="__main__":
    main()
