import os
import subprocess

import elftools.elf.elffile
import elftools.dwarf.die
import elftools.dwarf.dwarf_expr


def set_proc(processor):
    global PTR_BYTE_SIZE
    if processor in ('i386', 'i486', 'i586', 'i686', 'x86'):
        PTR_BYTE_SIZE = 4
    elif processor in ('x86_64', ):
        PTR_BYTE_SIZE = 8
    else:
        assert False, 'Unknown processor: {}'.format(processor)

set_proc(os.environ.get('PROC', os.uname()[4]))


DW_AT_GNU_numerator = 0x2303
DW_AT_GNU_denominator = 0x2304
DW_AT_GNU_bias = 0x2305


def build(source_file, cargs=None):
    """
    Build some Ada source file with debug information and minimal GNAT
    encodings. This should leave an object file in the current directory.
    """
    args = ['-g', '-fgnat-encodings=minimal', source_file] + (cargs or [])
    if 'GNAT1' in os.environ:
        basename, ext = source_file.rsplit('.', 1)
        assert ext in ('ads', 'adb')
        asm_file = basename + '.s'
        object_file = basename + '.o'
        subprocess.check_call([os.environ['GNAT1'], '-o', asm_file] + args)
        subprocess.check_call(['gcc', '-c', asm_file, '-o', object_file])
    else:
        subprocess.check_call(['gcc', '-c'] + args)


def get_dwarf(elf):
    """
    Assuming `elf` is an ELF file with exactly one DWARF compilation unit,
    return (CU, top DIE).
    """
    with open(elf, 'rb') as f:
        elf_file = elftools.elf.elffile.ELFFile(f)
        assert elf_file.has_dwarf_info()
        dwarf_info = elf_file.get_dwarf_info()
        cu_list = list(dwarf_info.iter_CUs())
        (cu, ) = cu_list
        return (cu, cu.get_top_DIE())


def find_die(die, tag=None, name=None):
    """
    Look for the first DIE in `die` whose tag is `tag` (if provided) and whose
    name is `name` (if provided). Return it if found or raise a ValueError.
    """

    def helper(die):
        if ((tag is None or die.tag == tag) and
            (name is None or ('DW_AT_name' in die.attributes and
                              die.attributes['DW_AT_name'].value == name))):
            return die

        for child in die.iter_children():
            result = helper(child)
            if result:
                return result

    result = helper(die)
    if result is None:
        raise ValueError('Could not find a DIE (tag={}, name={})'.format(
            tag, name
        ))
    return result


def find_die_by_offset(cu, offset):
    for die in cu.iter_DIEs():
        if die.offset == offset:
            return die
        elif die.offset > offset:
            break
    assert False, 'No DIE at {:#x}'.format(offset)


def die_children(die):
    return die._children


def die_child(die, n):
    """
    Return the `n`th child of DIE, or raise an IndexError if there is no such
    child.
    """
    return die_children(die)[n]

def attr_die(cu, die, attr_name):
    try:
        attr = die.attributes[attr_name]
    except KeyError as exc:
        raise KeyError('{} has no {} attribute'.format(
            custom_str(die), attr_name
        ))
    if attr.form in ('DW_FORM_ref1',
                     'DW_FORM_ref2',
                     'DW_FORM_ref4',
                     'DW_FORM_ref8',
                     'DW_FORM_ref_udata'):
        offset = attr.value
    else:
        assert False, (
            'Invalid/unsupported form for a DIE reference: {}'.format(
                attr.form
            )
        )

    return find_die_by_offset(cu, offset)


class DWARFExpressionDecoder(elftools.dwarf.dwarf_expr.GenericExprVisitor):
    def __init__(self, structs):
        super(DWARFExpressionDecoder, self).__init__(structs)
        self.result = []

    def _after_visit(self, opcode, opcode_name, args):
        self.result.append(tuple([opcode_name] + list(args)))


def attr_expr(cu, die, attr_name):
    try:
        attr = die.attributes[attr_name]
    except KeyError as exc:
        raise KeyError('{} has no {} attribute'.format(
            custom_str(die), attr_name
        ))
    assert attr.form == 'DW_FORM_exprloc', (
        'Invalid/unsupported form for a DWARF expression: {}'.format(attr.form)
    )

    decoder = DWARFExpressionDecoder(cu.structs)
    decoder.process_expr(attr.value)
    return decoder.result


def make_deref_expr(size):
    return (('DW_OP_deref', )
            if size == PTR_BYTE_SIZE else
            ('DW_OP_deref_size', size))


def parse_type_prefixes(die):
    prefixes = []
    type_die = die
    while type_die.tag in ('DW_TAG_pointer_type',
                           'DW_TAG_reference_type',
                           'DW_TAG_const_type',
                           'DW_TAG_volatile_type',
                           'DW_TAG_restrict_type'):
        prefixes.append(type_die.tag)
        type_die = attr_die(die.cu, type_die, 'DW_AT_type')
    return (prefixes, type_die)


def peel_typedef(cu, die):
    assert_eq(die.tag, 'DW_TAG_typedef')
    return attr_die(cu, die, 'DW_AT_type')


def attr_discr_list(die, discr_size, discr_signed):
    try:
        attr = die.attributes['DW_AT_discr_list']
    except KeyError as exc:
        raise KeyError('{} has no DW_AT_discr_list attribute'.format(
            custom_str(die), attr_name
        ))
    assert attr.form.startswith('DW_FORM_block'), (
        'Invalid/unsupported form for a discrimimant list: {}'.format(
            attr.form
        )
    )

    block = list(attr.value)
    def read_leb128():
        result = 0
        shift = 0
        while True:
            byte = block.pop(0)
            result = result | ((byte & 0x7f) << shift)
            shift += 7
            if not (byte & 0x80):
                break

        result &= 2**discr_size - 1
        if discr_signed and result & 2**(discr_size - 1):
            result |= -1 << discr_size

        return result

    print(attr)
    result = []
    while block:
        descriptor = block.pop(0)
        if descriptor == 0:
            result.append(('DW_DSC_label', read_leb128()))
        elif descriptor == 1:
            low = read_leb128()
            high = read_leb128()
            result.append(('DW_DSC_range', low, high))
        else:
            assert False, ('Invalid descriptor: {}'.format(result))

    return result


class Match(object):
    """Class used to match patterns in DWARF expression: see match_expr."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Match({})'.format(self.name)

def match_expr(expr, pattern):
    """
    Match a DWARF expression against the input pattern. Raise a ValueError when
    there is a mismatch. For instance:

        >>> matches = match_expr(expr, [('DW_OP_deref_size', 4),
                                        ('DW_OP_call4', Match('call1')),
                                        ('DW_OP_call4', Match('call2')),
                                        ('DW_OP_plus_uconst', 1)])
        >>> a = matches['call1']

    Match instances can only appear as operands.
    """
    matches = {}
    if len(expr) != len(pattern):
        raise ValueError('Input expression has {} operations'
                         ' ({} expected)'.format(len(expr), len(pattern)))
    for i, (got_op, pattern_op) in enumerate(
            zip(expr, pattern)):
        error = len(got_op) != len(pattern_op) or got_op[0] != pattern_op[0]
        if not error:
            for got_arg, pattern_arg in zip(got_op, pattern_op):
                if isinstance(pattern_arg, Match):
                    matches[pattern_arg.name] = got_arg
                elif got_arg != pattern_arg:
                    error = True
                    break
        if error:
            raise ValueError('Could not match operation {}:'
                             ' got {} ({} expected)'.format(
                                 i, got_op, pattern_op))
    return matches


def match_dwarf_proc(cu, die_or_offset, pattern):
    die = (find_die_by_offset(cu, die_or_offset)
           if isinstance(die_or_offset, int) else
           die_or_offset)
    assert_eq(die.tag, 'DW_TAG_dwarf_procedure')
    return match_expr(attr_expr(cu, die, 'DW_AT_location'), pattern)


def subrange_root(subrange_die):
    assert subrange_die.tag == 'DW_TAG_subrange_type'
    base_type = subrange_die
    while base_type.tag == 'DW_TAG_subrange_type':
        base_type = attr_die(base_type.cu, base_type, 'DW_AT_type')
    assert base_type.tag in ('DW_TAG_base_type', 'DW_TAG_enumeration_type')
    return base_type


def custom_str(obj):
    if isinstance(obj, elftools.dwarf.die.DIE):
        return str_die(obj)
    else:
        return str(obj)


def str_die(die):
    result = ['<{}'.format(die.tag)]
    if 'DW_AT_name' in die.attributes:
        result.append(' {}'.format(die.attributes['DW_AT_name'].value))
    result.append(' at {:#x}'.format(die.offset))
    result.append('>')
    return ''.join(result)


def assert_eq(value1, value2):
    assert value1 == value2, '{} != {}'.format(custom_str(value1),
                                               custom_str(value2))

def assert_in(value, accepted_values):
    assert value in accepted_values, '{} not in {}'.format(
        custom_str(value),
        '{{{}}}'.format(', '.join(custom_str(v) for v in accepted_values))
    )

def assert_no_attr(die, attr_name):
    assert attr_name not in die.attributes, (
        'Expected no {} attribute in {} but found one'.format(
            attr_name, custom_str(die)
        )
    )
