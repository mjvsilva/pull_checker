# Import libraries:
import csv
import os
import urllib.request, json 
from urllib.request import urlopen, Request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# gspread stuff (https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
# After that, search Google Sheets API and enable it as well.

print('\nGetting credentials from json...')

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

print('\nAdding links to txt...')

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
print('\nlinks.txt has been filled')


# Do the job:  

with open('links.txt', 'r') as f:
    reader = csv.reader(f)
    page_list = list(reader)[0][1:]
    

token = '5e71cf50d45536be4e0ea4d94a5c70419d69fc72'

week_number = int(input("\nWhich week? "))

limit_dict = {1:8, 2:16, 3:22, 4:30, 5:40, 6:40, 7:46, 8:len(page_list), 9:len(page_list)}

top_limit = limit_dict[week_number] + 2

print('\nGetting labs info (this may take a while)...\n\n')

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
                lab_links.append('[' + data[i]['user']['login'] + ']' + '  ' + data[i]['html_url'])
                count2 += 1
                
        i += 1
            
    if count2:
        print('\n' + str(count2) + ' PR to check for ' + lab_name + ':\n')
        lab_links.reverse()
        print(*lab_links,sep='\n')
      
print('\n\nHave a good time checking!\n')
