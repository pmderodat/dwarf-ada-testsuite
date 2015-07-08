from dwarf_tests import *


gnatmake('foo.adb')
cu, root = get_dwarf('foo.o')


def check_biased(die, base_name, bounds, bias):
    base_type = subrange_root(die)
    assert_eq(base_type.attributes['DW_AT_name'].value, base_name)
    assert_eq(die.attributes['DW_AT_lower_bound'].value, bounds[0])
    assert_eq(die.attributes['DW_AT_upper_bound'].value, bounds[1])
    assert_eq(die.attributes[DW_AT_GNU_bias].value, bias)


# Check that the I variable is of a biased subrange.
i_var = find_die(root, 'DW_TAG_variable', 'i')
prefixes, i_type = parse_type_prefixes(attr_die(cu, i_var, 'DW_AT_type'))
assert_eq(prefixes, ['DW_TAG_const_type'])
check_biased(i_type, 'foo__Tindex_typeB', (100, 107), 100)

# Check that R is a record whose members are of biased subranges.
r_var = find_die(root, 'DW_TAG_variable', 'r')
r_type = attr_die(cu, r_var, 'DW_AT_type')
assert_eq((r_type.tag, r_type.attributes['DW_AT_name'].value),
          ('DW_TAG_structure_type', 'foo__record_type'))

a_fld, b_fld = [c for c in die_children(r_type)
                if c.tag == 'DW_TAG_member']
check_biased(attr_die(cu, a_fld, 'DW_AT_type'),
             'foo__Tsmall_typeB', (50, 57), 50)
check_biased(attr_die(cu, b_fld, 'DW_AT_type'),
             'foo__Tsmall_typeB', (50, 57), 50)
