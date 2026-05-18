import numpy as np

def rgb_to_yuv(rgb_image):
    """
    Convert an RGB image to YUV (YCbCr).
    rgb_image: numpy array of shape (H, W, 3) with values in [0, 255]
    Returns: numpy array of shape (H, W, 3)
    """
    rgb_image = rgb_image.astype(np.float32)
    yuv_image = np.zeros_like(rgb_image)

    R = rgb_image[:, :, 0]
    G = rgb_image[:, :, 1]
    B = rgb_image[:, :, 2]

    yuv_image[:, :, 0] = 0.299 * R + 0.587 * G + 0.114 * B
    yuv_image[:, :, 1] = -0.168736 * R - 0.331264 * G + 0.5 * B + 128
    yuv_image[:, :, 2] = 0.5 * R - 0.418688 * G - 0.081312 * B + 128

    return yuv_image

def yuv_to_rgb(yuv_image):
    """
    Convert a YUV (YCbCr) image to RGB.
    yuv_image: numpy array of shape (H, W, 3)
    Returns: numpy array of shape (H, W, 3) with values in [0, 255]
    """
    yuv_image = yuv_image.astype(np.float32)
    rgb_image = np.zeros_like(yuv_image)

    Y = yuv_image[:, :, 0]
    U = yuv_image[:, :, 1]
    V = yuv_image[:, :, 2]

    rgb_image[:, :, 0] = Y + 1.402 * (V - 128)
    rgb_image[:, :, 1] = Y - 0.344136 * (U - 128) - 0.714136 * (V - 128)
    rgb_image[:, :, 2] = Y + 1.772 * (U - 128)

    return np.clip(rgb_image, 0, 255).astype(np.uint8)
