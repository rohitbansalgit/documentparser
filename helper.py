import os
import docx2txt
import textract
import re
import PyPDF2
import pytesseract
from PIL import Image


def extract_text_from_docx(path):
    temp = docx2txt.process(path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    final_text = ' '.join(text)
    return final_text


def extract_text_from_doc(filename):
    text = textract.process(filename)
    text = text.decode("utf-8")
    # print(text)
    return text


def get_data_from_text(file):
    # get file extension
    data = ''
    # print('here')
    extension = os.path.splitext(file)[-1]
    if extension.lower() == '.docx':
        data = extract_text_from_docx(file)
    elif extension.lower() == '.doc':
        data = extract_text_from_doc(file)
    elif extension.lower() == '.pdf':
        data = extract_text_from_pdf(file)
    elif extension.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
        data = extract_text_from_image(file)

    new_data = get_words_char_repeat(data)
    # print(new_data)
    return new_data


def get_words_char_repeat(text):
    words = text.strip()
    words = re.split(r'[ \n]+', words)
    # print(words)
    word_count = len(words)
    char_count = len(text.replace(' ', '').replace('\n', ''))

    char_frequency = {}
    word_frequency = {}
    data = {}

    trimmed_text = text.strip()
    list_text = re.split(r'[ \n]+', trimmed_text)
    # Count character frequencies
    clean_char = ''
    for char in list_text:
        char = char.strip()
        # create string of characters
        clean_char += char
    # print(clean_char)
    for char in clean_char:
        if char in char_frequency:
            char_frequency[char] += 1
        else:
            char_frequency[char] = 1

    # Count word frequencies
    for word in list_text:
        word = word.strip()
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1

    data['char_frequency'] = char_frequency
    data['word_frequency'] = word_frequency
    data['word_count'] = word_count
    data['char_count'] = char_count
    # print(data)
    return data


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    print(pdf_path)
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)

        # Initialize an empty string to store the extracted text
        raw_data = []

        # Iterate through each page of the PDF
        for page_num in range(len(reader.pages)):
            # Extract text from each page
            page = reader.pages[page_num]
            text = page.extract_text()
            raw_data.append(text)
    text = ' '.join(raw_data)
    return text


# Function to extract text from image
def extract_text_from_image(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)
        print(text)
        return text
    except Exception as e:
        return f"Error reading image: {str(e)}"
