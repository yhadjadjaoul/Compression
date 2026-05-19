import numpy as np

def calculate_psnr(original, reconstructed):
    """
    Calculate the Peak Signal-to-Noise Ratio (PSNR) between two images.

    Args:
        original: Original image as a numpy array.
        reconstructed: Reconstructed image as a numpy array.

    Returns:
        psnr: Calculated PSNR value.
    """
    mse = np.mean((original.astype(np.float32) - reconstructed.astype(np.float32)) ** 2)
    if mse == 0:
        return 100.0

    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr
