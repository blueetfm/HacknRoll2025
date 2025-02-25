from PIL import Image
import urllib.request
import os
import pytesseract
import re
from paddleocr import PaddleOCR

# script_dir = os.path.dirname(__file__)
# rel_path = "src/Resume.jpg"
# urllib.request.urlretrieve("https://tdbzbuocqslnmyfvxokj.supabase.co/storage/v1/object/public/images/Resume.jpg","image")
# text = pytesseract.image_to_string(Image.open("image"))

# split_text = text.split("\n")
# print(split_text)
# length = len(split_text)

# clean_text = []
# temp = []

# for i in range(length):
#     if len(split_text[i]) > 0:
#         temp.append(split_text[i])
#     else:
#         joined_string = ' '.join(temp)
#         clean_text.append(joined_string)


def read_resume(url):
    urllib.request.urlretrieve(url,"image")
    # text = pytesseract.image_to_string(Image.open("image"))
    # split_text = text.split("\n")
    # parsed_info = extract_relevant_info(split_text)
    # return parsed_info
    reader = PaddleOCR(
    use_angle_cls=False, 
    lang='en',
    use_gpu=False,         # Ensure it runs on CPU
    cpu_threads=2,         # Limit threads for efficiency
    det_db_box_thresh=0.7, # Adjust detection threshold
    rec_batch_num=2        # Reduce batch size
    )  # Specify the language(s) as needed

    # Step 3: Read text from the image
    results = reader.ocr("image")
    # Step 4: Extract text into lines
    txts = [line[1][0] for group in results for line in group]
    extracted_text = "\n".join(txts)
    split_text = extracted_text.split("\n")
    # Step 5: Parse the text lines
    parsed_info = extract_relevant_info(split_text)
    return parsed_info

def extract_relevant_info(resume_elements):
    # Cleaned up relevant info dictionary
    relevant_info = {
        "name": None,
        "email": None,
        "location": None,
        "job_titles": [],
        "education": [],
    }

    # Regex patterns for specific fields
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    job_title_keywords = ['engineer', 'developer', 'manager', 'associate', 'intern', 'analyst','business',]
    education_keywords = ['university', 'college', 'school']

    for element in resume_elements:
        # Strip whitespace and normalize the text
        element = element.strip()

        # Skip empty elements
        if not element:
            continue

        # Extract name (assume name is in uppercase and appears at the beginning)
        if relevant_info["name"] is None and re.match(r'^[A-Z][A-Z ]+\|?', element):
            relevant_info["name"] = element.split('|')[0].strip().title()

        # Extract email
        if relevant_info["email"] is None:
            email_match = re.search(email_pattern, element)
            if email_match:
                relevant_info["email"] = email_match.group(0)

        # Extract job titles
        if any(keyword in element.lower() for keyword in job_title_keywords):
            # Check if the element contains 4 or fewer words
            if len(element.split()) <= 4 and not any(char.isdigit() for char in element):
                relevant_info["job_titles"].append(element.title())

        # Extract education
        if any(keyword in element.lower() for keyword in education_keywords):
        # Preprocess to remove dates or reduce word count
            match = re.split(r'_*Singapore', element, maxsplit=1)
            if match:  # Check if there's a match
                title = match[0].strip().title()
            if len(title.split()) <= 5:  # Check word count
                relevant_info["education"].append(title)

    # Filter out empty values
    relevant_info = {key: value for key, value in relevant_info.items() if value}
    return relevant_info

# print(read_resume("https://tdbzbuocqslnmyfvxokj.supabase.co/storage/v1/object/public/images/Resume.jpg"))






