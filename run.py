#! /usr/bin/env python

import argparse
import os
import os.path
import subprocess
import sys


parser = argparse.ArgumentParser(description='Run the DWARF/Ada testsuite')
parser.add_argument(
    'testcase', nargs='*',
    help='Optional list of paths for testcases to run. If not provided, all'
         ' testcases in the "tests" directory are run.'
)


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


def which(program):
    return subprocess.check_output(['which', program]).strip()


def main(args):
    print('Using compiler: {}'.format(which(
        os.environ['GNAT1']
        if 'GNAT1' in os.environ else
        'gcc'
    )))
    test_list = args.testcase or (os.path.join('tests', d)
                                  for d in os.listdir('tests'))
    one_test_run = False
    for child in sorted(test_list):
        test_file = os.path.join(child, 'test.py')
        if os.path.isfile(test_file):
            one_test_run = True
            run_test(test_file)
    if not one_test_run:
        print('Warning: no test run')

if __name__ == '__main__':
    try:
        main(parser.parse_args())
    except KeyboardInterrupt:
        sys.exit(1)
