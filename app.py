from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import io
import base64
from jpeg_encoder.encoder import JPEGEncoder
from jpeg_encoder.conversions import yuv_to_rgb
from jpeg_encoder.quantization import get_quantization_table, LUMINANCE_TABLE

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quantization')
def quantization_lab():
    return render_template('quantization.html')

@app.route('/api/quantization_data', methods=['POST'])
def quantization_data():
    data = request.get_json()
    quality = int(data.get('quality', 50))
    base_table = LUMINANCE_TABLE.astype(int).tolist()
    resulting_table = get_quantization_table(quality, is_luminance=True).astype(int).tolist()

    if quality < 50:
        scale = 5000 / quality
    else:
        scale = 200 - 2 * quality

    return jsonify({
        "base_table": base_table,
        "resulting_table": resulting_table,
        "scale": scale / 100.0
    })

@app.route('/api/quantization_preview', methods=['POST'])
def quantization_preview():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    quality = int(request.form.get('quality', 50))

    img = Image.open(file.stream).convert('RGB')
    img_array = np.array(img)

    encoder = JPEGEncoder(quality=quality)
    results = encoder.process_image(img_array)

    return jsonify({
        "original": array_to_base64_img(results["original"]),
        "reconstructed": array_to_base64_img(results["reconstructed_rgb"]),
        "psnr": float(results["psnr"])
    })

def array_to_base64_img(arr, format="PNG"):
    """
    Convert a numpy array to a base64 encoded image for display or download.
    """
    # Clip and convert to uint8 if necessary
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)

    img = Image.fromarray(arr)
    buffered = io.BytesIO()
    img.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def visualize_channel_arr(arr, channel_type):
    """
    Create a colored visualization of a single channel and return it as a numpy array.
    channel_type: 'R', 'G', 'B', 'Y', 'U', 'V'
    """
    h, w = arr.shape
    vis = np.zeros((h, w, 3), dtype=np.uint8)
    arr_uint8 = np.clip(arr, 0, 255).astype(np.uint8)

    if channel_type == 'R':
        vis[:, :, 0] = arr_uint8
    elif channel_type == 'G':
        vis[:, :, 1] = arr_uint8
    elif channel_type == 'B':
        vis[:, :, 2] = arr_uint8
    elif channel_type == 'Y':
        # Grayscale for Y
        vis[:, :, 0] = vis[:, :, 1] = vis[:, :, 2] = arr_uint8
    elif channel_type == 'U':
        # Visualize U (Cb): Fix Y=128, V=128
        yuv = np.zeros((h, w, 3), dtype=np.float32)
        yuv[:, :, 0] = 128
        yuv[:, :, 1] = arr
        yuv[:, :, 2] = 128
        return yuv_to_rgb(yuv)
    elif channel_type == 'V':
        # Visualize V (Cr): Fix Y=128, U=128
        yuv = np.zeros((h, w, 3), dtype=np.float32)
        yuv[:, :, 0] = 128
        yuv[:, :, 1] = 128
        yuv[:, :, 2] = arr
        return yuv_to_rgb(yuv)

    return vis

def visualize_channel(arr, channel_type, format="PNG"):
    """
    Create a colored visualization of a single channel and return it as base64.
    """
    vis = visualize_channel_arr(arr, channel_type)
    return array_to_base64_img(vis, format=format)

def dct_to_arr(arr):
    """
    Visualize DCT coefficients by applying log scaling and return it as a numpy array.
    """
    # Take the absolute value and apply log scaling for better visualization
    arr_abs = np.abs(arr)
    arr_log = np.log1p(arr_abs)
    # Normalize to [0, 255]
    arr_min = np.min(arr_log)
    arr_max = np.max(arr_log)
    if arr_max > arr_min:
        arr_norm = (arr_log - arr_min) / (arr_max - arr_min) * 255
    else:
        arr_norm = arr_log * 0
    return arr_norm.astype(np.uint8)

def dct_to_base64_img(arr, format="PNG"):
    """
    Visualize DCT coefficients by applying log scaling and return it as base64.
    """
    return array_to_base64_img(dct_to_arr(arr), format=format)

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    quality = int(request.form.get('quality', 50))

    img = Image.open(file.stream).convert('RGB')
    img_array = np.array(img)

    encoder = JPEGEncoder(quality=quality)
    results = encoder.process_image(img_array)

    # Generate quality metrics vs Quality data
    metrics_plot_data = []
    qualities = [10, 25, 50, 75, 100] # Reduced number of points for performance
    for q in qualities:
        temp_encoder = JPEGEncoder(quality=q)
        temp_results = temp_encoder.process_image(img_array)
        metrics_plot_data.append({
            "quality": q,
            "psnr": float(temp_results["psnr"]),
            "ssim": float(temp_results["ssim"]),
            "vif": float(temp_results["vif"]),
            "vmaf": float(temp_results["vmaf"])
        })

    # Prepare data for frontend
    response_data = {
        "original": array_to_base64_img(results["original"]),
        "original_bmp": array_to_base64_img(results["original"], format="BMP"),
        "r_channel": visualize_channel(results["r_channel"], 'R'),
        "r_channel_bmp": visualize_channel(results["r_channel"], 'R', format="BMP"),
        "g_channel": visualize_channel(results["g_channel"], 'G'),
        "g_channel_bmp": visualize_channel(results["g_channel"], 'G', format="BMP"),
        "b_channel": visualize_channel(results["b_channel"], 'B'),
        "b_channel_bmp": visualize_channel(results["b_channel"], 'B', format="BMP"),
        "y_channel": visualize_channel(results["y_channel"], 'Y'),
        "y_channel_bmp": visualize_channel(results["y_channel"], 'Y', format="BMP"),
        "u_channel": visualize_channel(results["u_channel"], 'U'),
        "u_channel_bmp": visualize_channel(results["u_channel"], 'U', format="BMP"),
        "v_channel": visualize_channel(results["v_channel"], 'V'),
        "v_channel_bmp": visualize_channel(results["v_channel"], 'V', format="BMP"),
        "dct_y": dct_to_base64_img(results["dct"][:, :, 0]),
        "dct_y_bmp": dct_to_base64_img(results["dct"][:, :, 0], format="BMP"),
        "reconstructed": array_to_base64_img(results["reconstructed_rgb"]),
        "reconstructed_bmp": array_to_base64_img(results["reconstructed_rgb"], format="BMP"),
        "reconstructed_jpg": array_to_base64_img(results["reconstructed_rgb"], format="JPEG"),
        "psnr": float(results["psnr"]),
        "ssim": float(results["ssim"]),
        "vif": float(results["vif"]),
        "vmaf": float(results["vmaf"]),
        "metrics_plot_data": metrics_plot_data,
        "huffman_stats": results["huffman_stats"]
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
