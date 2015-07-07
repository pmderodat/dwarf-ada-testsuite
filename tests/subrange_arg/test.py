from dwarf_tests import *


gnatmake('foo.adb')
cu, root = get_dwarf('foo.o')


range_count = find_die(root, 'DW_TAG_subprogram', 'foo__range_count')

l_bound = find_die(range_count, 'DW_TAG_variable',
                   'foo__range_count__Tarray_typeD1___L')
u_bound = find_die(range_count, 'DW_TAG_variable',
                   'foo__range_count__Tarray_typeD1___U')

# Get the A variable and peel the typedef around the array type.
a_var = find_die(range_count, 'DW_TAG_variable', 'a')
array_type = peel_typedef(cu, attr_die(cu, a_var, 'DW_AT_type'))

# TODO: make sure the array type is below the range_count subprogram (this is
# not correct right now).

# Make sure this is an array with the subrange we expect.
assert_eq(array_type.tag, 'DW_TAG_array_type')
assert_eq(len(die_children(array_type)), 1)
array_range = die_child(array_type, 0)
assert_eq(subrange_root(array_range).attributes['DW_AT_name'].value, 'integer')

assert_eq(attr_die(cu, array_range, 'DW_AT_lower_bound'), l_bound)
assert_eq(attr_die(cu, array_range, 'DW_AT_upper_bound'), u_bound)
