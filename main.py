import streamlit as st
import os
import json
import requests
import ssl
import urllib.request
import FileHandler as fh
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

    if fh.isPDF(file_type):
        st.write("PDF uploaded successfully!")
        suffix = ".pdf"
    elif fh.isJPG(file_type):
        st.write("Image uploaded successfully!")
        suffix = ".jpg"
    elif fh.isPNG(file_type):
        st.write("Image uploaded successfully!")
        suffix = ".png"
    else:
        st.write("Unsuccessful upload!")
        
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_filename = temp_file.name
        with open(temp_filename, 'wb') as f:
            f.write(uploaded_file.read())

        url = "https://invoiceocr-flask.azurewebsites.net/"

        with open(temp_filename, 'rb') as file:
            files = {'invoice': file}
            response = requests.post(url, files=files)

        response_data = json.loads(response.text)
        extracted_text = response_data.get('extracted_text', '')

        # st.header("Response from OCR")
        # st.write(extracted_text)

        data = extracted_text

        body = str.encode(json.dumps(data))

        url = 'https://discobank-mistral-invoice-poc.eastus2.inference.ml.azure.com/score'
        #api_key = st.secrets["AZURE_ENDPOINT_KEY"]
        api_key = "ROTSNgmPMVq3DElWqpN3L1dg3r3J0ab6"
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")
        
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'mistral-7b-invoice-test' }

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            result = result.decode('utf-8')
            result = json.loads(result)

            # st.header("Response from LLM")
            # st.write(result)

        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            print(error.info())
            print(error.read().decode("utf8", 'ignore'))

        st.header("Payment Details")

        account_holder = ""
        bank_name = ""
        account_number = ""
        account_type = ""
        amount_due = ""
        currency = ""
        reference = ""

        try:
            account_holder = result.get("Account Holder")
        except:
            account_holder = "null"
        try:
            bank_name = result.get("Bank Name")
        except:
            bank_name = "null"
        try:
            account_number = result.get("Account Number")
        except:
            account_number = "null"
        try:
            account_type = result.get("Account Type")
        except:
            account_type = "null"
        try:
            amount_due = result.get("Amount Due")
        except:
            amount_due = "null"
        try:
            currency = result.get("Currency")
        except:
            currency = "null"
        try:
            reference = result.get("Reference")
        except:
            reference = "null"
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write("**Account Holder:**")
            st.write(account_holder)
        
        with col2:
            st.write("**Account Type:**")
            st.write(account_type)

        with col3:
            st.write("**Bank Name:**")
            st.write(bank_name)

        with col4:
            st.write("**Account Number:**")
            st.write(account_number)

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.write("**Amount Due:**")
            st.write(amount_due)

        with col6:
            st.write("**Currency:**")
            st.write(currency)

        with col7:
            st.write("**Reference:**")
            st.write(reference)

        with col8:
            st.write("\n")
        



















