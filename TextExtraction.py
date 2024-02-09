import streamlit as st
from paddleocr import PaddleOCR
import fitz
import io
from PIL import Image
from PyPDF2 import PdfReader


def isPDF(file):
    if file == "application/pdf":
        return True
    else:
        return False
    
def isPNG(file):
    if file == "image/png":
        return True
    else:
        return False
    
def isJPG(file):
    if file == "image/jpeg":
        return True
    else:
        return False

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
    parts = pdfToImage(file)
    index = 0
    for part in parts:
        textract= reader.pages[index].extract_text()
        if textract != "":
            ret_text = textract
        elif textract == "":
            result = ocr.ocr(part, cls=True)
            for page in result:
                for line in page:
                    ret_text += line[1][0]
        index += 1
    return ret_text

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
    return ret_text