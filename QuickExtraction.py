# A python file to extract text from PDF/Images for use when testing the model

import TextExtraction as te

input_file_path = "./InvoicesDataset/NonSelectablePDFs/InvoiceTest_10.pdf"

output_text = te.extractTextFromPDF(input_file_path)

print(f"""
=========================================================
This is the output text:
      
{output_text}

=========================================================

""")