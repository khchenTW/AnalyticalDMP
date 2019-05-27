# Analytical Approaches for Deadline-Miss Probability
- This is the readme about the evaluations we did on DATE submission.
- The paper can be found in https://ieeexplore.ieee.org/document/8714908

- File structure:
1. algo folder has all the implementation regarding the adopted algorithms in evaluations, e.g., the Chernoff-bound [1] and the task-level convolution approaches [2].
2. evaluations folder has the evaluation script.
3. generator folder is for the task generation, which shouldn't be called unless it is necessary.
4. plots folder has the scripts to draw the figures used in the submission.
5. tasksets folder has the generated task sets.
6. results_short folder stores the final results used to plot the figures in the paper.

- Hint:
1. Just use plots scripts unless there is a new design to evaluate.
2. There is a multithread version of scripts for evaluating.
3. To use plot scripts, the scripts should be changed depending on the situation.

- More details is in readme.txt in the plots folder.

# Reference
[1] K. H. Chen and J. J. Chen, "Probabilistic schedulability tests for uniprocessor fixed-priority scheduling under soft errors" 2017 12th IEEE International Symposium on Industrial Embedded Systems (SIES), Toulouse, France, 2017, pp. 1-8.

[2] Georg von der Brüggen, Nico Piatkowski, Kuan-Hsun Chen, Jian-Jia Chen, Katharina Morik, "Efficiently Approximating the Probability of Deadline Misses in Real-Time Systems", ECRTS 2018: 6:1-6:22
