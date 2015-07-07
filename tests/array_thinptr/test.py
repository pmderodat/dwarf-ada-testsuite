from dwarf_tests import *


gnatmake('thinptr.adb')
cu, root = get_dwarf('thinptr.o')


# Get the array type referenced by the AA formal parameter: it's really a
# constant typedef around a pointer to the array type.
put_line = find_die(root, 'DW_TAG_subprogram', 'thinptr__put_line')
aa_var = find_die(put_line, 'DW_TAG_formal_parameter', 'aa')

prefixes, array_type = parse_type_prefixes(attr_die(cu, aa_var, 'DW_AT_type'))
assert_eq(prefixes, ['DW_TAG_const_type'])

array_type = peel_typedef(cu, array_type)
prefixes, array_type = parse_type_prefixes(array_type)
assert_eq(prefixes, ['DW_TAG_pointer_type'])

assert_eq((array_type.tag, array_type.attributes['DW_AT_name'].value),
          ('DW_TAG_array_type', 'thinptr__array_type'))


# Arrays below thin pointers don't need a data location: the pointer already
# points to the array data.
assert_no_attr(array_type, 'DW_AT_data_location')


# Now check that its range is the subrange we expect
assert_eq(len(die_children(array_type)), 1)
array_range = die_child(array_type, 0)
assert_eq(subrange_root(array_range).attributes['DW_AT_name'].value, 'integer')

assert_eq(attr_expr(cu, array_range, 'DW_AT_lower_bound'),
          [('DW_OP_push_object_address', ),
           ('DW_OP_const1s', -8),
           ('DW_OP_plus', ),
           ('DW_OP_deref_size', 4)])

assert_eq(attr_expr(cu, array_range, 'DW_AT_upper_bound'),
          [('DW_OP_push_object_address', ),
           ('DW_OP_const1s', -8),
           ('DW_OP_plus', ),
           ('DW_OP_plus_uconst', 4),
           ('DW_OP_deref_size', 4)])
