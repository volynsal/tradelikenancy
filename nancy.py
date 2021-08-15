import csv, json, zipfile
import os, requests, fitz

zip_file_url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP'
pdf_file_url = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2021/'
r = requests.get(zip_file_url)
zipfile_name = '2021.zip'

# with open(zipfile_name, 'wb') as f:
#     f.write(r.content)

# with zipfile.ZipFile(zipfile_name) as z:
#     z.extractall('./')

# with open('2021FD.txt') as f:
#     for line in csv.reader(f, delimiter='\t'):
#         if line[1] == 'Pelosi':
#             print(line)
#             doc_id = line[8]

#             r = requests.get(pdf_file_url + (doc_id + '') + '.pdf')
#             print(r)

#             with open(doc_id + '.pdf', 'wb') as pdf_file:
#                 pdf_file.write(r.content)

for filename in os.listdir('./'):
    if filename.endswith('.pdf'):
        doc = fitz.open(filename)
        page = doc.load_page(page_id=0)
        print(page.get_text())
        print('------------------------------------------------------------')

