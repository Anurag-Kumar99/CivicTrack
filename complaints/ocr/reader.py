import pytesseract
from PIL import Image
import re 

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    print("🔍 RAW OCR OUTPUT >>>", repr(text))
    return text

def  clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text
