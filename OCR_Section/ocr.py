from PIL import Image

import os
import pytesseract

script_dir = os.path.dirname(__file__)
rel_path = "src/Resume.jpg"
text = pytesseract.image_to_string(Image.open(os.path.join(script_dir, rel_path)))

split_text = text.split("\n")
length = len(split_text)

clean_text = []
temp = []

for i in range(length):
    if len(split_text[i]) > 0:
        temp.append(split_text[i])
    else:
        joined_string = ' '.join(temp)
        clean_text.append(joined_string)
        temp.clear()







