from dwarf_tests import *


build('foo.ads', ['-O1'])
cu, root = get_dwarf('foo.o')


rec_type = find_die(root, 'DW_TAG_structure_type', 'foo__rec_type')
i_fld, var_part = die_children(rec_type)


def check_field(die, name, location):
    assert_eq((die.tag, die.attributes['DW_AT_name'].value),
              ('DW_TAG_member', name))
    data_member_location = die.attributes['DW_AT_data_member_location'].value
    if isinstance(location, int):
        assert_eq(location, data_member_location)
    else:
        return match_expr(data_member_location, location)


check_field(i_fld, 'i', 0)

# Variant part: check the discriminant, the variants themselves and the fields
# they contain.
assert_eq(attr_die(cu, var_part, 'DW_AT_discr'), i_fld)
var_0, var_1_0, var_complex, var_others = die_children(var_part)

# Variant when I = 0.
assert_eq(var_0.attributes['DW_AT_discr_value'].value, 0)
assert_no_attr(var_0, 'DW_AT_discr_list')
i0_fld, = die_children(var_0)
check_field(i0_fld, 'i0', 4)

# Variant when I in 1 .. 0
assert_no_attr(var_1_0, 'DW_AT_discr_value')
assert_eq(attr_discr_list(var_1_0, 32, True), [('DW_DSC_range', 1, 0)])
i1_fld, = die_children(var_1_0)
check_field(i1_fld, 'i1', 4)


# Variant when I in 1 .. 10 | Integer'Last .. Integer'First
assert_no_attr(var_complex, 'DW_AT_discr_value')
assert_eq(attr_discr_list(var_complex, 32, True),
          [('DW_DSC_range', 1, 10),
           ('DW_DSC_range', 2**31  - 1, -2**31)])
i2_fld, = die_children(var_complex)
check_field(i2_fld, 'i2', 4)

# Variant when others.
assert_no_attr(var_others, 'DW_AT_discr_value')
assert_no_attr(var_others, 'DW_AT_discr_list')
assert_eq(len(die_children(var_others)), 0)
