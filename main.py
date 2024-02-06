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



















