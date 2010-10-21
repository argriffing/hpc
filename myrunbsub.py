"""
Run a command line using bsub with some hardcoded parameters.
"""

import sys
import time

import lsf

if __name__=='__main__':
    b = lsf.Bsub()
    b.flags = {
            'n' : 1,
            'W' : 720,
            'q' : 'dean'}
    cmd = ' '.join("'%s'" % v for v in sys.argv[1:])
    b.commands = [cmd]
    out, err = b.submit()
    sys.stdout.write(out)
    sys.stderr.write(err)
    while b.job_number not in lsf.gen_unfinished_job_numbers():
        time.sleep(0.5)
