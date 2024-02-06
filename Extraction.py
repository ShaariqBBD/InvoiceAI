# Prerequisites:
# Install tesseract on machine (I used an installer for Windows from 'https://github.com/UB-Mannheim/tesseract/wiki')
# pip install opencv-python
# pip install pytesseract
# pip install fitz
# pip install PyMuPDF

import cv2
import pytesseract
from pytesseract import Output
import fitz
import os

# Pytesseract needs to point to the locally installed tesseract file
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\bbdnet3167\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


class TextExtraction:

    @staticmethod
    def image_to_dict(input_image_path):
        # Read the image file into opencv
        img = cv2.imread(input_image_path)

        # Convert the image to data stored in a dict
        d = pytesseract.image_to_data(img, output_type=Output.DICT)

        return d

    @staticmethod
    def image_to_text(input_image_path, output_text_path):
        # Convert image to text
        text = pytesseract.image_to_string(input_image_path)

        # Save the text to a text file
        with open(output_text_path, "w", encoding="utf-8") as f:
            f.write(text)

    # Can handle PDF files with multiple pages
    @staticmethod
    def pdf_to_text(input_pdf_path, output_text_path):
        doc = fitz.open(input_pdf_path)
        zoom = 4
        mat = fitz.Matrix(zoom, zoom)

        count = 0

        # Here we get the number of pages in the PDF file
        for p in doc:
            count += 1

        text = ""
        temp_image_path = "temp.jpg"

        for i in range(count):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=mat)
            pix.save(temp_image_path)
            text += pytesseract.image_to_string(temp_image_path) + "\n"
            os.remove(temp_image_path)

        with open(output_text_path, "w", encoding="utf-8") as f:
            f.write(text)

    @staticmethod
    def streamlit_text_generator(input_pdf_path):
        doc = fitz.open(input_pdf_path)
        zoom = 4
        mat = fitz.Matrix(zoom, zoom)

        count = 0

        # Here we get the number of pages in the PDF file
        for p in doc:
            count += 1

        text = ""
        temp_image_path = "temp.jpg"

        for i in range(count):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=mat)
            pix.save(temp_image_path)
            text += pytesseract.image_to_string(temp_image_path) + "\n"
            os.remove(temp_image_path)

            # Save the text to a text file
        return text


