import csv
import zipfile
import requests
import openai
import PyPDF2
import textwrap
import time
import os

key = input("Enter your OpenAI key")

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

date, doc_id

if len(date) > 1:
    print("We found multiple dates for this representative: ")
    for i,value in enumerate(dates):
        print(str(i+1) + ". " + value)
        date = dates[i-1]
        doc_id = doc_ids[i-1]
    index = input("Please enter the number in front of the date indicating which date you prefer: ")
    print("Generating the financial transactions for you now.")
elif len(date) == 1:
    print("We only found one date for this Representative: " + date + ". Generating the financial transactions for you now.")
elif len(date) == 0:
    print("No Representative with that last name found. Please run the script and try again.")

r = requests.get(pdf_file_url + str(doc_id) + '.pdf')

if (r.status_code != 404):
    with open(doc_id + '.pdf', 'wb') as pdf_file:
        if (r.status_code != 404):
            pdf_file.write(r.content)  

else:
    print("Unfortunately this filing is not available and returns a status code of 404. Please run the script and pick a different date.")


# Open the PDF file in read-binary mode
with open('./' + doc_id + '.pdf', 'rb') as file:
    # Create a PDF file reader object
    reader = PyPDF2.PdfReader(file)

    # Initialize an empty string to hold the PDF content
    pdf_content = ''

    # Read each page and add its text to the string
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        pdf_content += page.extract_text()

# Break the content into chunks of 2048 characters each
chunks = textwrap.wrap(pdf_content, 2048)


for chunk in chunks:
    
# The provided text
    prompt = "These are this House of Representative's transactions for the year. There is a table with the transactions. Please return the Asset, Description, Date, and Amount for each transaction in a table with those columns. Limit your output to this information only!\n"

    # Define the message to send to the ChatGPT API
    message = prompt + chunk

    while True:
        try:
            # Call the ChatGPT API for information extraction
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=message,
                max_tokens=3000,
                n=1,
                stop=None,
                temperature=0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )

            # Extract the extracted information from the response
            output = response.choices[0].text.strip()

            # Print the extracted information
            print("----------------------------------------------")
            print(output)
            break  # Break the loop if successful
            

        except openai.error.RateLimitError as e:
            # Handle rate limit error
            print("----------------------------------------------")
            print("Rate limit exceeded. Retrying in 60 seconds...")
            time.sleep(60)

print("----------------------------------------------")
print("Deleting locally generated files")

import os

# List of files to keep
files_to_keep = ['nancy.py', 'README.md', 'requirements.txt', '.git']

# Get the current directory
current_dir = os.getcwd()

# Get a list of all files in the directory
files_in_directory = os.listdir(current_dir)

# Loop through the files in the directory
for file_name in files_in_directory:
    # Check if the file is not in the list of files to keep
    if file_name not in files_to_keep:
        # Construct the absolute path to the file
        file_path = os.path.join(current_dir, file_name)
        
        # Delete the file
        os.remove(file_path)
        print(f"Deleted {file_path}")

print("Files deletion completed.")
