from dwarf_tests import *


build('foo.adb')
cu, root = get_dwarf('foo.o')


class BinaryScaleMatcher(object):
    def __init__(self, scale):
        self.scale = scale

    def match(self, cu, base_type):
        assert_no_attr(base_type, 'DW_AT_decimal_scale')
        assert_no_attr(base_type, 'DW_AT_small')
        assert_eq(base_type.attributes['DW_AT_binary_scale'].value,
                  self.scale)


class DecimalScaleMatcher(object):
    def __init__(self, scale):
        self.scale = scale

    def match(self, cu, base_type):
        assert_no_attr(base_type, 'DW_AT_binary_scale')
        assert_no_attr(base_type, 'DW_AT_small')
        assert_eq(base_type.attributes['DW_AT_decimal_scale'].value,
                  self.scale)


class SmallMatcher(object):
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def match(self, cu, base_type):
        assert_no_attr(base_type, 'DW_AT_binary_scale')
        assert_no_attr(base_type, 'DW_AT_decimal_scale')

        small = attr_die(cu, base_type, 'DW_AT_small')
        assert_eq(small.tag, DW_TAG_GNU_rational_constant)
        assert_eq(small.attributes[DW_AT_GNU_numerator].value,
                  self.numerator)
        assert_eq(small.attributes[DW_AT_GNU_denominator].value,
                  self.denominator)


def check_fp_array(var_name,
                   subrange_name, bounds,
                   base_name, matcher):
    # Extract the floating-point type behind the array variable.
    var = find_die(root, 'DW_TAG_variable', var_name)
    prefixes, array_type = parse_type_prefixes(attr_die(cu, var, 'DW_AT_type'))
    assert_eq(prefixes, ['DW_TAG_const_type'])
    assert_eq(array_type.tag, 'DW_TAG_array_type')

    # Check first the subrange.
    fp_type = attr_die(cu, array_type, 'DW_AT_type')
    assert_eq((fp_type.tag, fp_type.attributes['DW_AT_name'].value),
              ('DW_TAG_subrange_type', subrange_name))
    assert_eq(fp_type.attributes['DW_AT_lower_bound'].value, bounds[0])
    assert_eq(fp_type.attributes['DW_AT_upper_bound'].value, bounds[1])

    # Then check the subtype.
    base_type = subrange_root(fp_type)
    assert_eq((base_type.tag, base_type.attributes['DW_AT_name'].value),
              ('DW_TAG_base_type', base_name))
    matcher.match(cu, base_type)


check_fp_array('a1',
               'foo__fp1_type', (240, 16),
               'foo__Tfp1_typeB', BinaryScaleMatcher(-4))
check_fp_array('a2',
               'foo__fp2_type', (0xffffa50cef85c001, 0x5af3107a3fff),
               'foo__Tfp2_typeB', DecimalScaleMatcher(-2))
check_fp_array('a3',
               'foo__fp3_type', (0, 30),
               'foo__Tfp3_typeB', SmallMatcher(1, 30))
check_fp_array(
    'a4',
    'foo__fp4_type___XF_1_10000000000000000000_1_30000000000000000000',
    (0, 30),
    'foo__Tfp4_typeB___XF_1_10000000000000000000_1_30000000000000000000',
    SmallMatcher(0, 0))
