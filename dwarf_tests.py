import subprocess

import elftools.elf.elffile
import elftools.dwarf.die


def gnatmake(main):
    """
    Run gnatmake for minimal GNAT encodings on `main`.
    """
    subprocess.check_call(
        ['gnatmake', '-f', '-q', '-g', '-fgnat-encodings=minimal', main]
    )


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

    for ref_die in cu.iter_DIEs():
        if ref_die.offset == offset:
            return ref_die
        assert ref_die.offset < offset, (
            '{}: could not find the DIE referenced by the {} attribute'.format(
                custom_str(die),
                attr_name
            )
        )


def parse_type_prefixes(die):
    prefixes = []
    type_die = die
    while type_die.tag in ('DW_TAG_pointer_type',
                           'DW_TAG_reference_type',
                           'DW_TAG_const_type',
                           'DW_TAG_volatile_type'):
        prefixes.append(type_die.tag)
        type_die = attr_die(die.cu, type_die, 'DW_AT_type')
    return (prefixes, type_die)


def subrange_root(subrange_die):
    assert subrange_die.tag == 'DW_TAG_subrange_type'
    base_type = subrange_die
    while base_type.tag == 'DW_TAG_subrange_type':
        base_type = attr_die(base_type.cu, base_type, 'DW_AT_type')
    assert base_type.tag == 'DW_TAG_base_type'
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

def assert_no_attr(die, attr_name):
    assert attr_name not in die.attributes, (
        'Expected no {} attribute in {} but found one'.format(
            attr_name, custom_str(die)
        )
    )
