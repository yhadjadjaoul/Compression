import numpy as np
from jpeg_encoder.dct import dct_2d, idct_2d

def test_dct():
    original_block = np.random.randint(0, 256, (8, 8)).astype(np.uint8)

    dct_block = dct_2d(original_block)
    reconstructed_block = idct_2d(dct_block)

    print("Original Block (first 4x4):\n", original_block[:4, :4])
    print("Reconstructed Block (first 4x4):\n", reconstructed_block[:4, :4].astype(np.uint8))

    diff = np.abs(original_block.astype(np.float32) - reconstructed_block)
    print("Max difference:", np.max(diff))

    if np.max(diff) < 1e-3:
        print("Test Passed!")
    else:
        print("Test Failed!")

if __name__ == "__main__":
    test_dct()
