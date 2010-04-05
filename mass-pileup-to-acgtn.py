"""
Process a bunch of stuff in parallel using BSUB with LSF.
"""

import os
import time
import sys
import re

import argparse

import lsf

def main(args):
    extractcmd = os.path.join(args.exe_dir,
            'extract-pileup-chromosome ' + args.chromosome)
    processcmd = os.path.join(args.exe_dir,
            'pileup-to-acgtn ' + args.ref_sequence)
    # create the jobs
    bsubs = []
    for datapath in args.files:
        # define and create the output subdirectory
        outdir = os.path.join(args.out_dir, args.namescheme(datapath))
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        # Split the file into chunks to enable parallelism.
        # Each position has 4-byte A, C, G, T, and N counts,
        # for a total of 20 bytes.
        nbytes_per_position = 20
        npositions_per_file = 1000000
        # create the job
        b = lsf.Bsub()
        b.flags = {
                'W': 120, 'M': 1000,
                'o': 'out', 'e': 'err'}
        if args.queue:
            b.flags['q'] = args.queue
        splitcmd = ' '.join([
            'split',
            '--bytes=%d' % (nbytes_per_position * npositions_per_file),
            '--suffix-length=4',
            '--numeric-suffixes',
            '-',
            os.path.join(outdir, 'x')])
        cmd = 'zcat %s | %s | %s | %s' % (
                datapath, extractcmd, processcmd, splitcmd)
        b.commands = [cmd]
        bsubs.append(b)
    # submit the jobs
    jnums = set()
    for b in bsubs:
        out, err = b.submit()
        sys.stdout.write(out)
        sys.stderr.write(err)
        jnums.add(b.job_number)
    # initialize the set of unfinished job numbers
    prev_unfinished = set(jnums)
    # wait for all of the jobs to finish
    while True:
        curr_unfinished = jnums & set(lsf.gen_unfinished_job_numbers())
        newly_finished = prev_unfinished - curr_unfinished
        for jnum in newly_finished:
            print 'job', jnum, 'has finished'
        if not curr_unfinished:
            break
        prev_unfinished = curr_unfinished
        time.sleep(2.0)

def namescheme_20100403(datapath):
    """
    This is an ad hoc way to construct a directory name.
    The idea is to sequester the ugliness into this function.
    @param datapath: path to the gzipped pileup data file
    @return: a subdirectory name
    """
    basename = os.path.basename(datapath)
    m = re.search('([0-9]+)', basename)
    if not m:
        raise Exception('unexpected data filename')
    if len(m.groups()) != 1:
        raise Exception('expected one number in the filename')
    return m.groups()[0]

def namescheme(s):
    if s == '20100403':
        return namescheme_20100403
    else:
        raise TypeError('invalid name scheme')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chromosome', default='2L',
            help='the name of the chromosome of interest')
    parser.add_argument('--ref_sequence',
            default='/brc_share/brc_scratch/argriffi/ref-sequences/2L.raw',
            help='the reference chromosome sequence')
    parser.add_argument('--namescheme', type=namescheme,
            default=namescheme_20100403,
            help='how directory names are inferred from data filenames')
    parser.add_argument('-q', '--queue',
            help='specify a LSF queue')
    parser.add_argument('--out_dir', default='',
            help='subdirectories will be created here')
    parser.add_argument('--exe_dir', default='',
            help='path to the directory containing the executables')
    parser.add_argument('files', nargs='+',
            help='gzipped pileup files')
    args = parser.parse_args()
    main(args)
