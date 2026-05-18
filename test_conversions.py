import numpy as np
from jpeg_encoder.conversions import rgb_to_yuv, yuv_to_rgb

def test_conversion():
    original_rgb = np.array([
        [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
        [[255, 255, 255], [0, 0, 0], [128, 128, 128]]
    ], dtype=np.uint8)

    yuv = rgb_to_yuv(original_rgb)
    reconstructed_rgb = yuv_to_rgb(yuv)

    print("Original RGB:\n", original_rgb)
    print("Reconstructed RGB:\n", reconstructed_rgb)

    diff = np.abs(original_rgb.astype(np.int16) - reconstructed_rgb.astype(np.int16))
    print("Max difference:", np.max(diff))

    if np.max(diff) <= 1:
        print("Test Passed!")
    else:
        print("Test Failed!")

if __name__ == "__main__":
    test_conversion()
