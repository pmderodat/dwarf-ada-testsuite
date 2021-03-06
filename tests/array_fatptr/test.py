from dwarf_tests import *


build('fatptr.adb')
cu, root = get_dwarf('fatptr.o')


# Get the array type referenced by the A formal parameter.
discard = find_die(root, 'DW_TAG_subprogram', 'fatptr__discard')
a_var = find_die(discard, 'DW_TAG_formal_parameter', 'a')

prefixes, array_type = parse_type_prefixes(attr_die(cu, a_var, 'DW_AT_type'))
# The array type is always constant, but is also restricted with GCC 6
assert_eq(set(prefixes) | {'DW_TAG_restrict_type'},
          {'DW_TAG_const_type', 'DW_TAG_restrict_type'})
assert_eq((array_type.tag, array_type.attributes['DW_AT_name'].value),
          ('DW_TAG_array_type', 'fatptr__array_type'))


# Check that the data location is correct.
match_expr(attr_expr(cu, array_type, 'DW_AT_data_location'),
           [('DW_OP_push_object_address', ),
            ('DW_OP_deref', )])


# Now check that its range is the subrange we expect
assert_eq(len(die_children(array_type)), 1)
array_range = die_child(array_type, 0)
assert_eq(subrange_root(array_range).attributes['DW_AT_name'].value, 'integer')

match_expr(attr_expr(cu, array_range, 'DW_AT_lower_bound'),
           [('DW_OP_push_object_address', ),
            ('DW_OP_plus_uconst', PTR_BYTE_SIZE),
            ('DW_OP_deref', ),
            make_deref_expr(4)])

match_expr(attr_expr(cu, array_range, 'DW_AT_upper_bound'),
           [('DW_OP_push_object_address', ),
            ('DW_OP_plus_uconst', PTR_BYTE_SIZE),
            ('DW_OP_deref', ),
            ('DW_OP_plus_uconst', 4),
            make_deref_expr(4)])
