from dwarf_tests import *


build('foo.adb')
cu, root = get_dwarf('foo.o')


foo = find_die(root, 'DW_TAG_subprogram', 'foo')
# TODO: because of interactions with nested subprograms, the compiler sometimes
# emit nested types at the top-level. This should be fixed.
rec_type = find_die(root, 'DW_TAG_structure_type', 'foo__rec_type')


# TODO: in 32-bit, the compiler generates big unsigned literals instead of
# small negative ones. This should be fixed.
def make_litneg_expr(lit):
    assert lit < 0
    if PTR_BYTE_SIZE == 8:
        return ('DW_OP_const1s', lit)
    else:
        return ('DW_OP_const4u', lit & (2**32 - 1))


matches = match_expr(attr_expr(cu, rec_type, 'DW_AT_byte_size'),
                     [('DW_OP_push_object_address', ),
                      ('DW_OP_plus_uconst', 4),
                      make_deref_expr(4),
                      ('DW_OP_push_object_address', ),
                      make_deref_expr(4),
                      ('DW_OP_call4', Match('call'))])
matches = match_dwarf_proc(cu, matches['call'],
                           [('DW_OP_pick', 0),
                            ('DW_OP_lit0', ),
                            ('DW_OP_lt', ),
                            ('DW_OP_bra', 5),
                            ('DW_OP_pick', 0),
                            ('DW_OP_skip', 1),
                            ('DW_OP_lit0', ),
                            ('DW_OP_plus_uconst', 12),
                            make_litneg_expr(-4),
                            ('DW_OP_and', ),
                            ('DW_OP_pick', 2),
                            ('DW_OP_pick', 2),
                            ('DW_OP_call4', Match('call')),
                            ('DW_OP_plus', ),
                            ('DW_OP_plus_uconst', 3),
                            make_litneg_expr(-4),
                            ('DW_OP_and', ),
                            ('DW_OP_swap', ),
                            ('DW_OP_drop', ),
                            ('DW_OP_swap', ),
                            ('DW_OP_drop', )])
matches = match_dwarf_proc(cu, matches['call'],
                           [('DW_OP_pick', 0),
                            ('DW_OP_lit0', ),
                            ('DW_OP_ne', ),
                            ('DW_OP_bra', 4),
                            ('DW_OP_lit0', ),
                            ('DW_OP_skip', 28 if PTR_BYTE_SIZE == 8 else 31),
                            ('DW_OP_pick', 0),
                            ('DW_OP_lit0', ),
                            ('DW_OP_gt', ),
                            ('DW_OP_pick', 1),
                            ('DW_OP_lit10', ),
                            ('DW_OP_le', ),
                            ('DW_OP_and', ),
                            ('DW_OP_bra', 4),
                            ('DW_OP_lit4', ),
                            ('DW_OP_skip', 12 if PTR_BYTE_SIZE == 8 else 15),
                            ('DW_OP_pick', 1),
                            ('DW_OP_call4', Match('call')),
                            ('DW_OP_plus_uconst', 3),
                            make_litneg_expr(-4),
                            ('DW_OP_and', ),
                            ('DW_OP_swap', ),
                            ('DW_OP_drop', ),
                            ('DW_OP_swap', ),
                            ('DW_OP_drop', )])
matches = match_dwarf_proc(cu, matches['call'],
                           [('DW_OP_pick', 0),
                            ('DW_OP_lit0', ),
                            ('DW_OP_lt', ),
                            ('DW_OP_bra', 5),
                            ('DW_OP_pick', 0),
                            ('DW_OP_skip', 1),
                            ('DW_OP_lit0', ),
                            ('DW_OP_plus_uconst', 3),
                            make_litneg_expr(-4),
                            ('DW_OP_and', ),
                            ('DW_OP_pick', 1),
                            ('DW_OP_call4', Match('call')),
                            ('DW_OP_plus', ),
                            ('DW_OP_plus_uconst', 3),
                            make_litneg_expr(-4),
                            ('DW_OP_and', ),
                            ('DW_OP_swap', ),
                            ('DW_OP_drop', )])
matches = match_dwarf_proc(cu, matches['call'],
                           [('DW_OP_pick', 0),
                            ('DW_OP_lit0', ),
                            ('DW_OP_ne', ),
                            ('DW_OP_bra', 4),
                            ('DW_OP_lit0', ),
                            ('DW_OP_skip', 1),
                            ('DW_OP_lit4', ),
                            ('DW_OP_swap', ),
                            ('DW_OP_drop', )])


# Check the structure of this record type.

def filter_members(die):
    return [c for c in die_children(die)
            if c.tag in ('DW_TAG_member', 'DW_TAG_variant_part')]


def check_field(cu, die, name, location):
    assert_eq((die.tag, die.attributes['DW_AT_name'].value),
              ('DW_TAG_member', name))
    if isinstance(location, int):
        dml = die.attributes['DW_AT_data_member_location'].value
        assert_eq(location, dml)
    else:
        dml = attr_expr(cu, die, 'DW_AT_data_member_location')
        return match_expr(dml, location)


def check_variant(cu, die, dvalue=None, dlist=None):
    assert_eq(die.tag, 'DW_TAG_variant')
    if dvalue is None:
        assert_no_attr(die, 'DW_AT_discr_value')
    else:
        assert_eq(die.attributes['DW_AT_discr_value'].value, dvalue)
    if dlist is None:
        assert_no_attr(die, 'DW_AT_discr_list')
    else:
        assert_eq(die.attributes['DW_AT_discr_list'].value, dlist)

    return filter_members(die)

def check_variant_part(cu, die, discr):
    assert_eq((die.tag, attr_die(cu, die, 'DW_AT_discr')),
              ('DW_TAG_variant_part', discr))
    return die_children(die)

i1_fld, i2_fld, b_fld, s1_fld, i1_var = filter_members(rec_type)

# Top-level members
check_field(cu, i1_fld, 'i1', 0)
check_field(cu, i2_fld, 'i2', 4)
check_field(cu, b_fld, 'b', 8)
check_field(cu, s1_fld, 's1', 9)

var_0, var_1_10, var_others = check_variant_part(cu, i1_var, i1_fld)

# 1. Top-level variant part: first variant
assert_eq([], check_variant(cu, var_0, dvalue=0))

# 2. Top-level variant part: second variant
s2_fld, i2_var = check_variant(cu, var_1_10, dlist=[1, 1, 10])

matches = check_field(cu, s2_fld, 's2', [('DW_OP_call4', Match('call')),
                                         ('DW_OP_plus', )])
match_dwarf_proc(cu, matches['call'],
                 [('DW_OP_push_object_address', ),
                  make_deref_expr(4),
                  ('DW_OP_lit0', ),
                  ('DW_OP_lt', ),
                  ('DW_OP_bra', 6 if PTR_BYTE_SIZE == 8 else 5),
                  ('DW_OP_push_object_address', ),
                  make_deref_expr(4),
                  ('DW_OP_skip', 1),
                  ('DW_OP_lit0', ),
                  ('DW_OP_plus_uconst', 12),
                  make_litneg_expr(-4),
                  ('DW_OP_and', )])

i2_var_0, i2_var_2_20_22, i2_var_others = check_variant_part(cu, i2_var,
                                                             i2_fld)

# 2.1. Nested variant part: first variant
assert_eq([], check_variant(cu, i2_var_0, dvalue=0))

# 2.2. Nested variant part: second variant
c_fld, = check_variant(cu, i2_var_2_20_22, dlist=[1, 2, 20, 0, 22])
matches = check_field(cu, c_fld, 'c', [('DW_OP_call4', Match('call')),
                                       ('DW_OP_plus', )])
c_fld_loc_call = matches['call']
matches = match_dwarf_proc(cu, c_fld_loc_call,
                           [('DW_OP_call4', Match('call')),
                            ('DW_OP_push_object_address', ),
                            ('DW_OP_plus_uconst', 4),
                            make_deref_expr(4),
                            ('DW_OP_lit0', ),
                            ('DW_OP_lt', ),
                            ('DW_OP_bra', 8 if PTR_BYTE_SIZE == 8 else 7),
                            ('DW_OP_push_object_address', ),
                            ('DW_OP_plus_uconst', 4),
                            make_deref_expr(4),
                            ('DW_OP_skip', 1),
                            ('DW_OP_lit0', ),
                            ('DW_OP_plus_uconst', 3),
                            make_litneg_expr(-4),
                            ('DW_OP_and', ),
                            ('DW_OP_plus', )])
n1_fld_loc_call = matches['call']
match_dwarf_proc(cu, n1_fld_loc_call,
                 [('DW_OP_push_object_address', ),
                  make_deref_expr(4),
                  ('DW_OP_lit0', ),
                  ('DW_OP_lt', ),
                  ('DW_OP_bra', 6 if PTR_BYTE_SIZE == 8 else 5),
                  ('DW_OP_push_object_address', ),
                  make_deref_expr(4),
                  ('DW_OP_skip', 1),
                  ('DW_OP_lit0', ),
                  ('DW_OP_plus_uconst', 12),
                  make_litneg_expr(-4),
                  ('DW_OP_and', )])

# 2.3. Nested variant part: third variant

n2_fld, = check_variant(cu, i2_var_others)
matches = check_field(cu, n2_fld, 'n2', [('DW_OP_call4', Match('call')),
                                         ('DW_OP_plus', )])
# This field should have the same location as the N one.
assert_eq(matches['call'], c_fld_loc_call)

# 2.3. Top-level variant part: third variant
n1_fld, = check_variant(cu, var_others)
matches = check_field(cu, n1_fld, 'n1', [('DW_OP_call4', Match('call')),
                                         ('DW_OP_plus', )])
# Rely on the fact that N1 and C share common code to compute their location.
assert_eq(matches['call'], n1_fld_loc_call)
