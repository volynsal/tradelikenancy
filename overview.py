import csv
import zipfile
import requests
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

counter_sales = {}
counter_purchases = {}
top_five_keys_sales = []
top_five_key_purchases = []
counter = 0

for doc_id_url in doc_id_urls:
    doc_id = doc_id_url[-12:-5]
    r = requests.get(doc_id_url)

    if (r.status_code == 200):
        pdf_data = requests.get(doc_id_url).content

        pdf_stream = io.BytesIO(pdf_data)
        doc = fitz.open("pdf", pdf_stream)

        _, company_names, transaction_types, _, _, _ = parsing(doc)
        
        for index, company_name in enumerate(company_names):
            counter += 1
            company_names[index] = company_names[index].strip()

        for index, company_name in enumerate(company_names):
            if (transaction_types[index] == 'E' or transaction_types[index] == 'G'):
                continue
            elif (transaction_types[index] == 'S' or transaction_types[index] == 'S (partial)'):
                if (company_name in counter_sales):
                    counter_sales[company_name] += 1
                else:
                    counter_sales[company_name] = 1
            elif (transaction_types[index] == 'P' or transaction_types[index] == 'P (partial)'):
                if (company_name in counter_purchases):
                    counter_purchases[company_name] += 1
                else:
                    counter_purchases[company_name] = 1



top_five_keys_sales = sorted(counter_sales, key=counter_sales.get, reverse=True)[:5]
top_five_key_purchases = sorted(counter_purchases, key=counter_purchases.get, reverse=True)[:5]

print("Top 5 purchases for " + year + ":\n")
print(top_five_key_purchases)
print("Top 5 sales for " + year + ":\n")
print(top_five_keys_sales)

        
