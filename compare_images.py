import argparse
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from jpeg_encoder.metrics import calculate_psnr, calculate_ssim, calculate_vif, calculate_vmaf
from jpeg_encoder.encoder import JPEGEncoder

def main():
    parser = argparse.ArgumentParser(description="Compare two images using quality metrics.")
    parser.add_argument("original", help="Path to the original image.")
    parser.add_argument("reconstructed", nargs="?", help="Path to the reconstructed image (optional if plotting).")
    parser.add_argument("--metric", choices=["psnr", "ssim", "vif", "vmaf", "all"], default="all", help="Quality metric to compute.")
    parser.add_argument("--plot", action="store_true", help="Generate a quality vs metric plot.")
    parser.add_argument("--output", default="quality_plot.png", help="Output path for the plot.")

    args = parser.parse_args()

    img1 = np.array(Image.open(args.original).convert("RGB"))

    if args.plot:
        qualities = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        results = { "psnr": [], "ssim": [], "vif": [], "vmaf": [] }

        print("Generating plot data...")
        for q in qualities:
            encoder = JPEGEncoder(quality=q)
            res = encoder.process_image(img1)
            results["psnr"].append(res["psnr"])
            results["ssim"].append(res["ssim"])
            results["vif"].append(res["vif"])
            results["vmaf"].append(res["vmaf"])

        plt.figure(figsize=(10, 6))
        metrics_to_plot = ["psnr", "ssim", "vif", "vmaf"] if args.metric == "all" else [args.metric]

        for m in metrics_to_plot:
            plt.plot(qualities, results[m], label=m.upper(), marker='o')

        plt.title(f"JPEG Quality vs {args.metric.upper()}")
        plt.xlabel("Quality Level")
        plt.ylabel("Score")
        plt.legend()
        plt.grid(True)
        plt.savefig(args.output)
        print(f"Plot saved to {args.output}")

    if args.reconstructed:
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
