from dwarf_tests import *


build('foo.adb')
cu, root = get_dwarf('foo.o')


# TODO: in 32-bit, the compiler generates big unsigned literals instead of
# small negative ones. This should be fixed.
def make_litneg_expr(lit):
    assert lit < 0
    if PTR_BYTE_SIZE == 8:
        return ('DW_OP_const1s', lit)
    else:
        return ('DW_OP_const4u', lit & (2**32 - 1))


foo = find_die(root, 'DW_TAG_subprogram', 'foo')
rec_type = find_die(foo, 'DW_TAG_structure_type', 'foo__rec_type')


# Thanks to debug type substitution, local variables should directly reference
# rec_type.
for var_name in ('r0', 'r2', 'r11'):
    var = find_die(foo, 'DW_TAG_variable', var_name)
    prefixes, var_type = parse_type_prefixes(attr_die(cu, var, 'DW_AT_type'))
    assert_eq((prefixes, var_type), (['DW_TAG_const_type'], rec_type))


# This should be true for the formal, too.
r_var = find_die(foo, 'DW_TAG_formal_parameter', 'r')
prefixes, r_type = parse_type_prefixes(attr_die(cu, r_var, 'DW_AT_type'))
assert_eq((prefixes, r_type),
          (['DW_TAG_const_type', 'DW_TAG_reference_type'], rec_type))


# Now let's check that the structure is properly described: first the byte size
# expression and then each member/variant part.

matches = match_expr(attr_expr(cu, rec_type, 'DW_AT_byte_size'),
                     [('DW_OP_push_object_address', ),
                      make_deref_expr(4),
                      ('DW_OP_call4', Match('call')),
                      ('DW_OP_plus_uconst', 11),
                      make_litneg_expr(-4),
                      ('DW_OP_and', )])
dwarf_proc = find_die_by_offset(cu, matches['call'])
assert_eq(dwarf_proc.tag, 'DW_TAG_dwarf_procedure')
assert_eq(attr_expr(cu, dwarf_proc, 'DW_AT_location'),
          [('DW_OP_pick', 0),
           ('DW_OP_lit0', ),
           ('DW_OP_ne', ),
           ('DW_OP_bra', 4),
           ('DW_OP_lit0', ),
           ('DW_OP_skip', 1),
           ('DW_OP_lit4', ),
           ('DW_OP_swap', ),
           ('DW_OP_drop', )])

i_fld, b_fld, var_part = die_children(rec_type)


def check_field(die, name, location):
    assert_eq((die.tag, die.attributes['DW_AT_name'].value),
              ('DW_TAG_member', name))
    data_member_location = die.attributes['DW_AT_data_member_location'].value
    if isinstance(location, int):
        assert_eq(location, data_member_location)
    else:
        return match_expr(data_member_location, location)


check_field(i_fld, 'i', 0)
check_field(b_fld, 'b', 4)

# Variant part: check the discriminant, the variants themselves and the fields
# they contain.
assert_eq(attr_die(cu, var_part, 'DW_AT_discr'), i_fld)
var_0, var_1_10, var_others = die_children(var_part)

# Variant when I = 0.
assert_eq(var_0.attributes['DW_AT_discr_value'].value, 0)
assert_no_attr(var_0, 'DW_AT_discr_list')
assert_eq(len(die_children(var_0)), 0)

# Variant when I in 1 .. 10.
assert_no_attr(var_1_10, 'DW_AT_discr_value')
# TODO: enhance pyelftools to decode discriminant lists.
assert_eq(var_1_10.attributes['DW_AT_discr_list'].value, [1, 1, 10])
c_fld, = die_children(var_1_10)
check_field(c_fld, 'c', 8)

# Variant when others.
assert_no_attr(var_others, 'DW_AT_discr_value')
assert_no_attr(var_others, 'DW_AT_discr_list')
# This variant may also hold a subrange type, so filter fields first.
fields = [c for c in die_children(var_others) if c.tag == 'DW_TAG_member']
n_fld, = fields
check_field(n_fld, 'n', 8)
