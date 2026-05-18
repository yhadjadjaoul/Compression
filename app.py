from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import io
import base64
from jpeg_encoder.encoder import JPEGEncoder

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def array_to_base64_img(arr):
    """
    Convert a numpy array to a base64 encoded PNG image for display.
    """
    # Clip and convert to uint8 if necessary
    if arr.dtype != np.uint8:
        # For visualization of DCT/YUV, we might need to normalize or shift
        # But for simple reconstruction, we just clip
        arr = np.clip(arr, 0, 255).astype(np.uint8)

    img = Image.fromarray(arr)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def dct_to_base64_img(arr):
    """
    Visualize DCT coefficients by applying log scaling.
    """
    # Take the absolute value and apply log scaling for better visualization
    # Shift to positive range
    arr_abs = np.abs(arr)
    arr_log = np.log1p(arr_abs)
    # Normalize to [0, 255]
    arr_min = np.min(arr_log)
    arr_max = np.max(arr_log)
    if arr_max > arr_min:
        arr_norm = (arr_log - arr_min) / (arr_max - arr_min) * 255
    else:
        arr_norm = arr_log * 0
    return array_to_base64_img(arr_norm.astype(np.uint8))

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

    # Prepare data for frontend
    response_data = {
        "original": array_to_base64_img(results["original"]),
        "y_channel": array_to_base64_img(results["y_channel"]),
        "u_channel": array_to_base64_img(results["u_channel"]),
        "v_channel": array_to_base64_img(results["v_channel"]),
        "dct_y": dct_to_base64_img(results["dct"][:, :, 0]),
        "reconstructed": array_to_base64_img(results["reconstructed_rgb"]),
        "huffman_stats": results["huffman_stats"]
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
