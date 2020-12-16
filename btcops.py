"""
sonicskye@2020

Bitcoin-related operations
"""

from hashlib import sha256
import binascii


def header_hash(header_hex):
    # Reverse inputs before and after hashing
    # due to big-endian / little-endian nonsense
    #a1 = binascii.unhexlify(header_hex)[::-1]
    a1 = binascii.unhexlify(header_hex)
    # double sha256 of a1
    #h = hashlib.sha256(hashlib.sha256(a1).digest()).digest()
    #return binascii.hexlify(h[::-1]).decode() # add .decode() here if you want str instead of bytes
    return binascii.hexlify(sha256(sha256(a1).digest()).digest()[::-1]).decode()