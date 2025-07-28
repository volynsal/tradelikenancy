import csv
import zipfile
import requests
import os
import sys

import fitz  # PyMuPDF
import io
import requests

from parsing import parsing

## Drill down
year = input("Enter year: ")
last_name = input("Enter Representative last name: ")

zip_file_url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/' + year + 'FD.ZIP'
pdf_file_url = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/' + year + '/'
r = requests.get(zip_file_url)
zipfile_name = year + '.zip'

with open(zipfile_name, 'wb') as f:
    f.write(r.content)

with zipfile.ZipFile(zipfile_name) as z:
    z.extractall('./')

dates = []
doc_ids = []

def is_ptr_doc(doc_id, year):
    url = f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf"
    r = requests.get(url)
    if r.status_code != 200:
        return False
    try:
        pdf_stream = io.BytesIO(r.content)
        doc = fitz.open("pdf", pdf_stream)
        for page in doc:
            if "PERIODIC TRANSACTION REPORT" in page.get_text().upper():
                return True
        return False
    except Exception as e:
        print(f"Error parsing PDF {doc_id}: {e}")
        return False

with open(year + 'FD.txt') as f:
    for line in csv.reader(f, delimiter='\t'):
        if line[1] == last_name:
            doc_id = line[8]

            if is_ptr_doc(doc_id, year):
                dates.append(line[7])
                doc_ids.append(line[8])             

doc_id_url = ""

current_dir = os.getcwd()

zip_file_path = os.path.join(current_dir, year+ ".zip")
txt_file_path = os.path.join(current_dir, year+ "FD.txt")
xml_file_path = os.path.join(current_dir, year+ "FD.xml")
os.remove(zip_file_path)
os.remove(txt_file_path)
os.remove(xml_file_path)

if len(dates) > 1:
    print("We found multiple dates for this representative: ")
    for i,value in enumerate(dates):
        print(str(i+1) + ". " + value)
    index = input("Please enter the number in front of the date indicating which date you prefer: ")
    date = dates[int(index)-1]
    doc_id_url = pdf_file_url + doc_ids[int(index)-1] + '.pdf'
    print("Generating the financial transactions for you now.")
elif len(dates) == 1:
    print("We only found one date for this Representative: " + dates[0] + ". Generating the financial transactions for you now.")
    doc_id_url = pdf_file_url + doc_ids[0] + '.pdf'
elif len(dates) == 0:
    print("No Representative with that last name found or no Periodic Transaction Reports for that year. Please run the script and try again.")
    sys.exit()

r = requests.get(doc_id_url)

if (r.status_code == 200):
    pdf_data = requests.get(doc_id_url).content

    pdf_stream = io.BytesIO(pdf_data)
    doc = fitz.open("pdf", pdf_stream)

    owners, company_names, transaction_types, dates, notification_dates, amounts = parsing(doc)

    for index, company_name in enumerate(company_names):
        print('---------------------------')
        print('Owner: ' + owners[index])
        print('Company Name: ' + company_names[index])
        print('Transaction Type: ' + transaction_types[index])
        print('Date: ' + dates[index])
        print('Notification Date: ' + notification_dates[index])
        print('Amount: ' + amounts[index])
else:
    print("Unfortunately this filing is not available and returns a status code of 404. Please run the script and pick a different date.")
