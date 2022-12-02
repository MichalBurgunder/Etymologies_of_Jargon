import re
import json
import requests
import time
from datetime import datetime
from file_management import save_as_csv, read_csv




def fetch_json(url):
    # url = "https://api.github.com/repos/MichalBurgunder/filigree"
    headers = {
        'x-rapidapi-host': "random-facts2.p.rapidapi.com",
        'x-rapidapi-key': "YOUR-RAPIDAPI-HUB-Key"
        }
    return str(requests.request("GET", url, headers=headers).text)


def get_strings(url):
    # test = "https://api.github.com/repos/MichalBurgunder/filigree"
    # t2 = 'https://github.com/MichalBurgunder/Filigree'
    text = url[19:]
    for i in range(0,len(text)):
        if text[i] == '/':
            return text[:i], text[i+1:]


data = read_csv('links_anaconda_packages', False, '')

final_data = []
# get_strings()
# x = re.search("https://github.com/[a-zA-Z_-]{0,100}/[a-zA-Z_0-9]{0,100}", txt)
regex = 'https://github.com/[a-zA-Z_-]{0,100}/[a-zA-Z_0-9]{0,100}'
# data = [['https://github.com/MichalBurgunder/Filigree', 'me']]
waits = 0
for i in range(0, len(data)):
    try:
        if i % 20 == 0:
            print(f'completed {i}')
        if waits == 7:
            break
        if re.search(regex, data[i][0]):
            creator, repo = get_strings(data[i][0])
            res = fetch_json(f"https://api.github.com/repos/{creator}/{repo}")
            the_json = json.loads(res)
            if 'message' in the_json and 'API rate limit exceeded' in the_json['message']:
                waits += 1
                print(f"requests exceeded. Going to nap for an hour now (starting at {datetime.now()}). Good night...")

                time.sleep(3650) # per hour limit
                # we try again
                res = fetch_json(f"https://api.github.com/repos/{creator}/{repo}")
                the_json = json.loads(res)
            year = the_json['created_at'][0:4]
            final_data.append([data[i][1], year])

        else:
            final_data.append([data[i][1], ''])
    except: 
        print('Error occured. Appending nothing')
        print(data[i])
        final_data.append([data[i][1], ''])
        
save_as_csv(final_data, 'conda_links', False, {})