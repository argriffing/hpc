"""
Process a bunch of stuff in parallel using BSUB with LSF.
"""

import os
import time
import sys
import collections

import argparse

import lsf
import whackamole

def nonempty_stripped_lines(lines):
    for raw_line in lines:
        line = raw_line.strip()
        if line:
            yield line

def switch(qname, jnum):
    out, err = lsf.bswitch(qname, jnum)
    sys.stdout.write(out)
    sys.stderr.write(err)

class Job:
    def __init__(self, datapath, exepath, outpath):
        self.b = lsf.Bsub()
        self.datapath = datapath
        self.exepath = exepath
        self.outpath = outpath
        self.b.flags = {
                'W': 10, 'M': 1000,
                'o': 'out', 'e': 'err'}
        if datapath.endswith('.gz'):
            catcmd = 'zcat'
        else:
            catcmd = 'cat'
        cmd = '%s %s | %s > %s' % (catcmd, datapath, exepath, outpath)
        self.b.commands = [cmd]
    def submit(self, queue):
        self.b.flags['q'] = queue
        out, err = self.b.submit()
        sys.stdout.write(out)
        sys.stderr.write(err)
    def validate(self, expected_names):
        """
        This should be called after the job has finished.
        """
        with open(self.outpath) as fin:
            observed_names = set(nonempty_stripped_lines(fin))
            unexpected = list(observed_names - expected_names)
            unobserved = list(expected_names - observed_names)
            if unexpected:
                msg_a = 'unexpected chromosome names '
                msg_b = 'in %s: %s' % (self.datapath, unexpected)
                msg = msg_a + msg_b
                print msg
            if unobserved:
                msg_a = 'unobserved chromosome names '
                msg_b = 'in %s: %s' % (self.datapath, unobserved)
                msg = msg_a + msg_b
                print msg

def main(args):
    # define the path to the exe
    exepath = os.path.join(args.exe_dir, args.exe_name)
    # read the expected chromosome names
    with open(args.expected) as fin:
        expected_names = set(nonempty_stripped_lines(fin))
    # get the defined queues and put the debug queue at the front
    queues = list(lsf.gen_accessible_queues())
    i = queues.index('debug')
    queues[0], queues[i] = queues[i], queues[0]
    # define the switcher
    switcher = whackamole.Switcher(queues, switch)
    # create the jobs
    jobs = []
    for i, datapath in enumerate(args.files):
        gzname = os.path.basename(datapath)
        outpath = os.path.join(args.scratch, gzname + '.names.' + str(i))
        jobs.append(Job(datapath, exepath, outpath))
    number_to_job = {}
    # submit all of the jobs to the debug queue
    for job in jobs:
        job.submit('debug')
        number_to_job[job.b.job_number] = job
    # tell the switcher that all jobs were submitted to the debug queue
    switcher.on_submission({'debug': set(number_to_job)})
    # initialize the set of unfinished job numbers
    all_numbers = set(number_to_job)
    prev_unfinished = set(number_to_job)
    # go until all of the jobs have finished
    while prev_unfinished:
        time.sleep(2.0)
        # query the state of the submitted jobs
        jnum_state_queue_triples = list(lsf.bjobs())
        # possibly switch some queues
        qname_to_jnums = collections.defaultdict(set)
        for jnum, state, queue in jnum_state_queue_triples:
            if state == 'PEND':
                qname_to_jnums[queue].add(jnum)
        switcher.on_observation(qname_to_jnums)
        # check for finished jobs
        if jnum_state_queue_triples:
            jnums, states, queues = zip(*jnum_state_queue_triples)
        else:
            jnums, states, queues = [], [], []
        curr_unfinished = all_numbers & set(jnums)
        newly_finished = prev_unfinished - curr_unfinished
        for jnum in newly_finished:
            print 'job', jnum, 'has finished'
            number_to_job[jnum].validate(expected_names)
        prev_unfinished = curr_unfinished

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', required=True,
            help='a file containing the expected chromosome names')
    parser.add_argument('--scratch', default='',
            help='a directory writable by all cluster nodes')
    parser.add_argument('--exe_dir', default='',
            help='path to the directory containing the executable')
    parser.add_argument('--exe_name',
            default='get-pileup-chromosome-names',
            help='name of the executable')
    parser.add_argument('files', nargs='+',
            help='pileup files')
    args = parser.parse_args()
    main(args)
