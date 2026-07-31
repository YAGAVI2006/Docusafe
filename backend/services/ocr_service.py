import pytesseract
from PIL import Image
import re
import datetime

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Configure as needed

def extract_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

def find_expiry_date(text):
    # Regex for YYYY-MM-DD, DD/MM/YYYY, etc.
    date_patterns = [
        r'\b(20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12][0-9]|3[01])\b',
        r'\b(0[1-9]|[12][0-9]|3[01])[-/](0[1-9]|1[0-2])[-/](20\d{2})\b'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            # Simple extraction for now
            date_str = match.group(0)
            try:
                if '-' in date_str and len(date_str.split('-')[0]) == 4:
                    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                if '/' in date_str and len(date_str.split('/')[2]) == 4:
                    return datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
            except ValueError:
                pass
    return None
