from dwarf_tests import *


gnatmake('foo.adb')
cu, root = get_dwarf('foo.o')


range_type = find_die(root, 'DW_TAG_enumeration_type', 'foo__range_type')


def check_array_var(var_name, type_name, expected_bounds):
    var = find_die(root, 'DW_TAG_variable', var_name)

    # We expect the type to be wrapped inside a typedef: unwrap it.
    var_type = attr_die(cu, var, 'DW_AT_type')
    assert_eq(var_type.tag, 'DW_TAG_typedef')
    array_type = attr_die(cu, var_type, 'DW_AT_type')
    assert_eq((array_type.tag, array_type.attributes['DW_AT_name'].value),
              ('DW_TAG_array_type', type_name))

    # We expect the array to have exactly one dimension whose index is a
    # subrange of range_type.
    assert_eq(len(die_children(array_type)), 1)
    array_range = die_child(array_type, 0)
    assert_eq(subrange_root(array_range), range_type)
    if expected_bounds[0] == 1:
        assert_no_attr(array_range, 'DW_AT_lower_bound')
    else:
        assert_eq(array_range.attributes['DW_AT_lower_bound'].value,
                  expected_bounds[0])
    assert_eq(array_range.attributes['DW_AT_upper_bound'].value,
              expected_bounds[1])


check_array_var('a', 'foo__array_type', (0, 1))
check_array_var('a2', 'foo__array2_type', (1, 2))
check_array_var('a3', 'foo__array3_type', (1, 2))
