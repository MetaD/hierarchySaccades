from data_conversion_util import list2csv
import os
import pickle


with open('../saccades_design.pkl', 'r') as infile:
    run_seqs = [pickle.load(infile), pickle.load(infile)]  # {'step_time': 1.0, 'stim': 2, 'iti': 6}

sid_list = [datafile[:3] for datafile in os.listdir('../log/')
            if 'saccades.log' in datafile and datafile[0] == '1']

directions = ['up', 'down', 'right', 'left']
header = ['onset', 'duration', 'direction', 'iti']
for sid in sid_list:
    for i, run in enumerate(run_seqs):
        events = [header]
        time = 4.0  # first saccade
        for trial in run:
            duration = trial['step_time'] * 4
            direction = directions[trial['stim']]
            events.append([time, duration, direction, trial['iti']])
            time += duration + trial['iti']
        events[-1][3] = 10  # last ITI in run

        filename = 'sub-%s_task-sacc_run-0%d_event.tsv' % (sid, i + 1)
        list2csv(events, filename, delimiter='\t')
