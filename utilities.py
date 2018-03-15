import re

def lo8(x):
    return x & 0xff


def hi8(x):
    return x >> 8


def lo4(x):
    return x & 0xf


def hi4(x):
    return x >> 4


def _bv(bit):
    return 1 << bit


def reverse_bits(byte):
    byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
    byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
    byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
    return byte


def bytes_to_hex(nbytes):
    """
    :param nbytes
    This script will print out a byte array in a human readable format 
    (hexadecimal). This is often useful during debugging. 
    """
    return '[{}]'.format(', '.join(hex(x) for x in nbytes))
