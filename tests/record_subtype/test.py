from dwarf_tests import *


build('bar.ads')
cu, root = get_dwarf('bar.o')


r1_type = find_die(root, 'DW_TAG_structure_type', 'bar__r1_t')
r5_type = find_die(root, 'DW_TAG_structure_type', 'bar__r5_t')
r7_type = find_die(root, 'DW_TAG_structure_type', 'bar__r7_t')


def check_var(name, var_type):
    var = find_die(root, 'DW_TAG_variable', name)
    assert_eq(attr_die(cu, var, 'DW_AT_type'), var_type)


# Check that all subtypes from the same record type are all the same in DWARF.
check_var('bar__r1', r1_type)
check_var('bar__r2', r1_type)
check_var('bar__r3', r1_type)
check_var('bar__r4', r1_type)

# Same here.
check_var('bar__r5', r5_type)
check_var('bar__r6', r5_type)

# ... but derived types must be different.
check_var('bar__r7', r7_type)
