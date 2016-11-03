from dwarf_tests import *


build('foo.adb')
cu, root = get_dwarf('foo.o')

record_type = find_die(root, 'DW_TAG_structure_type', 'foo__record_type')
length1_fld = find_die(record_type, 'DW_TAG_member', 'length1')
length2_fld = find_die(record_type, 'DW_TAG_member', 'length2')

# Check that multiple entities reference exactly this record.
r_var = find_die(root, 'DW_TAG_variable', 'r')
assert_eq(attr_die(cu, r_var, 'DW_AT_type'), record_type)

r_param = find_die(root, 'DW_TAG_formal_parameter', 'r')
r_param_type_prefixes, r_param_type = parse_type_prefixes(
    attr_die(cu, r_param, 'DW_AT_type')
)
assert_eq(r_param_type_prefixes[-1], 'DW_TAG_reference_type')
# Depending on GCC versions, the reference type can be constant, restricted, or
# both.
allowed_prefixes = {'DW_TAG_const_type', 'DW_TAG_restrict_type'}
assert_eq(set(r_param_type_prefixes[:-1]) | allowed_prefixes, allowed_prefixes)
assert_eq(r_param_type, record_type)

# Check array type for A1

a1_fld = find_die(record_type, 'DW_TAG_member', 'a1')
a1_type = attr_die(cu, a1_fld, 'DW_AT_type')
assert_eq(a1_type.tag, 'DW_TAG_array_type')

assert_eq(len(die_children(a1_type)), 1)
a1_range = die_child(a1_type, 0)
assert_eq(subrange_root(a1_range).attributes['DW_AT_name'].value, 'integer')
assert_no_attr(a1_range, 'DW_AT_lower_bound')
assert_eq(attr_die(cu, a1_range, 'DW_AT_upper_bound'), length1_fld)

# Check array type for A2

a2_fld = find_die(record_type, 'DW_TAG_member', 'a2')
a2_type = attr_die(cu, a2_fld, 'DW_AT_type')
assert_eq(a2_type.tag, 'DW_TAG_array_type')

assert_eq(len(die_children(a2_type)), 1)
a2_range = die_child(a2_type, 0)
assert_eq(subrange_root(a2_range).attributes['DW_AT_name'].value, 'integer')
assert_eq(attr_die(cu, a2_range, 'DW_AT_lower_bound'), length1_fld)
assert_eq(attr_die(cu, a2_range, 'DW_AT_upper_bound'), length2_fld)
