"""
Process a bunch of stuff in parallel using BSUB with LSF.
"""

import os
import time
import sys

import argparse

import lsf

def nonempty_stripped_lines(lines):
    for raw_line in lines:
        line = raw_line.strip()
        if line:
            yield line

class Job:
    """
    Instantiation submits a job.
    """
    def __init__(self, datapath, exepath, outpath):
        self.b = lsf.Bsub()
        self.datapath = datapath
        self.exepath = exepath
        self.outpath = outpath
        self.b.flags = {
                'W': 10, 'M': 1000,
                'o': 'out', 'e': 'err'}
        cmd = 'zcat %s | %s > %s' % (datapath, exepath, outpath)
        self.b.commands = [cmd]
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
                raise Exception(msg_a + msg_b)
            if unobserved:
                msg_a = 'unobserved chromosome names '
                msg_b = 'in %s: %s' % (self.datapath, unobserved)
                raise Exception(msg_a + msg_b)

def main(args):
    # define the path to the exe
    exepath = os.path.join(args.exe_dir, args.exe_name)
    # read the expected chromosome names
    with open(args.expected) as fin:
        expected_names = set(nonempty_stripped_lines(fin))
    # create and submit the jobs
    number_to_job = {}
    for datapath in args.files:
        gzname = os.path.basename(datapath)
        outpath = os.path.join(args.scratch, gzname + '.names')
        job = Job(datapath, exepath, outpath)
        number_to_job[job.b.job_number] = job
    # initialize the set of unfinished job numbers
    all_numbers = set(number_to_job)
    prev_unfinished = set(number_to_job)
    # wait for all of the jobs to finish
    while True:
        curr_unfinished = all_numbers & set(lsf.gen_unfinished_job_numbers())
        newly_finished = prev_unfinished - curr_unfinished
        for jnum in newly_finished:
            print 'job', jnum, 'has finished'
            number_to_job[jnum].validate(expected_names)
        if not curr_unfinished:
            break
        prev_unfinished = curr_unfinished
        time.sleep(2.0)

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
            help='gzipped pileup files')
    args = parser.parse_args()
    main(args)
