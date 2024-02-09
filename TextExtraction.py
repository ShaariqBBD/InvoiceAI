import streamlit as st
from paddleocr import PaddleOCR
import fitz
import io
from PIL import Image
from PyPDF2 import PdfReader
import numpy as np


def isPDF(file):
    return file.name.endswith('.pdf')

def isImage(file): 
    try:
        Image.open(file)
        return True
    except Exception as e:
        return False
    
def pdfToImage(file):
    mat = fitz.Matrix(2, 2)
    images = []
    with fitz.open(file) as doc:
        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
    return images

def extractTextFromPDF(file):
    reader = PdfReader(file)
    ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)
    text = ""
    for page_num, page in enumerate(reader.pages):
        textract = page.extract_text()
        if textract:
            print("This has selectable text")
            text += textract
        else:
            with st.spinner("No selectable text found, using OCR instead."):
                print("This does not have selectable text, using OCR instead.")
                st.balloons()
                images = pdfToImage(file)
                if page_num < len(images):
                    for image in images:
                        image = images[0]
                        with io.BytesIO() as output:
                            image.save(output, format="PNG")
                            data = output.getvalue()
                        result = ocr.ocr(data, cls=True)
                        for page_result in result:
                            for line in page_result:
                                text += line[1][0]
    return text

def extractTextFromImage(file):
    image = Image.open(file)
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        data = output.getvalue()
    ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)
    result = ocr.ocr(data, cls=True)
    ret_text = ""
    for page in result:
        for line in page:
            ret_text += line[1][0]
    return ret_text, image