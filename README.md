# JPEG Encoder from Scratch

This project is a modular JPEG encoder built from scratch using Python and NumPy. It's designed for educational use in video compression courses. It includes a Flask-based web interface to visualize intermediate encoding steps and compression statistics.

## Features

- RGB to YUV conversion
- 8x8 block-based Discrete Cosine Transform (DCT)
- Quantization with adjustable quality levels
- ZigZag scanning
- Entropy coding using Run-Length Encoding (RLE) and Huffman coding
- Web-based visualization tool

## Installation

To run this project, you need Python 3 and the following dependencies:

```bash
pip install numpy Pillow flask
```

## How to Run

### Web Interface

To launch the web application and visualize the JPEG encoding process:

```bash
python3 app.py
```
Then open your browser and navigate to `http://localhost:5000`.

### Generate Sample Image

If you need a sample image to test the encoder, you can generate one:

```bash
python3 generate_sample.py
```
This will create a `sample.bmp` file in the root directory.

### Running Individual Component Tests

You can run individual scripts to test and see each component of the JPEG encoding pipeline in action:

#### Color Conversion (RGB <-> YUV)
```bash
python3 test_conversions.py
```

#### Discrete Cosine Transform (DCT <-> IDCT)
```bash
python3 test_dct.py
```

#### ZigZag Scanning
```bash
python3 test_zigzag.py
```

#### Entropy Coding (RLE & Huffman)
```bash
python3 test_entropy.py
```

## Project Structure

- `jpeg_encoder/`: Core encoding logic.
  - `conversions.py`: RGB/YUV conversion.
  - `dct.py`: 2D DCT and IDCT implementation.
  - `quantization.py`: Quantization and dequantization.
  - `zigzag.py`: ZigZag and inverse ZigZag scanning.
  - `entropy_coding.py`: RLE and Huffman coding.
  - `encoder.py`: Orchestrates the full encoding/decoding pipeline.
- `app.py`: Flask web application.
- `generate_sample.py`: Utility to create a test BMP image.
- `test_conversions.py`, `test_dct.py`, `test_zigzag.py`, `test_entropy.py`: Scripts to test and demonstrate individual encoding steps.
- `templates/` & `static/`: Frontend assets for the web interface.
