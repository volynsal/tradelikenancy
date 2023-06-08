import fitz  # PyMuPDF
import io
import requests

# pdf_path = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2021/20018244.pdf"
# pdf_data = requests.get(pdf_path).content
 
# pdf_stream = io.BytesIO(pdf_data)
# doc = fitz.open("pdf", pdf_stream)

def parsing(doc):
    owner = []
    company_name = []
    transaction_type = []
    date = []
    notification_date = []
    amount = []

    filing_status = "FILING STATUS:"
    subholding_of = "SUBHOLDING OF:"
    description = "DESCRIPTION:"

    for pag_ind, page in enumerate(doc):
        text = page.get_text()

        split_text = text.split('\n')

        # Changed while loop to be greater than 0 instead of equal, helps to process first row on every page after first
        prev_index = -1
        prev_amount = ''

        for index, line in enumerate(split_text):
            # Empty line
            if (len(line) == 0):
                continue

            # First transaction (end of the header of the document)
            elif (line[0] == '$' and line[-1] == '?'):
                prev_index = index
                continue

            # Amount is on 2 lines
            elif (line[0] == "$" and line.count('$') == 1 and line.count(',') > 0):
                if (prev_amount == ''):
                    prev_amount = line
                    continue
                else:
                    line = prev_amount + " " + line
                    index -= 1
                    prev_amount = ''
        
            # Index to start processing for company name
            new_index = 0

            if (line[0] == ('$') and line.count('$') == 2 and line.count(',') > 0):
                amount.append(line)
                if split_text[index-1].count('/') == 4:
                    dates = split_text[index-1].split(' ')
                    date.append(dates[0])
                    notification_date.append(dates[1])
                    
                    temp_type = split_text[index - 2]
                                        
                    new_index = index - 3
                else:
                    date.append(split_text[index-2])
                    notification_date.append(split_text[index-1])
                    
                    temp_type = split_text[index - 3]
                    
                    new_index = index - 4
                
                temp_types = temp_type.split(' ')

                # S or P or E or G
                if (len(temp_types) == 1):
                    transaction_type.append(temp_types[0])
                    temp_owner = ""

                # S (partial) or P (partial)
                elif (len(temp_types) == 2 and temp_types[1][0] == "(" and temp_types[1][-1] == ")"):
                    transaction_type.append(temp_types[0] + " " + temp_types[1])
                    temp_owner = ""

                # Company name + S (partial)
                elif (len(temp_types[-2]) == 1 and temp_types[-1][0] == "(" and temp_types[-1][-1] == ")"):
                    transaction_type.append(temp_types[-2] + " " + temp_types[-1])
                    temp_list = temp_types[:-2]
                    temp_owner = ' '.join(temp_list)

                # Company name + S
                elif (len(temp_types[-1]) == 1):
                    transaction_type.append(temp_types[-1])
                    temp_list = temp_types[:-1]
                    temp_owner = ' '.join(temp_list)
                
                temp_name = ""

                while (new_index > prev_index and split_text[new_index].upper().count(filing_status) == 0 and split_text[new_index].upper().count(subholding_of) == 0 
                    and split_text[new_index].upper().count(description) == 0):
                    temp_name = temp_owner + " " + temp_name
                    temp_owner = split_text[new_index]
                    new_index -=1

                if (temp_owner == 'JT' or temp_owner == 'SP' or temp_owner == 'SM' or temp_owner == 'DC'):
                    owner.append(temp_owner)
                    company_name.append(temp_name.upper())
                else:
                    owner.append('N/A')
                    company_name.append(temp_owner.upper() + temp_name.upper())

                prev_index = index

    if not (len(amount) == len(transaction_type) == len(date) == len(notification_date) == len(owner) == len(company_name)):
        print("Warning: The lists are not equal in length!")

    return (company_name, transaction_type)

    # with open('output.txt', 'w') as f:
    #     for i in range(len(company_name)):
    #         print("--------------", file=f)
    #         print(company_name[i], file=f)
    #         print(owner[i], file=f)
    #         print(date[i], file=f)
    #         print(notification_date[i], file=f)
    #         print(transaction_type[i], file=f)
    #         print(amount[i], file=f)


