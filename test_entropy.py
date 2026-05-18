import numpy as np
from jpeg_encoder.entropy_coding import run_length_encode, huffman_encode

def test_entropy():
    # Sample quantized zigzagged block
    zigzagged = np.zeros(64, dtype=np.int32)
    zigzagged[0] = 50 # DC
    zigzagged[1] = 10
    zigzagged[2] = -5
    zigzagged[5] = 2
    # Others are 0

    dc, rle = run_length_encode(zigzagged)
    print("DC:", dc)
    print("RLE:", rle)

    # Huffman test
    data = ["A", "B", "A", "C", "B", "A"]
    encoded, codes = huffman_encode(data)
    print("Huffman Codes:", codes)
    print("Encoded String:", encoded)

    if len(rle) > 0 and len(codes) > 0:
        print("Test Passed!")
    else:
        print("Test Failed!")

if __name__ == "__main__":
    test_entropy()
