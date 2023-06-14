import csv
import zipfile
import requests
import os

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

with open(year + 'FD.txt') as f:
    for line in csv.reader(f, delimiter='\t'):
        if line[1] == last_name:
            date = line[7]
            doc_id = line[8]

            dates.append(line[7])
            doc_ids.append(line[8]) 

doc_id_url = ""

if len(date) > 1:
    print("We found multiple dates for this representative: ")
    for i,value in enumerate(dates):
        print(str(i+1) + ". " + value)
    index = input("Please enter the number in front of the date indicating which date you prefer: ")
    date = dates[int(index)-1]
    doc_id_url = pdf_file_url + doc_ids[int(index)-1] + '.pdf'
    print("Generating the financial transactions for you now.")
elif len(date) == 1:
    print("We only found one date for this Representative: " + date + ". Generating the financial transactions for you now.")
    doc_id_url = pdf_file_url + doc_ids[0] + '.pdf'
elif len(date) == 0:
    print("No Representative with that last name found. Please run the script and try again.")

current_dir = os.getcwd()

zip_file_path = os.path.join(current_dir, year+ ".zip")
txt_file_path = os.path.join(current_dir, year+ "FD.txt")
xml_file_path = os.path.join(current_dir, year+ "FD.xml")
os.remove(zip_file_path)
os.remove(txt_file_path)
os.remove(xml_file_path)

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



