"""
Use the subprocess module to interact with lsf-related programs.
This could be done better using something like pyLSF
to access the LSF API directly.
"""

import getpass
import re
import subprocess
from subprocess import PIPE

class LSFError(Exception): pass

def nonempty_stripped_lines(lines):
    for raw_line in lines:
        line = raw_line.strip()
        if line:
            yield line

def bswitch(target_queue, jnum):
    """
    Switch a job to a different queue.
    @param target_queue: the job will go into this queue
    @param jnum: the id of the job to switch
    @return: (out, err)
    """
    cmd = ['bswitch', target_queue, str(jnum)]
    p = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return p.communicate()

def gen_accessible_queues():
    cmd = ['bqueues', '-u', getpass.getuser()]
    p = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    lines = list(nonempty_stripped_lines(out.splitlines()))
    if lines:
        header_line, data_lines = lines[0], lines[1:]
        for line in data_lines:
            queue, rest = line.split(None, 1)
            yield queue

def _get_bsub_job_number(bsub_output):
    """
    This is a helper function.
    @param bsub_output: the output of bsub on stdout
    @return: the job number
    """
    matches = re.search('<([0-9]+)>', bsub_output)
    if not matches:
        raise LSFError('no job number found in bsub output')
    groups = matches.groups()
    if len(groups) != 1:
        msg_a = 'expected one job number in bsub output'
        msg_b = 'but found %d' % len(groups)
        raise LSFError(msg_a + msg_b)
    return int(groups[0])

class Bsub:
    def __init__(self):
        self.shell = None
        self.flags = {}
        self.commands = []
        self.job_number = None
    def gen_lines(self):
        if self.shell:
            yield '#! ' + self.shell
        for kv in self.flags.items():
            yield '#BSUB -%s %s' % kv
        for line in self.commands:
            yield line
    def submit(self):
        """
        Use bsub to submit the job to the LSF cluster.
        Note that the returned values are not the outputs
        from the commands in the job, but are rather the outputs
        from the bsub command itself.
        @return: bsub stdout and stderr contents
        """
        p = subprocess.Popen(['bsub'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate(str(self))
        self.job_number = _get_bsub_job_number(out)
        return (out, err)
    def __str__(self):
        return '\n'.join(self.gen_lines())

def bjobs():
    """
    Yield tuples (jobid, state, queue)
    """
    # -w suppresses truncation
    p = subprocess.Popen(['bjobs', '-w'], stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    lines = list(nonempty_stripped_lines(out.splitlines()))
    if lines:
        header_line, data_lines = lines[0], lines[1:]
        for line in data_lines:
            try:
                JOBID, USER, STAT, QUEUE, rest = line.split(None, 4)
            except ValueError, e:
                raise Exception('error: %s\n in line: %s' % (e, line))
            yield (int(JOBID), STAT, QUEUE)
    
def gen_unfinished_job_numbers():
    # -w suppresses truncation
    p = subprocess.Popen(['bjobs', '-w'], stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    lines = list(nonempty_stripped_lines(out.splitlines()))
    if lines:
        header_line, data_lines = lines[0], lines[1:]
        for line in data_lines:
            job, rest = line.split(None, 1)
            yield int(job)
