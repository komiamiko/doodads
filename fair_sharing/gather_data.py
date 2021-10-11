"""
Runs the fair sharing computation up to a limit,
and logs some amount of that to file for analysis
of repeated substrings or other analysis later.
"""

import argparse
import datetime
import os
import struct
import subprocess
import time

def safe_write_ab(fn, data):
    """
    Append to a file. If it fails, wait and try again.
    """
    success = False
    failcount = 0
    while not success:
        try:
            with open(fn, 'ab') as file:
                file.write(data)
            success = True
        except:
            failcount += 1
            if failcount % 100 == 0:
                print(f'Failed {failcount} times to write to {fn}')

def _fair_sharing_array(n=3, degree=2, limit=10**6, use_numpy=False):
    """
    Modified version of the normal one with debug outputs.
    """
    
    import itertools
    np = None
    try:
        if use_numpy:
            import numpy as np
    except ImportError:
        pass
    
    def reset():
        points = [1] + [0] * degree
        scores = [[0] * (degree + 1) for _ in range(n)]
        stack = list(range(n))
        stack = stack + stack[::-1]
        bstack = []
        if np:
            dtype = np.int64 if limit**degree < 2**63 else object
            points = np.array(points, dtype=dtype)
            scores = np.array(scores, dtype=dtype)
        return points, scores, stack, bstack

    points, scores, stack, bstack = reset()
    skip_first = 0
    k = 0

    while True:
        if stack:
            j = stack.pop()
            expand = False
        else:
            j = 0
            dupli = 0
            for i in range(1, n):
                if np:
                    eq = scores[i] == scores[j]
                    if np.all(eq):
                        dupli += 1
                    else:
                        l = np.argmin(eq)
                        if scores[i,l] < scores[j,l]:
                            j = i
                            dupli = 0
                else:
                    if scores[i] < scores[j]:
                        j = i
                        dupli = 0
                    elif scores[i] == scores[j]:
                        dupli += 1
            expand = dupli != 0 and k >= n
            bstack.append(j)
            if len(bstack) == n:
                stack, bstack = bstack, stack
        if expand:
            degree += 1
            with open('mnp.txt', 'a') as file:
                file.write(f'{n}\t{degree}\t{k}\n')
            points, scores, stack, bstack = reset()
            skip_first = k
            k = 0
            continue
        if np:
            scores[j] += points
            points[1:] -= points[:-1]
        else:
            for i in range(degree+1):
                scores[j][i] += points[i]
            for i in range(degree,0,-1):
                points[i] -= points[i-1]
        if k >= skip_first:
            yield j
        k += 1

def get_options():
    parser = argparse.ArgumentParser(description='Run fair sharing to fill more table entries and generate data for analysis.')
    parser.add_argument('-n', type=int, required=True,
                        help='n to compute for (max: 256)')
    parser.add_argument('-b', '--block-size', type=int, required=True,
                        help='write to disk every this many elements')
    parser.add_argument('-e', '--elements-to-compute', type=int, required=True,
                        help='elements to compute. used in searching for M_n(p)')
    parser.add_argument('-l', '--elements-to-log', type=int, required=True,
                        help='length of the prefix to save to the log file')
    parser.add_argument('-r', '--root', action='store_true',
                        help='clear log files and split subprocesses for n up to specified n')

    args = parser.parse_args()
    return args

def remove_if_exists(fp):
    if os.path.exists(fp):
        os.remove(fp)
        return True
    return False

def main_root(args):
    # clear log files
    print('Cleaning up old files...')
    remove_if_exists('mnp.txt')
    for i in range(3, args.n+1):
        if not remove_if_exists(f'{i}.fs'):
            break
    # spawn child processes
    print('Starting...')
    subs = []
    for i in range(3, args.n+1):
        sub = subprocess.Popen(['py', 'gather_data.py',
            '-n', str(i), '-b', str(args.block_size),
            '-e', str(args.elements_to_compute),
            '-l', str(args.elements_to_log)])
        subs.append((i, sub))
    # periodically update
    start_time = datetime.datetime.utcnow()
    interval = 1.0
    while subs:
        for i in range(len(subs))[::-1]:
            n, sub = subs[i]
            if sub.poll() is not None:
                print(f'n={n} completed')
                subs.pop(i)
        time.sleep(interval)
        interval = min(interval * 1.01, 600)
        print(f'{datetime.datetime.utcnow() - start_time} elapsed')

def main_single(args):
    # compute!
    gen = iter(_fair_sharing_array(n=args.n, limit=args.elements_to_compute))
    buf = []
    for _ in range(args.elements_to_log):
        buf.append(next(gen))
        if len(buf) >= args.block_size:
            safe_write_ab(f'{args.n}.fs', struct.pack(f'{len(buf)}B', *buf))
            buf = []
    if buf:
        safe_write_ab(f'{args.n}.fs', struct.pack(f'{len(buf)}B', *buf))
    for _ in range(args.elements_to_compute - args.elements_to_log):
        _ = next(gen)

def main():
    args = get_options()
    if args.root:
        main_root(args)
    else:
        main_single(args)

if __name__ == '__main__':
    main()
