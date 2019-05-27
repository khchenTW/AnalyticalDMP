#!/bin/bash

# python evaluations.py -i series_kuan -n 10 -s 100 -m 0.05 -f 0.025 -h 1.83 -r -q &
# sleep 1

# python evaluations.py -i series_kuan -n 20 -s 25 -m 0.05 -f 0.025 -h 1.83 -r -q &
# sleep 1

# python evaluations.py -i series_kuan -n 25 -s 50 -m 0.05 -f 0.025 -h 1.83 -r -q &
# sleep 1

# python evaluations.py -i series_kuan -n 50 -s 20 -m 0.05 -f 0.025 -h 1.83 -r -q &
# sleep 1

# python evaluations.py -i series_kuan -n 100 -s 10 -m 0.05 -f 0.025 -h 1.83 -r -q &
# sleep 1

# python evaluations.py -i special_kuan -n 1000 -s 1 -m 0.05 -f 0.025 -h 1.83 -r -q &
# sleep 1


python mp_evaluations.py -i special_kuan -n 100 -s 4 -m 0.05 -f 0.025 -h 1.83 -r -q &
sleep 1
# python mp_evaluations.py -i special_kuan -n 250 -s 4 -m 0.05 -f 0.025 -h 1.83 -r -q &
# sleep 1
# python mp_evaluations.py -i special_kuan -n 500 -s 4 -m 0.05 -f 0.025 -h 1.83 -r -q &
# sleep 1
# python mp_evaluations.py -i special_kuan -n 1000 -s 4 -m 0.05 -f 0.025 -h 1.83 -r -q &
# sleep 1

