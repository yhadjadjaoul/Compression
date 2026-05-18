import numpy as np
from jpeg_encoder.zigzag import zigzag_scan, inverse_zigzag_scan

def test_zigzag():
    original_block = np.arange(64).reshape((8, 8))
    zigzagged = zigzag_scan(original_block)
    reconstructed = inverse_zigzag_scan(zigzagged)

    print("Original Block:\n", original_block[:2, :4])
    print("Zigzagged:\n", zigzagged[:10])
    print("Reconstructed:\n", reconstructed[:2, :4])

    if np.array_equal(original_block, reconstructed):
        print("Test Passed!")
    else:
        print("Test Failed!")

if __name__ == "__main__":
    test_zigzag()
