import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def compress_pdf(input_pdf_path, output_pdf_path):
    pdf = PdfFileReader(input_pdf_path)
    pdf_writer = PdfFileWriter()

    for page_num in range(pdf.getNumPages()):
        page = pdf.getPage(page_num)
        page.compressContentStreams()
        pdf_writer.addPage(page)

    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

def compress_txt(input_txt_path, output_txt_path):
    with open(input_txt_path, 'r') as input_file:
        content = input_file.read()
        compressed_content = ' '.join(content.split())

    with open(output_txt_path, 'w') as output_file:
        output_file.write(compressed_content)

# Example usage for compressing a PDF
input_pdf_path = 'input.pdf'
output_pdf_path = 'output_compressed.pdf'
compress_pdf(input_pdf_path, output_pdf_path)

# Example usage for compressing a text (TXT) file
input_txt_path = 'input.txt'
output_txt_path = 'output_compressed.txt'
compress_txt(input_txt_path, output_txt_path)
