import numpy as np

# Standard JPEG ZigZag order (indices in a flattened 8x8 block)
ZIGZAG_ORDER = [
     0,  1,  8, 16,  9,  2,  3, 10,
    17, 24, 32, 25, 18, 11,  4,  5,
    12, 19, 26, 33, 40, 48, 41, 34,
    27, 20, 13,  6,  7, 14, 21, 28,
    35, 42, 49, 56, 57, 50, 43, 36,
    29, 22, 15, 23, 30, 37, 44, 51,
    58, 59, 52, 45, 38, 31, 39, 46,
    53, 60, 61, 54, 47, 55, 62, 63
]

def zigzag_scan(block):
    """
    Perform zigzag scan on an 8x8 block.
    """
    flat = block.flatten()
    zigzagged = np.zeros(64, dtype=block.dtype)
    for i in range(64):
        zigzagged[i] = flat[ZIGZAG_ORDER[i]]
    return zigzagged

def inverse_zigzag_scan(zigzagged):
    """
    Perform inverse zigzag scan to reconstruct an 8x8 block.
    """
    block = np.zeros(64, dtype=zigzagged.dtype)
    for i in range(64):
        block[ZIGZAG_ORDER[i]] = zigzagged[i]
    return block.reshape((8, 8))
