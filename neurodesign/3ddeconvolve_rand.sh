#!/bin/tcsh

3dDeconvolve -nodata 379 1              \
    -num_stimts 4                       \
    -polort A                           \
    -stim_times 1 rand_stimulus_0.txt 'GAM'  \
    -stim_label 1 stim0                 \
    -stim_times 2 rand_stimulus_1.txt 'GAM'  \
    -stim_label 2 stim1                 \
    -stim_times 3 rand_stimulus_2.txt 'GAM'  \
    -stim_label 3 stim2                 \
    -stim_times 4 rand_stimulus_3.txt 'GAM'  \
    -stim_label 4 stim3                 \
    -x1D X.xmat.1D -xjpeg X.jpg         \
    -x1D_uncensored X.nocensor.xmat.1D
