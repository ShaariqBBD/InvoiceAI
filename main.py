import streamlit as st
import os
import json
import urllib.request
import ssl
import TextExtraction as te
import tempfile

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)


st.title("Invoice AI 💰")

uploaded_file = st.file_uploader("Choose your file", type=["pdf", "jpeg", "jpg", "png"])

if uploaded_file is not None:

    filename = uploaded_file.name
    file_type = uploaded_file.type
    suffix = ""
    isImage = False

    if te.isPDF(file_type):
        st.write("PDF uploaded successfully!")
        suffix = ".pdf"
    elif te.isJPG(file_type):
        st.write("Image uploaded successfully!")
        suffix = ".jpg"
    elif te.isPNG(file_type):
        st.write("Image uploaded successfully!")
        suffix = ".png"
    else:
        st.write("Unsuccessful upload!")
        
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_filename = temp_file.name
        with open(temp_filename, 'wb') as f:
            f.write(uploaded_file.read())

        if te.isPDF(file_type):
            text = te.extractTextFromPDF(temp_filename)
            st.header("Extracted text:")
            st.write(text)
        elif te.isJPG(file_type) or te.isPNG(file_type): 
            text = te.extractTextFromImage(temp_filename)
            st.header("Extracted text:")
            st.write(text)

        data = text

        body = str.encode(json.dumps(data))

        url = 'https://discobank-llama2-invoice-poc.eastus2.inference.ml.azure.com/score'
        api_key = st.secrets["AZURE_ENDPOINT_KEY"]
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")
        
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'llama2-7b-invoice-test' }

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            result = json.loads(result)

        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            print(error.info())
            print(error.read().decode("utf8", 'ignore'))

        st.header("Payment Details")

        bank = ""
        total_amount = ""
        account_number = ""
        reference = ""

        try:
            bank = result["invoice"].get("bank")
        except:
            bank = "None"
        try:
            total_amount = result["invoice"].get("total_amount")
        except:
            total_amount = "None"
        try:
            account_number = result["invoice"].get("account_number")
        except:
            account_number = "None"
        try:
            reference = result["invoice"].get("reference")
        except:
            reference = "None"
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write("Bank:")
            st.write(bank)
        
        with col2:
            st.write("Account Number:")
            st.write(account_number)

        with col3:
            st.write("Amount Due:")
            st.write(total_amount)

        with col4:
            st.write("Reference:")
            st.write(reference)
        
        confirmed = st.checkbox("Confirm the payment details are correct")

        if confirmed:
            st.success("Payment confirmed!")
        else:
            st.warning("Please review the details carefully before confirming.")



















