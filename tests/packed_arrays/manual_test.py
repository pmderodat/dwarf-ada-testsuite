import re
import subprocess
import sys


class State:
    def __init__(self):
        self.arrays = {}
        self.reset()

    def reset(self):
        self.in_array = False
        self.name = None
        self.stride = None

    def digest(self):
        if self.in_array:
            assert self.name
            self.arrays[self.name] = self.stride
        self.reset()


def get_match(regexp, line, line_no):
    match = re.search(regexp, line)
    if not match:
        print(
            'Could not find a match for:\n\t{}\n... in line {}:\n\t{}'.format(
                regexp, line_no, line
            )
        )
        sys.exit(1)
    return match.groups(0)


dwdis = subprocess.check_output(['objdump', '--dwarf=info', sys.argv[1]])
s = State()

for line_no, line in enumerate(dwdis.split('\n'), 1):
    if '(DW_TAG_array_type' in line:
        s.digest()
        s.in_array = True

    elif 'DW_TAG_' in line:
        s.digest()

    elif s.in_array:
        if 'DW_AT_name' in line:
            s.name = line.split()[-1]
        if 'DW_AT_bit_stride' in line:
            s.stride = line.split()[-1]

s.digest()

for name in sorted(s.arrays):
    stride = s.arrays[name]
    print('{}: {}'.format(
        name, 'stride = {}'.format(stride) if stride else 'no stride'
    ))
