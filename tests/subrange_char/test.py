from elftools.dwarf.constants import DW_ATE_unsigned_char
from dwarf_tests import *


build('pkg.ads')
cu, root = get_dwarf('pkg.o')

char_type = find_die(root, 'DW_TAG_base_type', 'character')
assert_eq(char_type.attributes['DW_AT_encoding'].value, DW_ATE_unsigned_char)

for var_name, (lower_bound, upper_bound) in (
    ('pkg__lr', (0, 127)),
    ('pkg__mr', (64, 164)),
    ('pkg__ur', (128, 255)),
):
    var_die = find_die(root, 'DW_TAG_variable', var_name)
    prefixes, subr_type = parse_type_prefixes(
        attr_die(cu, var_die, 'DW_AT_type')
    )
    assert_eq((prefixes, subr_type.tag), ([], 'DW_TAG_subrange_type'))

    assert_eq(attr_die(cu, subr_type, 'DW_AT_type'), char_type)
    assert_eq(
        (var_name,
         subr_type.attributes['DW_AT_lower_bound'].value,
         subr_type.attributes['DW_AT_upper_bound'].value),
        (var_name, lower_bound, upper_bound)
    )
