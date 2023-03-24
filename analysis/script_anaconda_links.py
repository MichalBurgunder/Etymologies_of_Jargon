# This is a script file that automatically fetches all of the anaconda
# package information and only saves information on the creation year
# of the package. In particular, it accesses the data via an API call.
# For every conda package, it checks whether the package is hosted on
# github, in which case its creation date can be fetched from it. If
# this isn't the case, the the script skips this entry, and moves on to
# the next.
# 
# Because Github only allows for 50 API calls every hour, I
# have spaced out the requests whenever the limit has been reached, so
# that it would try again when access to the API is available again.
# This way, By the end of the script, one will have as much (easily
# accessible) information as possible on the possible creation dates
# of conda packages.
 
# Finally once this is done, it saves the data to conda_links.csv.


import re
import json
import requests
import time
from datetime import datetime
from file_management import save_as_csv, read_csv

def fetch_json(url):
    """
    Access the internet for a specific URL (example below), and saves the contents as a JSON
    """
    # url = "https://api.github.com/repos/MichalBurgunder/filigree"
    headers = {
        'x-rapidapi-host': "random-facts2.p.rapidapi.com",
        'x-rapidapi-key': "YOUR-RAPIDAPI-HUB-Key"
        }
    return str(requests.request("GET", url, headers=headers).text)

def get_strings(url):
    """
    Extracts the creator and repo name of a given link to a conda package.
    In general, this also works for any github repo.
    """
    # test = "https://api.github.com/repos/MichalBurgunder/filigree"
    # t2 = 'https://github.com/MichalBurgunder/Filigree'
    text = url[19:]
    for i in range(0,len(text)):
        if text[i] == '/':
            return text[:i], text[i+1:]


# we require a list of links to every package we would like to anaylze
data = read_csv('links_anaconda_packages', False, '')

final_data = [] # we store the data to be saved here

regex = 'https://github.com/[a-zA-Z_-]{0,100}/[a-zA-Z_0-9]{0,100}' # checks for github links

waits = 0 # determines how many times we should "wait" for the API to become available. Comment out the code references of this variable below to let it run until it's done.
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
  
        final_data.append([data[i][1], ''])
        
save_as_csv(final_data, 'conda_links', False, {})