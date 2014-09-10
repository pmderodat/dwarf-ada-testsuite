BE, LE = 0, 1

# LSB first
ITER_BITS = {
    BE: iter,
    LE: reversed,
}

def bytes_to_bits(bytes_list, endianness):
    result = []
    for byte in bytes_list:
        for i in range(8):
            result.append((byte >> i) & 0x1)
    return result

def bits_to_int(bits, endianness):
    result = 0
    for bit in reversed(bits):
        result = (result << 1) | bit
    return result

def int_to_bits(n, size, endianness):
    result = []
    for i in range(size):
        result.append(n & 0x1)
        n = n >> 1
    return result


class Transcoder:

    def __init__(self, endianness):
        self.endianness = endianness

    def bytes_to_bits(self, bytes_list):
        return bytes_to_bits(bytes_list, self.endianness)

    def bits_to_int(self, bits):
        return bits_to_int(bits, self.endianness)

    def int_to_bits(self, n, size):
        return int_to_bits(n, size, self.endianness)

    def bits_to_int_array(self, bits, size):
        result = []
        for offset in range(0, len(bits), size):
            bit_slice = bits[offset:offset + size]
            result.append(self.bits_to_int(bit_slice))
        return result


if __name__ == '__main__':
    t = Transcoder(LE)
    array = [129, 48, 16, 133, 113, 32, 137, 2, 96]
    a_bits = t.bytes_to_bits(array)
    print('a_bits:', a_bits)
    for i, elt in enumerate(array):
        print('  ', i, t.int_to_bits(elt, 8))

    print('--')
    for offset in range(0, 6 * 10, 6):
        bit_slice = a_bits[offset:offset + 6]
        print('{:#x}: {} -> {}'.format(
            offset,
            bit_slice,
            t.bits_to_int(bit_slice),
        ))
