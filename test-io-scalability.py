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
    def __init__(self, datapath, exepath, nminutes, index):
        self.b = lsf.Bsub()
        self.datapath = datapath
        self.exepath = exepath
        jobname = 'job.%d' % index
        nkilobytes = 1000
        self.b.flags = {
                'J': jobname,
                'W': nminutes, 'M': nkilobytes,
                'o': 'out', 'e': 'err'}
        if datapath.endswith('.gz'):
            catcmd = 'zcat'
        else:
            catcmd = 'cat'
        cmd = '%s %s | %s > /dev/null' % (catcmd, datapath, exepath)
        self.b.commands = [cmd]
    def submit(self, queue):
        self.b.flags['q'] = queue
        out, err = self.b.submit()
        sys.stdout.write(out)
        sys.stderr.write(err)

def process_no_switching(filenames, exepath, qname, nminutes):
    # create the jobs
    jobs = []
    for i, datapath in enumerate(filenames):
        jobs.append(Job(datapath, exepath, nminutes, i))
    # submit all of the jobs to the specified queue
    jnums = set()
    for job in jobs:
        job.submit(qname)
        jnums.add(job.b.job_number)
    # go until all jobs have finished
    while True:
        time.sleep(2.0)
        # query the state of the submitted jobs
        jnum_state_queue_triples = list(lsf.bjobs())
        # if no submitted jobs were found then we are done
        if not jnum_state_queue_triples:
            break
    # return the job numbers for the finished jobs
    return jnums

def process_switching(filenames, exepath, queues, nminutes):
    # define the switcher
    switcher = whackamole.Switcher(queues, switch)
    # create the jobs
    jobs = []
    for i, datapath in enumerate(filenames):
        jobs.append(Job(datapath, exepath, nminutes, i))
    # submit all of the jobs to the debug queue
    number_to_job = {}
    for job in jobs:
        job.submit('debug')
        number_to_job[job.b.job_number] = job
    # tell the switcher that all jobs were submitted to the debug queue
    switcher.on_submission({'debug': set(number_to_job)})
    # go until all jobs have finished
    while True:
        time.sleep(2.0)
        # query the state of the submitted jobs
        jnum_state_queue_triples = list(lsf.bjobs())
        # if no submitted jobs were found then we are done
        if not jnum_state_queue_triples:
            break
        # possibly switch some queues
        qname_to_jnums = collections.defaultdict(set)
        for jnum, state, queue in jnum_state_queue_triples:
            if state == 'PEND':
                qname_to_jnums[queue].add(jnum)
        switcher.on_observation(qname_to_jnums)
    # return the job numbers for the finished jobs
    return set(number_to_job)

def gen_powers_of_two():
    p = 1
    while True:
        yield p
        p *= 2

def main(args):
    nseconds = args.minutes * 60
    # define the path to the exe
    exepath = os.path.join(args.exe_dir, args.exe_name)
    # get the defined queues and put the debug queue at the front
    if not args.queue:
        queues = list(lsf.gen_accessible_queues())
        i = queues.index('debug')
        queues[0], queues[i] = queues[i], queues[0]
    # start writing the report
    with open(args.report, 'w') as fout:
        headings = [
                'N',
                'MEAN_SUCCESS_WALL_RUN_TIME',
                'SUCCESS_PROPORTION',
                'BATCH_WALL_TIME']
        print >> fout, '\t'.join(headings)
        # run the parallel processing for an increasing number of nodes
        for cap in gen_powers_of_two():
            filenames = args.files[:cap]
            if cap > len(args.files):
                break;
            # run a few jobs to completion
            tm_start = time.time()
            if args.queue:
                jnums = process_no_switching(
                        filenames, exepath, args.queue, args.minutes)
            else:
                jnums = process_switching(
                        filenames, exepath, queues, args.minutes)
            tm_end = time.time()
            # get the seconds of wall time each job was in the run state
            id_run_wall_pairs = list(lsf.bhist(jnums))
            # if a job took too long then it failed
            successes = [t for j, t in id_run_wall_pairs if t < nseconds]
            failures = [t for j, t in id_run_wall_pairs if t >= nseconds]
            nsuccesses = len(successes)
            nfailures = len(failures)
            if successes:
                mswrt = sum(successes) / float(nsuccesses)
            else:
                mswrt = '-'
            success_proportion = nsuccesses / float(cap)
            # write the results
            typed_row = [cap, mswrt, success_proportion, tm_end - tm_start]
            print >> fout, '\t'.join(str(x) for x in typed_row)

def whole_number(s):
    x = int(s)
    if x < 1:
        raise TypeError()
    return x

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minutes', type=whole_number, default=15,
            help='maximum wall minutes in run state per job')
    parser.add_argument('--queue',
            help='pass this queue to bsub and do not switch among queues')
    parser.add_argument('--report', default='report.txt',
            help='path to the report output file')
    parser.add_argument('--exe_dir', default='',
            help='path to the directory containing the executable')
    parser.add_argument('--exe_name',
            default='get-pileup-chromosome-names',
            help='name of the executable')
    parser.add_argument('files', nargs='+',
            help='pileup files')
    args = parser.parse_args()
    main(args)
