import streamlit as st
from paddleocr import PaddleOCR
import fitz
import io
from PIL import Image
from PyPDF2 import PdfReader
import numpy as np

def pdfHasImages(file):
    print("PDF has Images run")
    doc = fitz.open(file)
    for pageNum in range(len(doc)):
        page = doc.load_page(pageNum)
        images = page.get_images(full=True)
        if images:
            print("Has images.")
            return True
    print("Has no images.")
    return False

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
    pdfFile = fitz.open(file)
    reader = PdfReader(file)
    ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)
    text = ""
    for page_num, page in enumerate(reader.pages):
        textract = page.extract_text()

        # CASE 1: If the page has ONLY selectable text
        if textract and pdfHasImages(file) == False:
            print("This has selectable text")
            text += textract

        # CASE 2: If the page has embedded images
        elif textract and pdfHasImages(file) == True:
            # get the page itself
            page = pdfFile[page_num]
            image_list = page.get_images()
            # printing number of images found in this page
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images in page {page_num}")
            else:
                print("[!] No images found on page", page_num)
            for image_index, img in enumerate(page.get_images(), start=1):
                # get the XREF of the image
                xref = img[0]
                # extract the image bytes
                base_image = pdfFile.extract_image(xref)
                image_bytes = base_image["image"]
                # get the image extension
                image_ext = base_image["ext"]
                # load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                # perform OCR
                result = ocr.ocr(image_bytes, cls=True)
                if result!=[None]:
                    print("Result::::", result)
                    for page_result in result:
                        for line in page_result:
                            text += line[1][0]
            # append the selectable text
            text+=textract

        # CASE 3: If the page has NO selectable text
        else:
            with st.spinner("No selectable text found, using OCR instead."):
                print("This does not have selectable text, using OCR instead.")
                st.balloons()
                images = pdfToImage(file)
                if page_num < len(images):
                    image = images[page_num]
                    with io.BytesIO() as output:
                        image.save(output, format="PNG")
                        data = output.getvalue()
                    result = ocr.ocr(data, cls=True)
                    print("Result", result)
                    if result!=[None]:
                        print("Result::::", result)
                        for page_result in result:
                            for line in page_result:
                                text += line[1][0]
                    else:
                        print("No text found in image at index", page_num)

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
    return ret_text