#!/bin/bash

# EXPERIMENT 1
# echo 'Plotting Experiment 1'
# python plot.py -i series_kuan -n 10 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v time
# sleep 1
# python plot.py -i series_kuan -n 10 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v prob
# sleep 1
# python plot.py -i series_kuan -n 10 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v prob_log
# sleep 1

# EXPERIMENT for DATE figures:
echo 'plotting DATE experiments'
# python plot_short.py -i series_kuan -u 50 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v time
sleep 1
python plot_short.py -i series_kuan -u 50 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v prob_log
sleep 1

# python plot_short.py -i series_kuan -u 70 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v time
sleep 1
python plot_short.py -i series_kuan -u 70 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v prob_log
sleep 1

# EXPERIMENT 3
#echo 'Plotting Experiment 3'
#python plot.py -i series_kuan -n 10 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v time
#sleep 1
#python plot.py -i series_kuan -n 10 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v prob
#sleep 1

# EXPERIMENT 4
#echo 'Plotting Experiment 4'
#python plot.py -i series_kuan -n 10 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v time
#sleep 1
#python plot.py -i series_kuan -n 10 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -v prob
#sleep 1

cp *.pdf ../../Paper/figures/
