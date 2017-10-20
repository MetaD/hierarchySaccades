from psychopy_util import Presenter, DataLogger
import timeit
import time
import os

if os.path.isfile('log/test.log'):
   os.remove('log/test.log')
info_logger = DataLogger('log/', 'test.log', 'info_logger', True)
presenter = Presenter(fullscreen=False, info_logger='info_logger', trigger='5')


def foo():
    presenter.draw_stimuli_for_duration([], 1, True)


print timeit.timeit(foo, number=50)
