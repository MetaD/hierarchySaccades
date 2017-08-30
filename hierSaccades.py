#!/usr/bin/env python

#
# A skeleton file for PsychoPy experiments
# Author: Meng Du
# August 2017
#

from psychopy_util import *
from config import *
import random


def show_one_trial():
    pass


def validation(items):
    # check empty field
    for key in items.keys():
        if items[key] is None or len(items[key]) == 0:
            return False, str(key) + ' cannot be empty.'
    # check age
    try:
        if int(items['Age']) <= 0:
            raise ValueError
    except ValueError:
        return False, 'Age must be a positive integer'
    # everything is okay
    return True, ''


if __name__ == '__main__':
    # subject ID dialog
    sinfo = {'ID': '', 'Mode': ['Test', 'Exp']}
    show_form_dialog(sinfo, validation, order=['ID', 'Gender', 'Age', 'Mode'])
    sid = int(sinfo['ID'])

    # create logging file
    infoLogger = DataLogger(LOG_FOLDER, str(sid) + '.log', 'info_logger', logging_info=True)
    # create window
    presenter = Presenter(fullscreen=(sinfo['Mode'] == 'Exp'), info_logger='info_logger')

    # show instructions
    presenter.show_instructions(INSTR_BEGIN)
    # show trials
    for t in range(NUM_TRIALS):
        show_one_trial()
    # end of experiment
    presenter.show_instructions(INSTR_END)
    infoLogger.logger.info('End of experiment')
