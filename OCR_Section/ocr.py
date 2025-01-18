from PIL import Image

import os
import pytesseract

script_dir = os.path.dirname(__file__)
rel_path = "src/Resume.jpg"
text = pytesseract.image_to_string(Image.open(os.path.join(script_dir, rel_path)))

for line in text.split("\n"):
    print(line)

