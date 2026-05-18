import numpy as np
from .conversions import rgb_to_yuv, yuv_to_rgb
from .dct import dct_2d, idct_2d
from .quantization import get_quantization_table, quantize, dequantize
from .zigzag import zigzag_scan, inverse_zigzag_scan
from .entropy_coding import run_length_encode, huffman_encode

class JPEGEncoder:
    def __init__(self, quality=50):
        self.quality = quality
        self.luma_table = get_quantization_table(quality, is_luminance=True)
        self.chroma_table = get_quantization_table(quality, is_luminance=False)

    def process_image(self, rgb_image):
        h, w, _ = rgb_image.shape
        # Pad image to multiples of 8
        pad_h = (8 - h % 8) % 8
        pad_w = (8 - w % 8) % 8
        padded_rgb = np.pad(rgb_image, ((0, pad_h), (0, pad_w), (0, 0)), mode='edge')

        # 1. RGB to YUV
        yuv_image = rgb_to_yuv(padded_rgb)

        h_padded, w_padded, _ = yuv_image.shape

        # We will store intermediate results for visualization
        results = {
            "original": padded_rgb,
            "r_channel": padded_rgb[:, :, 0],
            "g_channel": padded_rgb[:, :, 1],
            "b_channel": padded_rgb[:, :, 2],
            "yuv": yuv_image,
            "y_channel": yuv_image[:, :, 0],
            "u_channel": yuv_image[:, :, 1],
            "v_channel": yuv_image[:, :, 2],
            "dct": np.zeros_like(yuv_image),
            "quantized": np.zeros_like(yuv_image, dtype=np.int32),
            "reconstructed_yuv": np.zeros_like(yuv_image),
            "reconstructed_rgb": np.zeros_like(padded_rgb),
            "rle_stats": [],
            "huffman_stats": {},
            "psnr": 0.0
        }

        all_rle_data = []

        # Process each 8x8 block
        for i in range(0, h_padded, 8):
            for j in range(0, w_padded, 8):
                for c in range(3):
                    table = self.luma_table if c == 0 else self.chroma_table
                    block = yuv_image[i:i+8, j:j+8, c]

                    # 2. DCT
                    dct_block = dct_2d(block)
                    results["dct"][i:i+8, j:j+8, c] = dct_block

                    # 3. Quantization
                    quant_block = quantize(dct_block, table)
                    results["quantized"][i:i+8, j:j+8, c] = quant_block

                    # 4. ZigZag & RLE (for stats/demo)
                    zigzagged = zigzag_scan(quant_block)
                    dc, rle = run_length_encode(zigzagged)
                    all_rle_data.append((dc, rle))

                    # --- Decompression for visualization ---
                    # 5. Dequantization
                    dequant_block = dequantize(quant_block, table)

                    # 6. IDCT
                    idct_block = idct_2d(dequant_block)
                    results["reconstructed_yuv"][i:i+8, j:j+8, c] = idct_block

        # Final reconstruction
        results["reconstructed_rgb"] = yuv_to_rgb(results["reconstructed_yuv"])

        # PSNR Calculation
        mse = np.mean((padded_rgb.astype(np.float32) - results["reconstructed_rgb"].astype(np.float32)) ** 2)
        if mse == 0:
            results["psnr"] = 100.0
        else:
            max_pixel = 255.0
            results["psnr"] = 20 * np.log10(max_pixel / np.sqrt(mse))

        # Entropy coding stats (simplified)
        symbols = []
        for dc, rle in all_rle_data:
            symbols.append(f"DC:{dc}")
            for run, val in rle:
                symbols.append(f"{run},{val}")

        encoded_str, codes = huffman_encode(symbols)
        results["huffman_stats"] = {
            "total_symbols": len(symbols),
            "unique_symbols": len(codes),
            "encoded_bits": len(encoded_str),
            "original_bits": len(symbols) * 8 # assuming 8 bits per symbol for comparison
        }

        return results
