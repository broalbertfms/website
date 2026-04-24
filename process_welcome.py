from PIL import Image
import numpy as np

img_path = r'C:\Users\BERT-FMS\Desktop\2026-04-17 19_10_24-NVIDIA GeForce Overlay.png'
out_path = r'C:\Users\BERT-FMS\Desktop\VB PROJECTS\MaristEastAsia\assets\images\welcome-brush.png'

try:
    img = Image.open(img_path).convert('RGBA')
    data = np.array(img)
    
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    new_a = 255 - luminance
    new_a = np.clip(new_a * 1.5, 0, 255).astype(np.uint8)
    
    data[:, :, 0] = 196
    data[:, :, 1] = 30
    data[:, :, 2] = 58
    data[:, :, 3] = new_a
    
    new_img = Image.fromarray(data, 'RGBA')
    new_img.save(out_path)
    print(f"Successfully processed and saved to {out_path}")
except Exception as e:
    print(f"Error: {e}")
