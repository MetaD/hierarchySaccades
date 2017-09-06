#!/usr/bin/env python

#
# A skeleton file for PsychoPy experiments
# Author: Meng Du
# August 2017
#

from psychopy_util import *
from saccades_config import *
import random

"""
Assumptions:
- Horizontal/Vertical jitters are randomly picked from a range
- The second part of ITI (a "+" at the center) is also considered the beginning of the next trial
    - So participants don't actually know when the iti begins?
- Waiting for a trigger only at the end of ITI
"""


def random_position(direction, step_num):
    if direction == 'u':
        return (0 + random.uniform(-small_jitters[0], small_jitters[0]),
                step_num * step_distances[1] + random.uniform(-large_jitters[1], large_jitters[1]))
    if direction == 'd':
        return (0 + random.uniform(-small_jitters[0], small_jitters[0]),
                -step_num * step_distances[1] + random.uniform(-large_jitters[1], large_jitters[1]))
    if direction == 'r':
        return (step_num * step_distances[0] + random.uniform(-large_jitters[0], large_jitters[0]),
                0 + random.uniform(-small_jitters[1], small_jitters[1]))
    if direction == 'l':
        return (-step_num * step_distances[0] + random.uniform(-large_jitters[0], large_jitters[0]),
                0 + random.uniform(-small_jitters[1], small_jitters[1]))


def show_one_trial(step_time, iti, direction):
    infoLogger.logger.info('Starting saccade')
    # center fixation
    presenter.show_fixation(duration=step_time)
    # saccades
    pos = 0
    for step in range(1, NUM_STEPS_PER_TRIAL + 1):
        pos = random_position(direction, step)
        presenter.show_fixation(duration=step_time, pos=pos)
    # ITI part 1
    infoLogger.logger.info('End of saccade, starting ITI')
    half_iti = float(iti)/2
    presenter.show_fixation(duration=half_iti, pos=pos)
    # ITI part 2
    presenter.show_fixation(duration=int(half_iti), wait_trigger=True) # todo
    infoLogger.logger.info('End of ITI')


def validation(items):
    # check empty field
    for key in items.keys():
        if items[key] is None or len(items[key]) == 0:
            return False, str(key) + ' cannot be empty.'
    # everything is okay
    return True, ''


def randomization():
    directions = ['u' for _ in range(NUM_TRIALS_PER_RUN)] + ['d' for _ in range(NUM_TRIALS_PER_RUN)] + \
                 ['r' for _ in range(NUM_TRIALS_PER_RUN)] + ['l' for _ in range(NUM_TRIALS_PER_RUN)]
    random.shuffle(directions)
    return directions


if __name__ == '__main__':
    # subject ID dialog
    sinfo = {'ID': '', 'Mode': ['Exp', 'Test']}
    show_form_dialog(sinfo, validation, order=['ID', 'Mode'])
    sid = int(sinfo['ID'])

    # create log file
    infoLogger = DataLogger(LOG_FOLDER, str(sid) + '_saccades.log', 'info_logger', logging_info=True)
    # create window
    serial = SerialUtil(SERIAL_PORT, BAUD_RATE, logger='info_logger')
    presenter = Presenter(fullscreen=(sinfo['Mode'] == 'Exp'), info_logger='info_logger', serial=serial) # todo
    # lengths in normalized units
    step_distances = presenter.pixel2norm(STEP_DISTANCE)
    small_jitters = presenter.pixel2norm(SMALL_JITTER_MAX)
    large_jitters = presenter.pixel2norm(LARGE_JITTER_MAX)

    # get trial sequences TODO
    # show trials
    for r in range(NUM_RUNS):
        dir_seq = randomization()
        presenter.show_instructions('', next_page_text=None, duration=1, wait_trigger=True)  # TODO time between runs?
        infoLogger.logger.info('Run ' + str(r))
        for t in range(NUM_TRIALS_PER_RUN):
            show_one_trial(step_time=random.choice(STEP_TIMES), iti=random.choice(ITIS), direction=dir_seq[t])  # TODO not random?
    # end of experiment
    infoLogger.logger.info('End of experiment')
