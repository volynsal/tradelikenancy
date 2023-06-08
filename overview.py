import csv
import zipfile
import requests
import openai
import PyPDF2
import textwrap
import time
import os
import ast
import re

import fitz  # PyMuPDF
import io
import requests

from parsing import parsing

## Drill down
year = input("Enter year: ")

zip_file_url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/' + year + 'FD.ZIP'
pdf_file_url = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/' + year + '/'
r = requests.get(zip_file_url)
zipfile_name = year + '.zip'

with open(zipfile_name, 'wb') as f:
    f.write(r.content)

with zipfile.ZipFile(zipfile_name) as z:
    z.extractall('./')

doc_ids = []

with open(year + 'FD.txt') as f:
    for line in csv.reader(f, delimiter='\t'):
        if line[8] != 'DocID':
            doc_ids.append(line[8])

for i in range(len(doc_ids)):
    doc_ids[i] = pdf_file_url + str(doc_ids[i]) + '.pdf'

current_dir = os.getcwd()

zip_file_path = os.path.join(current_dir, year+ ".zip")
txt_file_path = os.path.join(current_dir, year+ "FD.txt")
xml_file_path = os.path.join(current_dir, year+ "FD.xml")
os.remove(zip_file_path)
os.remove(txt_file_path)
os.remove(xml_file_path)

doc_id_urls = doc_ids
del doc_ids

company_names_counter = {}

for doc_id_url in doc_id_urls:
    doc_id = doc_id_url[-12:-5]
    r = requests.get(doc_id_url)

    if (r.status_code == 200):
        pdf_data = requests.get(doc_id_url).content

        pdf_stream = io.BytesIO(pdf_data)
        doc = fitz.open("pdf", pdf_stream)

        company_names, transaction_types = parsing(doc)
        print(company_names, transaction_types)

        
