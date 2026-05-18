import numpy as np
from PIL import Image

def generate_sample_bmp():
    # Create a 128x128 color gradient image
    img = np.zeros((128, 128, 3), dtype=np.uint8)
    for i in range(128):
        for j in range(128):
            img[i, j, 0] = i * 2 # Red gradient
            img[i, j, 1] = j * 2 # Green gradient
            img[i, j, 2] = (i + j) # Blue gradient

    # Add some patterns
    img[30:60, 30:60, :] = [255, 255, 255] # White square
    img[70:100, 70:100, :] = [255, 0, 0] # Red square

    pil_img = Image.fromarray(img)
    pil_img.save('sample.bmp')
    print("Sample BMP image generated: sample.bmp")

if __name__ == "__main__":
    generate_sample_bmp()
