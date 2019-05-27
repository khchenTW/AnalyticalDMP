from __future__ import division

import sys, time, getopt
import numpy as np
import matplotlib.pyplot as plt
import itertools
import matplotlib
# matplotlib.use('Agg')
plt.switch_backend('Agg')
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
rcParams["figure.figsize"] = (20,15)

def giveMeBrief(datasets, utilization):
    for dataset in datasets:
        num_tasks = [val[1] for val in dataset]
        print num_tasks
        chernoff = [val[2] for val in dataset]
        print chernoff
        george = [val[3] for val in dataset]
        print george

def plot_datasets(datasets, view, utilization):
    figlabel = itertools.cycle(('a','b','c','d','e','f','g','h','i'))
    marker = itertools.cycle(('o', 'v','*','D','x','+'))
    colors = itertools.cycle(('c','r','b','g','r','y','y','b'))
    names = []
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust (top = 0.5, bottom = 0.2, left = 0.1, right = 0.95, hspace = 0.3, wspace=0.05)
    ax.set_ylabel('Average runtime (sec)',size=35)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor = 'w', top = 'off', bottom = 'off', left = 'off', right = 'off')

    width = 0.25
    # ax.set_xticks(ind+1*width, ('10', '15', '20', '25'))
    for dataset in datasets:
        num_tasks = [val[1] for val in dataset]
        # print num_tasks
        chernoff = [val[2] for val in dataset]
        # print chernoff
        george = [val[3] for val in dataset]
        # print george

        if view == 'prob':
            num_tasks = [val[1] for val in dataset]
            chernoff = [val[2] for val in dataset]
            george = [val[3] for val in dataset]
            # ax.axis([-2, 102, -0.02, 1.02])
            ax.set_ylabel('Calculated DMP',size=25)
            plt.xticks(ind+1*width, ('10', '15', '20', '25'))
        elif view == 'prob_log':
            # print dataset
            s_opts_pre = [val[1] for val in dataset]
            chernoff_pre = [val[2] for val in dataset]
            george_pre = [val[3] for val in dataset]

            s_opts = []
            chernoff = []
            george = []

            print len(george_pre)
            #pre-checking
            for s, c, g in zip(s_opts_pre, chernoff_pre, george_pre):
                # if g > 10**-300:
                if g > 10**-300:
                    s_opts.append(s)
                    chernoff.append(c)
                    george.append(g)
            print len(george)
            # ax.axis([-2, 102, -0.02, 1.02])
            #ax.set_ylim([10**-400,10**10])
            ax.set_yscale("log")
            if utilization == 50:
                plt.ylim([10**-300,10**5])
            # if utilization == 50:
            # else:
            #     pass
            ax.set_ylabel('Calculated DMP (log-scale)',size=25)
            # ax.set_xlabel('Sets with 20 Tasks',size=25)
            # print len(chernoff)

            labels = []
            for ind in range(len(chernoff)):
                if utilization == 50:
                    labels.append('Set'+str(ind))
                else:
                    labels.append('S'+str(ind))

            ind = np.arange(len(chernoff))
            plt.xticks(ind+0.5*width, labels)

            bar_chern = ax.bar(ind, chernoff, width, label = 'Chernoff', alpha=0.8)
            names.append('Chernoff ' + '(' + str(float(dataset[0][0])*100) + '\%)')
            bar_georg = ax.bar(ind+width, george, width,  label = 'Prune', alpha=0.8)
            names.append('Pruning ' + '(' + str(float(dataset[0][0])*100) + '\%)')
            ax.tick_params(labelcolor='k', top='off', bottom='off', left='off', right='off')

            for rect, s in zip(bar_chern, s_opts):
                height = rect.get_height()
                # print height
                if height > 10**-100:
                    plt.text(rect.get_x()+rect.get_width()/2.0, height, '%.3f' % s, ha='center', va='bottom', fontsize=15)
                else:
                    plt.text(rect.get_x()+rect.get_width()/2.0, 10**-96, '%.3f' % s, ha='center', va='bottom', fontsize=15)

        else:
            ind = np.arange(4)
            # autoscale
            # max_value = max(max(george), max(chernoff))
            # print george, chernoff
            # ax.axis([-2,102,-2, max_value + 5])
            #ax.set_ylim(-2, max_value + 5)
            ax.set_yscale("log")
            plt.ylim([10**-2,10**5])
            ax.set_ylabel('Average runtime (sec)',size=35)
            ax.set_xlabel('Number of Tasks',size=35)
            plt.xticks(ind+1*width, ('10', '15', '20', '25'))

            ax.bar(ind, chernoff, width, label = 'chernoff', alpha=0.8)
            print chernoff
            names.append('Chernoff ' + '(' + str(float(dataset[0][0])*100) + '\%)')
            ax.bar(ind+width, george, width,  label = 'prune', alpha=0.8)
            print george
            names.append('Pruning ' + '(' + str(float(dataset[0][0])*100) + '\%)')
            ax.tick_params(labelcolor='k', top='off', bottom='off', left='off', right='off')

    if utilization == 70:
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(25)
    else:
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(25)


    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(25)

    #plt.title(title)
    ax.grid()
    if utilization == 70 and view == 'prob_log':
        return fig
    ax.legend(names, bbox_to_anchor=(0.95, 0.9),
                                loc=5,
                                ncol=3,
                                markerscale = 1.5,
                            borderaxespad=0.,framealpha=1,
                            prop={'size':25})


    #plt.show()
    return fig

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:u:s:m:f:h:rv:", ["ident=", "utilization=", "num_sets=", "max_fault_rate=", "fault_rate_step_size=", "hard_task_factor=", "rounded", "view="])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    # num_tasks,
    num_sets, max_fault_rate, step_size_fault_rate, hard_task_factor = 0, 0, 0, 0
    ident, view, title = None, None, None
    rounded = False

    utilization = 50
    #utilization = 70
    for opt, arg in opts:
        if opt in ('-i', '--ident'):
            ident = str(arg)
        # if opt in ('-n', '--num_tasks'):
        #     num_tasks = int(arg)
        if opt in ('-u', '--utilization'):
            utilization = int(arg)
        # if opt in ('-s', '--num_sets'):
        #     num_sets = int(arg)
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
    fault_rate = 0.025
    # for fault_rate in np.arange(step_size_fault_rate, max_fault_rate + step_size_fault_rate, step_size_fault_rate):
    dataset = []
    # setting for Figure 3 and 4
    # for num_tasks, num_sets in zip([10, 15, 20, 25], [100, 50, 25, 5]):
    # setting for Figure 5
    for num_tasks, num_sets in zip([20], [25]):
    # setting for Special
    # for num_tasks, num_sets in zip([100], [4]):
        if ident is not None:
            filename_chernoff = 'res_chernoff_tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + str('r' if rounded else '')
            filename_george = 'res_george_tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + str('r' if rounded else '')
            try:
                results_chernoff = np.load('../results_short/' + filename_chernoff + '.npy')
                # print results_chernoff
                results_george = np.load('../results_short/' + filename_george + '.npy')
                # print results_george
                if view == 'brief':
                    print [result['ms'] for result in results_chernoff]
                    print [fault_rate, num_tasks, sum()/num_sets, 1]
                    print "hello:"
                    dataset.append([fault_rate, num_tasks, sum([result['ms'] for result in results_chernoff])/num_sets, sum([result['ms'] for result in results_chernoff])/num_sets])
                # print results_chernoff, results_george
                if view == 'time':
                    dataset.append([fault_rate, num_tasks, sum([result['ms'] for result in results_chernoff])/num_sets, sum([result['ms'] for result in results_george])/num_sets])
                elif view == 'prob':
                    dataset.append([fault_rate, num_tasks, sum([result['ErrProb'] for result in results_chernoff])/num_sets, sum([result['ErrProb'] for result in results_george])/num_sets])
                elif view == 'prob_log':
                    # if num_tasks == 20:
                        for res_chern, res_georg in zip(results_chernoff, results_george):
                            # print res_chern, res_georg
                            # print res_chern['s_opt']
                            if (res_chern['s_opt']<9999):
                                dataset.append([fault_rate, res_chern['s_opt'], res_chern['ErrProb'], res_georg['ErrProb']])
                    # else:
                    #     pass

            except Exception as e:
                print e
                continue
        else:
            print 'Must specify identifier'
            return
    datasets.append(dataset)
    if view == 'brief':
        giveMeBrief(datasets, utilization)
    else:
        plot = plot_datasets(datasets, view, utilization)        
        save_pdf = PdfPages(ident  + '_' + str(view) + '.pdf')
        save_pdf.savefig(plot, bbox_inches='tight', pad_inches=0.0)
        save_pdf.close()

if __name__=="__main__":
    main()
