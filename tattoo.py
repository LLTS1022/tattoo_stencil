import cv2
import numpy as np
from tkinter import Tk, filedialog
from PIL import Image
from flask import Flask
app = Flask(__name__)


# Step 1: Select image file
Tk().withdraw()
file_path = filedialog.askopenfilename()
if not file_path:
    print("No file selected.")
    exit()

# Step 2: Load image and convert to grayscale
image = cv2.imread(file_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 3: Invert the grayscale image
inverted = cv2.bitwise_not(gray)

# Step 4: Apply Gaussian blur
blurred = cv2.GaussianBlur(inverted, (21, 21), 0)

# Step 5: Dodge blend (Color Dodge effect)
def dodge(front, back):
    result = cv2.divide(front, 255 - back, scale=256)
    return np.clip(result, 0, 255)

stencil = dodge(gray, blurred)

# Step 6: Save and display result
output_path = file_path.rsplit('.', 1)[0] + '_stencil.png'
cv2.imwrite(output_path, stencil)

cv2.imshow("Original", image)
cv2.imshow("Stencil Effect", stencil)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"Stencil image saved to: {output_path}")
