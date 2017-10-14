# Numbers
NUM_RUNS = 2
NUM_TRIALS_PER_RUN = 40
NUM_STEPS_PER_TRIAL = 4
# MRI stuff
TRIGGER = '5'
# Paths
LOG_FOLDER = 'log/'
# Times
STEP_TIMES = [0.5, 0.75, 1]
ITIS = [6, 7, 8]
ITI_PART1 = 3
# Distances (in pixel)
STEP_DISTANCE = 150  # TODO ?
LARGE_JITTER_MAX = 80  # TODO
SMALL_JITTER_MAX = 40  # TODO
# Instructions TODO
INSTR = 'Run #{} of ' + str(NUM_RUNS) + ' is starting soon.'
NEXT_RUN_INSTR = 'Waiting for the experimenter...'
