import streamlit as st
from Extraction import TextExtraction
import tempfile

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



















