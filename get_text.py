import os
import csv
import re
import urllib
import requests
import ssl
from time import sleep
from bs4 import BeautifulSoup

context = ssl._create_unverified_context()

def format_query(search_query, year_from, year_to):
    year = 'AND' + year_from + ':' + year_to + '[pdat]'
    if ' ' not in search_query and year_from =='':
      final_query = search_query
    else:
      query = '"' + '+'.join(search_query.split())
      final_query = query + year + '"'

    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    db = 'db=pubmed'
    search_eutil = 'esearch.fcgi?'
    search_term = '&term=' + final_query
    search_usehistory = '&usehistory=y'
    search_rettype = '&rettype=json'
    search_url = base_url + search_eutil + db + search_term + search_usehistory + search_rettype

    return search_url


def fetch_url(search_url):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    db = 'db=pubmed'

    f = urllib.request.urlopen(search_url, context = context)
    search_data = f.read().decode('utf-8')
    total_abstract_count = int(re.findall("<Count>(\d+?)</Count>", search_data)[0])

    fetch_webenv = '&WebEnv=' + re.findall("<WebEnv>(\S+)<\/WebEnv>", search_data)[0]
    fetch_querykey = '&query_key=' + re.findall("<QueryKey>(\d+?)</QueryKey>", search_data)[0]
    fetch_eutil = 'efetch.fcgi?'
    retmax = 100
    retstart = 0
    fetch_retstart = "&retstart=" + str(retstart)
    fetch_retmax = "&retmax=" + str(retmax)
    fetch_retmode = "&retmode=text"
    fetch_rettype = "&rettype=abstract"

    fetched_url = base_url + fetch_eutil + db + fetch_querykey + fetch_webenv + fetch_retstart + fetch_retmax + fetch_retmode + fetch_rettype
    return fetched_url

def download_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        return text
    else:
        print("Failed to download.")
        return None

def save_text_to_file(text, filename):
    with open(filename, 'w', encoding = 'utf-8') as file:
        file.write(text)
    print("Text saved to" , filename)
