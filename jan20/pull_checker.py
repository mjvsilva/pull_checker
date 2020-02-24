# Import libraries:
import csv
import os
import urllib.request, json 
from urllib.request import urlopen, Request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import random

# gspread stuff (https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
# After that, search Google Sheets API and enable it as well.

# print('\nGetting credentials from json...')

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('control-panel.json', scope)
client = gspread.authorize(creds)

print('\nOpening spreadsheet...')

cp = client.open("January 2020 Data Analytics Full Time | Control Panel v1.0")

labs = cp.get_worksheet(9)

lab_cp = dict(zip([labs.cell(2,i).value for i in range(4,63)], list(range(4,63))))

users = {'japana26':3, 'anafrs':4, 'pengtianan':5, '4kiUta':6, 'Mariehllrd':7,
         'ElviraHae':8, 'duarteharris':9, 'joaopbe':10, 'SilviaNicolau':11, 'aariops':12,
         'cleanspin':13, 'GabrielaScatena':14, 'fckoch':15, 'Satarasiel':16, 'ricardozacarias':17, 'beatrizrenault':18, 'josemrquintas':19, 'TiagoCasaleiroDias':20}

# Get links:

# print('\nAdding links to txt...')

with open('lab_names.txt', 'r') as f:
    reader = csv.reader(f)
    lab_names = [name.strip("\'") for name in list(reader)[0]]

path1 = 'https://api.github.com/repos/ta-data-lis/'
path2 = '/pulls?state=closed'

with open('links.txt', 'w', newline='') as myfile:
#          wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#          wr.writerow(path1 + lab_name + path2)
    for lab_name in lab_names:
        myfile.write(",\"" + path1 + lab_name + path2 + "\"")
        
# print('\nlinks.txt has been filled')


# Do the job:  

with open('links.txt', 'r') as f:
    reader = csv.reader(f)
    page_list = list(reader)[0][1:]
    

token = '5e71cf50d45536be4e0ea4d94a5c70419d69fc72'

week_number = int(input("\nWhich week? "))

limit_dict = {1:8, 2:16, 3:22, 4:30, 5:40, 6:40, 7:46, 8:len(page_list), 9:len(page_list)}

top_limit = limit_dict[week_number] + 2

fun = ["the first electronic computer ENIAC weighed more than 27 tons and took up 1800 square feet.", "only about 10% of the world’s currency is physical money, the rest only exists on computers.", "TYPEWRITER is the longest word that you can write using the letters only on one row of the keyboard of your computer.", "Doug Engelbart invented the first computer mouse in around 1964 which was made of wood.", "there are more than 5000 new computer viruses are released every month.", "around 50% of all Wikipedia vandalism is caught by a single computer program with more than 90% accuracy.", "if there was a computer as powerful as the human brain, it would be able to do 38 thousand trillion operations per second and hold more than 3580 terabytes of memory.", "the password for the computer controls of nuclear tipped missiles of the U.S was 00000000 for eight years.", "approximately 70% of virus writers are said to work under contract for organized crime syndicates.", "HP, Microsoft and Apple have one very interesting thing in common – they were all started in a garage.", "an average person normally blinks 20 times a minute, but when using a computer he/she blinks only 7 times a minute.", "the house where Bill Gates lives, was designed using a Macintosh computer.", "the first ever hard disk drive was made in 1979, and could hold only 5MB of data.", "the first 1GB hard disk drive was announced in 1980 which weighed about 550 pounds, and had a price tag of $40,000.", "more than 80% of the emails sent daily are spams.", "a group of 12 engineers designed IBM PC and they were called as The Dirty Dozen.", "the original name of Windows was Interface Manager.", "the first microprocessor created by Intel was the 4004. It was designed for a calculator, and in that time nobody imagined where it would lead.", "IBM 5120 from 1980 was the heaviest desktop computer ever made. It weighed about 105 pounds, not including the 130 pounds external floppy drive.", "Genesis Device demonstration video in Star Trek II: The Wrath of Khan was the the first entirely computer generated movie sequence in the history of cinema. That studio later become Pixar."]

print(f"\nGetting labs info (this may take a while)...\n\nIn the meantime, did you know that {random.choice(fun).rstrip('.')}?\n\n")

api_limit = 0

for url in page_list[:top_limit]:
    
    lab_name = url[39:].strip('pulls?state=closed').strip('/')
    request = Request(url)
    request.add_header('Authorization', 'token %s' % token)
    response = urlopen(request)
    # print(response.read())
    data = json.loads(response.read().decode())

    count2 = 0
    
    lab_links = []
    
    i = 0
    

    while i < len(data) and data[i]['created_at'].startswith('2020'):   
        
        if len(data[i]['labels'])==0:

            user = data[i]['user']['login']

            # Writes Delivered in Control Panel
            if user in users:
                labs.update_cell(users[user], lab_cp[lab_name], 'Delivered')
                api_limit += 1
                lab_links.append('[' + data[i]['user']['login'] + ']' + '  ' + data[i]['html_url'])
                count2 += 1
                
        i += 1
        
        if api_limit == 98:
            print("")
            if input("\nAPI limit reached.\n\nYou have 100 labs to check. Want to wait 100 seconds and retrieve more? (y/n)") == "y":                
                print(f"\nRetrieveing more labs...\n\nIn the meantime, did you know that {random.choice(fun).rstrip('.')}?\n")
                time.sleep(100)
            
            else:
                api_limit += 1
                break
            
    if count2:
        print('\n' + str(count2) + ' PR to check for ' + lab_name + ':\n')
        lab_links.reverse()
        print(*lab_links,sep='\n')
        
    if api_limit == 99:
        break
      
print('\n\nHave a good time checking! 🍕 \n')
