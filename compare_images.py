import argparse
import numpy as np
from PIL import Image
from jpeg_encoder.metrics import calculate_psnr, calculate_ssim, calculate_vif, calculate_vmaf

def main():
    parser = argparse.ArgumentParser(description="Compare two images using quality metrics.")
    parser.add_argument("original", help="Path to the original image.")
    parser.add_argument("reconstructed", help="Path to the reconstructed image.")
    parser.add_argument("--metric", choices=["psnr", "ssim", "vif", "vmaf", "all"], default="all", help="Quality metric to compute.")

    args = parser.parse_args()

    img1 = np.array(Image.open(args.original).convert("RGB"))
    img2 = np.array(Image.open(args.reconstructed).convert("RGB"))

    metrics = {}
    if args.metric in ["psnr", "all"]:
        metrics["PSNR"] = calculate_psnr(img1, img2)
    if args.metric in ["ssim", "all"]:
        metrics["SSIM"] = calculate_ssim(img1, img2)
    if args.metric in ["vif", "all"]:
        metrics["VIF"] = calculate_vif(img1, img2)
    if args.metric in ["vmaf", "all"]:
        metrics["VMAF"] = calculate_vmaf(img1, img2)

    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")

if __name__ == "__main__":
    main()
