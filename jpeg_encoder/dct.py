import numpy as np

def get_dct_matrix(n=8):
    """
    Generate the n x n DCT transformation matrix.
    """
    dct_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == 0:
                dct_matrix[i, j] = 1 / np.sqrt(n)
            else:
                dct_matrix[i, j] = np.sqrt(2 / n) * np.cos((2 * j + 1) * i * np.pi / (2 * n))
    return dct_matrix

DCT_MATRIX_8x8 = get_dct_matrix(8)

def dct_2d(block):
    """
    Apply 2D DCT to an 8x8 block.
    """
    # Shift to range [-128, 127]
    block = block.astype(np.float32) - 128
    return np.dot(DCT_MATRIX_8x8, np.dot(block, DCT_MATRIX_8x8.T))

def idct_2d(dct_block):
    """
    Apply 2D IDCT to an 8x8 block.
    """
    # IDCT: T' * block * T
    block = np.dot(DCT_MATRIX_8x8.T, np.dot(dct_block, DCT_MATRIX_8x8))
    # Shift back to range [0, 255]
    return np.clip(block + 128, 0, 255)
