import streamlit as st
import os
import json
import urllib.request
import ssl
from Extraction import TextExtraction
import tempfile

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)


st.title("Invoice AI 💰")

uploaded_invoice = st.file_uploader("Choose your .pdf file", type="pdf")

if uploaded_invoice is not None:
    filename = uploaded_invoice.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_filename = temp_file.name

        with open(temp_filename, 'wb') as f:
            f.write(uploaded_invoice.read())

        invoice_text = TextExtraction.streamlit_text_generator(temp_filename)
        st.success("PDF file uploaded and processed successfully")
        st.write(invoice_text)
        data = invoice_text

        body = str.encode(json.dumps(data))

        url = 'https://discobank-llama2-invoice-poc.eastus2.inference.ml.azure.com/score'
        api_key = '2bwtTLswXxoWg5ry5x8BrtspldlBqx6j'
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")
        
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'llama2-7b-invoice-test' }

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            print(result)

            st.write("result goes here")
            st.write(result)

        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            print(error.info())
            print(error.read().decode("utf8", 'ignore'))

        st.header("Payment Details")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write("Bank:")
            st.write("Discovery Bank")
        
        with col2:
            st.write("Account Number:")
            st.write("6831908727")

        with col3:
            st.write("Amount Due:")
            st.write("R2 000 000.00")

        with col4:
            st.write("Reference:")
            st.write("Invoice02")
        
        confirmed = st.checkbox("Confirm the payment details are correct")

        if confirmed:
            st.success("Payment confirmed!")
        else:
            st.warning("Please review the details carefully before confirming.")



















