from data_conversion_util import list2csv
import os
from datetime import datetime


DATA_DIR = '../log/'


def append_duration(logfile, block_end_line, events, task_time, last_block=False):
    assert 'End of fixations' in logfile[block_end_line]
    assert ('Showing instructions' in logfile[block_end_line + 1]) != last_block
    block_end_time = datetime.strptime(logfile[block_end_line][:23], '%Y-%m-%d %H:%M:%S,%f')
    duration = round((block_end_time - task_time).total_seconds()) - events[-1][0]
    events[-1].append(duration)


header = ['onset', 'block_type', 'duration']
for datafile in os.listdir(DATA_DIR):
    if 'localizer.log' not in datafile or datafile[0] != '1':
        continue
    sid = datafile[:3]
    with open(DATA_DIR + datafile, 'r') as infile:
        logfile = infile.readlines()[38:]

    events = [header]
    task_time = None
    for i, line in enumerate(logfile):
        if 'Block' not in line:
            continue
        if task_time is not None:  # not the first block
            append_duration(logfile, i - 5, events, task_time)
        block_type = line[-10:].strip()
        block_time = datetime.strptime(line[:23], '%Y-%m-%d %H:%M:%S,%f')
        if task_time is None:
            task_time = block_time
        block_onset = (block_time - task_time).total_seconds()
        int_block_onset = round(block_onset)
        assert block_onset - int_block_onset < 0.01
        events.append([int_block_onset, block_type])
    append_duration(logfile, -12, events, task_time, last_block=True)

    filename = 'sub-%s_task-loca_event.tsv' % sid
    list2csv(events, filename, delimiter='\t')
