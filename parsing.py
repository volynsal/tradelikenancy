def parsing(doc):
    owner = []
    company_name = []
    transaction_type = []
    date = []
    notification_date = []
    amount = []
    id = []

    filing_status = "FILING STATUS:"
    subholding_of = "SUBHOLDING OF:"
    description = "DESCRIPTION:"
    filing_id = "FILING ID #"

    text = ""

    for page in doc:
        text += page.get_text()

    split_text = text.split('\n')

    # Changed while loop to be greater than 0 instead of equal, helps to process first row on every page after first
    prev_index = -1
    prev_amount = ''
    first_amount_index = -1

    for index, line in enumerate(split_text):
        # Empty line
        if (len(line) == 0):
            continue
        # Ignore line if it has only one lowercase letter
        elif (len(line) == 1 and line[0] >= 'a' and line[0] <= 'z'):
            continue
        # First transaction (end of the header of the document)
        elif (line[0] == '$' and line[-1] == '?'):
            prev_index = index
            continue

        # Amount is on 2 lines
        elif (line[0] == "$" and line.count('$') == 1 and line.count(',') > 0):
            if (prev_amount == ''):
                prev_amount = line
                first_amount_index = index
                continue
            else:
                line = prev_amount + " " + line
                index -= 1
                prev_amount = ''
    
        # Index to start processing for company name
        new_index = 0
    
        if ((line[0] == ('$') and line.count('$') == 2 and line.count(',') > 0)):
            amount.append(line)
            if (first_amount_index > -1):
                index = first_amount_index
                first_amount_index = -1
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
                and split_text[new_index].upper().count(description) == 0 and split_text[new_index].upper().count(filing_id) == 0):
                temp_name = temp_owner + " " + temp_name
                temp_owner = split_text[new_index]
                new_index -=1

            split_temp_owner = temp_owner.split(' ')

            #Just owner
            if (len(split_temp_owner) == 1 and (temp_owner == 'JT' or temp_owner == 'SP' or temp_owner == 'SM' or temp_owner == 'DC')):
                id.append('N/A')
                owner.append(temp_owner)
                company_name.append(temp_name.upper())
            # Just ID
            elif (len(split_temp_owner) == 1 and len(temp_owner) == 10 and temp_owner.isdigit()):
                id.append(temp_owner)
                owner.append('N/A')
                company_name.append(temp_name.upper())
            # ID + Owner
            elif (len(split_temp_owner) == 2 and len(split_temp_owner[0]) == 10 and split_temp_owner[0].isdigit() and 
                  (split_temp_owner[1] == 'JT' or split_temp_owner[1] == 'SP' or split_temp_owner[1] == 'SM' or split_temp_owner[1] == 'DC')):
                id.append(split_temp_owner[0])
                owner.append(split_temp_owner[1])
                company_name.append(temp_name.upper())
            #Company name without anything
            else:
                id.append('N/A')
                owner.append('N/A')
                company_name.append(temp_owner.upper() + " " + temp_name.upper())

            prev_index = index

    if not (len(amount) == len(transaction_type) == len(date) == len(notification_date) == len(owner) == len(company_name)):
        print("Warning: The lists are not equal in length!")

    # with open('output.txt', 'w') as f:
    #     for i in range(len(company_name)):
    #         print("--------------", file=f)
    #         print(id[i], file=f)
    #         print(company_name[i], file=f)
    #         print(owner[i], file=f)
    #         print(date[i], file=f)
    #         print(notification_date[i], file=f)
    #         print(transaction_type[i], file=f)
    #         print(amount[i], file=f)

    return (owner, company_name, transaction_type, date, notification_date, amount)




