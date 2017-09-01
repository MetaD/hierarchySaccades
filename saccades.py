#!/usr/bin/env python

#
# A skeleton file for PsychoPy experiments
# Author: Meng Du
# August 2017
#

from psychopy_util import *
from config import *
import random


def show_one_trial(color, duration, pos):
    presenter.show_two_fixations(duration=duration, color=color, pos=pos)


def validation(items):
    # check empty field
    for key in items.keys():
        if items[key] is None or len(items[key]) == 0:
            return False, str(key) + ' cannot be empty.'
    # everything is okay
    return True, ''


def randomization():
    times, positions = [], []
    distances = presenter.pixel2norm(DISTANCE)
    dist_jitters = presenter.pixel2norm(DISTANCE_MAX_JITTER)
    for _ in range(NUM_BLOCKS):
        # times
        tmp_num = (NUM_TRIALS_PER_BLOCK - NUM_TRIALS_PER_BLOCK / 3) / 2
        block_times = [FIXATION_TIMES[1] for _ in range(NUM_TRIALS_PER_BLOCK / 3)] + \
                      [FIXATION_TIMES[0] for _ in range(tmp_num)] + \
                      [FIXATION_TIMES[2] for _ in range(tmp_num)]
        assert(len(block_times) == NUM_TRIALS_PER_BLOCK)
        random.shuffle(block_times)
        times.append(block_times)
        # positions
        block_pos = [(0 + random.randint(-dist_jitters[0], dist_jitters[0]),
                      distances[1] + random.randint(-dist_jitters[1], dist_jitters[1]))
                     for _ in range(NUM_TRIALS_PER_BLOCK / 2)] + \
                    [(distances[0] + random.randint(-dist_jitters[0], dist_jitters[0]),
                      0 + random.randint(-dist_jitters[1], dist_jitters[1]))
                     for _ in range(NUM_TRIALS_PER_BLOCK / 2)]
        assert(len(block_pos) == NUM_TRIALS_PER_BLOCK)
        random.shuffle(block_pos)
        positions.append(block_pos)
    return times, positions


if __name__ == '__main__':
    # subject ID dialog
    sinfo = {'ID': '', 'Mode': ['Test', 'Exp']}
    show_form_dialog(sinfo, validation, order=['ID', 'Mode'])
    sid = int(sinfo['ID'])

    # create log file
    infoLogger = DataLogger(LOG_FOLDER, str(sid) + '.log', 'info_logger', logging_info=True)
    # create window
    presenter = Presenter(fullscreen=(sinfo['Mode'] == 'Exp'), info_logger='info_logger')

    # show instructions
    presenter.show_instructions(INSTR_BEGIN)
    # get trial sequences
    time_seq, pos_seq = randomization()
    # show trials
    for b in range(NUM_BLOCKS):
        infoLogger.logger.info('Block ' + str(b))
        for t in range(NUM_TRIALS_PER_BLOCK):
            show_one_trial(color=RED, duration=time_seq[b][t], pos=pos_seq[b][t])
        for t in range(NUM_TRIALS_PER_BLOCK):
            show_one_trial(color=GREEN, duration=time_seq[b][t], pos=pos_seq[b][t])
    # end of experiment
    presenter.show_instructions(INSTR_END)
    infoLogger.logger.info('End of experiment')
