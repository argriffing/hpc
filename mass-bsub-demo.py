"""
Process a bunch of stuff in parallel using BSUB with LSF.
"""

import sys
import os
import subprocess
from subprocess import PIPE

import argparse

g_pileups_root = '/brc_share/brc_scratch/argriffi/pileups'
g_piledriver_root = '/brc_share/brc/argriffi/repos/piledriver'

class Bsub:
    def __init__(self):
        self.shell = None
        self.flags = {}
        self.commands = []
    def gen_lines(self):
        if self.shell:
            yield '#! ' + self.shell
        for kv in self.flags.items():
            yield '#BSUB -%s %s' % kv
        for line in self.commands:
            yield line
    def __str__(self):
        return '\n'.join(self.gen_lines())

def make_submission(strain):
    b = Bsub()
    b.flags = {'W': 10, 'M': 1000, 'o': 'out', 'e': 'err'}
    # define input, execution, and output paths
    filename = 'dgrp-%s.slx.bwa.sorted.bam.pileup.gz' % strain
    datapath = os.path.join(g_pileups_root, filename)
    exepath = os.path.join(g_piledriver_root, 'get-pileup-chromosome-names')
    outpath = '%s.out' % strain
    # build the command
    cmd = 'zcat %s | %s > %s' % (datapath, exepath, outpath)
    b.commands = [cmd]
    return b

def main(args):
    for strain in (208, 301, 303, 304):
        b = make_submission(strain)
        p = subprocess.Popen(['bsub'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate(str(b))
        sys.stdout.write(out)
        sys.stderr.write(err)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    main(args)
