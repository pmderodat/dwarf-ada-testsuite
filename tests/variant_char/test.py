from elftools.dwarf.constants import DW_ATE_unsigned_char
from dwarf_tests import *


build('pkg.ads')
cu, root = get_dwarf('pkg.o')

char_type = find_die(root, 'DW_TAG_base_type', 'character')
assert_eq(char_type.attributes['DW_AT_encoding'].value, DW_ATE_unsigned_char)

rec_type = find_die(root, 'DW_TAG_structure_type', 'pkg__rec_type')
var = find_die(root, 'DW_TAG_variable', 'pkg__r')

# Make sure the variable references the generic (!= specific) type
prefixes, var_type = parse_type_prefixes(attr_die(cu, var, 'DW_AT_type'))
assert_eq((prefixes, var_type), ([], rec_type))

# Quickly check the variant part topology
c_member, variant_part = die_children(rec_type)
assert_eq(attr_die(cu, c_member, 'DW_AT_type'), char_type)
assert_eq(attr_die(cu, variant_part, 'DW_AT_discr'), c_member)
var_first, var_127, var_128, var_last, var_others = die_children(variant_part)

# Now check how the variants are encoded
for var_item, discr_value in (
    (var_first,  0),
    (var_127,    127),
    (var_128,    128),
    (var_last,   255),
    (var_others, None),
):
    assert 'DW_AT_discr_list' not in var_item.attributes
    discr_attr = var_item.attributes.get('DW_AT_discr_value', None)
    if discr_value is None:
        assert_eq(discr_attr, None)
    else:
        assert_eq(discr_attr.value, discr_value)
