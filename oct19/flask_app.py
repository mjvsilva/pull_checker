
# Import libraries:
import csv
import os
import urllib.request, json 
from urllib.request import urlopen, Request


# Get links:

with open('lab_names.txt', 'r') as f:
    reader = csv.reader(f)
    lab_names = [name.strip("\'") for name in list(reader)[0]]

path1 = 'https://api.github.com/repos/ta-data-lis/'
path2 = '/pulls?state=open'


if not os.path.isfile('links.txt'):

    open('links.txt', 'a').close()

    for lab_name in lab_names:

        with open('links.txt', 'a', newline='') as myfile:
    #          wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #          wr.writerow(path1 + lab_name + path2)
            myfile.write(",\"" + path1 + lab_name + path2 + "\"")
    print('links.txt has been filled')
else:
    print('links.txt already existed')

with open('links.txt', 'r') as f:
    reader = csv.reader(f)
    page_list = list(reader)[0][1:]


# Do the job:    

token = '5e71cf50d45536be4e0ea4d94a5c70419d69fc72'

zeroes = [] # labs with 0 open pull requests

for url in page_list:

    lab_name = url[39:].strip('pulls?state=open').strip('/')
    request = Request(url)
    request.add_header('Authorization', 'token %s' % token)
    response = urlopen(request)
    # print(response.read())
    data = json.loads(response.read().decode())

    count = 0

    lab_links = []

    for i in range(10):

        try:
            lab_links.append('[' + data[i]['user']['login'] + ']' + '  ' + data[i]['html_url'])
        except:
            break

    count = i
    if not count:
        zeroes.append(lab_name)

    else:
        print('\n' + str(count) + ' open PR for ' + lab_name + ':\n')
        print(*lab_links,sep='\n')

print('\n\n' + str(len(zeroes)) + ' labs with 0 PR')
