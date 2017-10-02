import operator
import random
import pickle

DIR = 'design_2/'
NUM_STIMULI = 4
STIMULUS_DURATION = 3.0


file_names = ['stimulus_{}.txt'.format(i) for i in range(NUM_STIMULI)] + ['ITIs.txt']
design = {}
for i, filename in enumerate(file_names):
    with open(DIR + filename, 'r') as iti_file:
        design[file_names[i][:-4]] = [float(time) for time in iti_file.read().split('\n') if len(time) > 1]


def get_order(stimuli_onset_lists):
    # stimuli_onset_lists: a list of lists of stimuli onsets
    order, onsets = [], []
    indexes = [0 for _ in range(len(stimuli_onset_lists))]
    current_onsets = [stimuli_onset_lists[stim_i][0] for stim_i in range(len(stimuli_onset_lists))]
    for onset_list in stimuli_onset_lists:
        onset_list.append(float('inf'))
    while True:
        stim_i, min_onset = min(enumerate(current_onsets), key=operator.itemgetter(1))
        if min_onset == float('inf'):
            return order, onsets
        order.append(stim_i)
        onsets.append(min_onset)
        indexes[stim_i] += 1
        current_onsets[stim_i] = stimuli_onset_lists[stim_i][indexes[stim_i]]


def check_iti(onsets, itis):
    # TODO this is temporary and supposed to be wrong if neurodesign gives correct output...
    assert(len(onsets) == len(itis))
    assert(itis[0] == 0)
    for i in range(len(onsets) - 1):
        assert(onsets[i] + STIMULUS_DURATION + itis[i + 1] == onsets[i + 1])
    print('ITIs match stimuli onsets.')


stim_order, all_onsets = get_order([design[k[:-4]] for k in file_names[:-1]])
check_iti(all_onsets, design['ITIs'])
design['ITIs'].append(0.0)

### random baseline ###
# stim_order = [0 for _ in range(10)] + [1 for _ in range(10)] + [2 for _ in range(10)] + [3 for _ in range(10)]
# random.shuffle(stim_order)
# design['ITIs'] = [float(random.randint(6, 8)) for _ in range(40)]
# design['ITIs'][0] = 0.0
# with open(DIR + 'rand_ITIs.txt', 'w') as outfile:
#     outfile.write('\n'.join([str(iti) for iti in design['ITIs']]))
### random baseline ###

# rand_stim_durations = [float(random.randint(2, 4)) for _ in range(len(stim_order))]
# real_stim_onsets = [[] for _ in range(NUM_STIMULI)]
# time = 0.0
# for i in range(len(stim_order)):
#     real_stim_onsets[stim_order[i]].append(str(time))
#     time += rand_stim_durations[i] + float(design['ITIs'][i + 1])
#
# # txt for AFNI
# for i in range(NUM_STIMULI):
#     with open(DIR + 'real_stimulus_{}.txt'.format(i), 'w') as outfile:
#         outfile.write('\n'.join(real_stim_onsets[i]))
#
# with open(DIR + 'real_stim_durations.txt', 'w') as outfile:
#     outfile.write('\n'.join([str(t) for t in rand_stim_durations]))

#######################

with open(DIR + 'real_stim_durations.txt', 'r') as infile:
    rand_stim_durations = infile.read().split('\n')
step_times = [float(stim_time) / 4 for stim_time in rand_stim_durations]

# pickle for experiment
trials = [{'stim': stim_order[i],
           'step_time': step_times[i],
           'iti': int(design['ITIs'][i + 1])}
          for i in range(len(stim_order))]

with open('saccades_design2.pkl', 'w') as outfile:
    pickle.dump(trials, outfile)

# with open('saccades_design1.pkl', 'r') as outfile:
#     d1 = pickle.load(outfile)
# with open('saccades_design2.pkl', 'r') as outfile:
#     d2 = pickle.load(outfile)
# with open('saccades_design.pkl', 'w') as outfile:
#     pickle.dump(d1, outfile)
#     pickle.dump(d2, outfile)
