import numpy as np
from jpeg_encoder.metrics import calculate_psnr, calculate_ssim, calculate_vif, calculate_vmaf

def test_metrics():
    # Identity test
    img1 = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)
    img2 = img1.copy()

    psnr = calculate_psnr(img1, img2)
    ssim = calculate_ssim(img1, img2)
    vif = calculate_vif(img1, img2)
    vmaf = calculate_vmaf(img1, img2)

    print(f"Identity - PSNR: {psnr}, SSIM: {ssim}, VIF: {vif}, VMAF: {vmaf}")
    assert psnr >= 100.0
    assert np.isclose(ssim, 1.0)
    assert np.isclose(vif, 1.0)
    assert vmaf > 90.0 # Should be high

    # Degraded test
    img3 = np.zeros((128, 128, 3), dtype=np.uint8)
    psnr_deg = calculate_psnr(img1, img3)
    ssim_deg = calculate_ssim(img1, img3)
    vif_deg = calculate_vif(img1, img3)
    vmaf_deg = calculate_vmaf(img1, img3)

    print(f"Degraded - PSNR: {psnr_deg}, SSIM: {ssim_deg}, VIF: {vif_deg}, VMAF: {vmaf_deg}")
    assert psnr_deg < psnr
    assert ssim_deg < ssim
    assert vif_deg < vif
    assert vmaf_deg < vmaf

if __name__ == "__main__":
    test_metrics()
    print("All metric tests passed!")
