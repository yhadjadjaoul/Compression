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

def _gaussian_kernel(size, sigma):
    """Generates a 2D Gaussian kernel."""
    x, y = np.mgrid[-size//2 + 1:size//2 + 1, -size//2 + 1:size//2 + 1]
    g = np.exp(-((x**2 + y**2)/(2.0*sigma**2)))
    return g / g.sum()

def _convolve2d(image, kernel):
    """Simple 2D convolution using numpy's stride_tricks for speed."""
    ki, kj = kernel.shape
    ii, ij = image.shape
    output_shape = (ii - ki + 1, ij - kj + 1)

    # Use sliding window view for faster convolution
    from numpy.lib.stride_tricks import sliding_window_view
    windows = sliding_window_view(image, (ki, kj))
    return np.einsum('ijkl,kl->ij', windows, kernel)

def calculate_ssim(img1, img2):
    """
    Calculate the Structural Similarity Index Measure (SSIM) between two images.
    """
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    # Handle RGB images by averaging SSIM across channels
    if len(img1.shape) == 3:
        ssims = []
        for i in range(img1.shape[2]):
            ssims.append(calculate_ssim(img1[:,:,i], img2[:,:,i]))
        return float(np.mean(ssims))

    K1 = 0.01
    K2 = 0.03
    L = 255
    C1 = (K1 * L)**2
    C2 = (K2 * L)**2

    kernel = _gaussian_kernel(11, 1.5)

    mu1 = _convolve2d(img1, kernel)
    mu2 = _convolve2d(img2, kernel)

    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = _convolve2d(img1**2, kernel) - mu1_sq
    sigma2_sq = _convolve2d(img2**2, kernel) - mu2_sq
    sigma12 = _convolve2d(img1 * img2, kernel) - mu1_mu2

    # Correct possible small negative values due to precision
    sigma1_sq[sigma1_sq < 0] = 0
    sigma2_sq[sigma2_sq < 0] = 0

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / \
               ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    return float(np.mean(ssim_map))

def calculate_vif(img1, img2):
    """
    Calculate a simplified version of Visual Information Fidelity (VIF).
    """
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    if len(img1.shape) == 3:
        vifs = []
        for i in range(img1.shape[2]):
            vifs.append(calculate_vif(img1[:,:,i], img2[:,:,i]))
        return float(np.mean(vifs))

    sigma_nsq = 2.0
    kernel = _gaussian_kernel(11, 1.5)

    num = 0.0
    den = 0.0

    # Multi-scale approach (simplified to single scale for "from scratch")
    # In a full VIF, this would be done over multiple wavelet scales

    mu1 = _convolve2d(img1, kernel)
    mu2 = _convolve2d(img2, kernel)
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = _convolve2d(img1**2, kernel) - mu1_sq
    sigma2_sq = _convolve2d(img2**2, kernel) - mu2_sq
    sigma12 = _convolve2d(img1 * img2, kernel) - mu1_mu2

    sigma1_sq[sigma1_sq < 0] = 0
    sigma2_sq[sigma2_sq < 0] = 0

    g = sigma12 / (sigma1_sq + 1e-10)
    sv_sq = sigma2_sq - g * sigma12

    g[sigma1_sq < 1e-10] = 0
    sv_sq[sigma1_sq < 1e-10] = sigma2_sq[sigma1_sq < 1e-10]
    sv_sq[sv_sq < 1e-10] = 1e-10

    num += np.sum(np.log10(1 + g**2 * sigma1_sq / (sv_sq + sigma_nsq)))
    den += np.sum(np.log10(1 + sigma1_sq / sigma_nsq))

    return float(num / (den + 1e-10))

def calculate_vmaf(img1, img2):
    """
    Calculate a representative "from scratch" version of VMAF.
    Since VMAF is a complex model, we use a weighted fusion of PSNR, SSIM, and VIF.
    """
    psnr = calculate_psnr(img1, img2)
    ssim = calculate_ssim(img1, img2)
    vif = calculate_vif(img1, img2)

    # Normalize PSNR to [0, 1] for fusion (approximate mapping)
    psnr_norm = np.clip(psnr / 50.0, 0, 1)

    # Simple weighted fusion as a representative of VMAF's fusion approach
    vmaf = 0.2 * psnr_norm + 0.4 * ssim + 0.4 * vif

    # Scale to [0, 100] to match VMAF range
    return float(vmaf * 100)
