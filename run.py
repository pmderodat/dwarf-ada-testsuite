#! /usr/bin/env python

import os
import os.path
import subprocess
import sys


# Move to the testsuite's root directory and setup paths
os.chdir(os.path.dirname(os.path.abspath(__file__)))

lib_path = os.path.abspath('utils')
sys.path.append(lib_path)


def indent(text):
    return '\n'.join('    {}'.format(line) for line in text.rstrip().split('\n'))


def run_test(test_file):
    test_name = os.path.dirname(test_file)
    with open(os.devnull, 'r') as devnull:
        env = dict(os.environ)
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = '{}:{}'.format(lib_path, env['PYTHONPATH'])
        else:
            env['PYTHONPATH'] = '{}'.format(lib_path)
        p = subprocess.Popen(
            [sys.executable, os.path.abspath(test_file)],
             cwd=os.path.dirname(test_file),
             env=env,
             stdin=devnull, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            print('\x1b[31mERROR\x1b[0m: {}'.format(test_name))
            if stdout:
                print(indent(stdout))
            if stderr:
                print(indent(stderr))
        else:
            print('\x1b[32mOK\x1b[0m:    {}'.format(test_name))


def main(args):
    for child in os.listdir('tests'):
        test_file = os.path.join('tests', child, 'test.py')
        if os.path.isfile(test_file):
            run_test(test_file)

if __name__ == '__main__':
    try:
        main(None)
    except KeyboardInterrupt:
        sys.exit(1)
