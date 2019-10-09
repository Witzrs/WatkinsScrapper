# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os


#Website root, used to download
root_url = "https://cis.whoi.edu"
# The URL of the index page of Watkins Dataset
index_url= 'https://cis.whoi.edu/science/B/whalesounds/index.cfm'
# url = "https://cis.whoi.edu/science/B/whalesounds/fullCuts.cfm"
base_download_list_url = 'https://cis.whoi.edu/science/B/whalesounds/'
# Connect to the URL

def getBestOfAudios():
    response = requests.get(index_url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    listing=soup.findAll('div',{"class": "large-3"})
    for element in listing[:-1]:
        species_name = (element.div.h3.text) #Species Name, and folder name
        species_url = (element.a['href']) #URL containing the list of audio files
        download_url = base_download_list_url + species_url
        downloadSpeciesAudioFiles(species_name, download_url)
        # time.sleep(1)

def downloadSpeciesAudioFiles (species_name, download_page_url):
    if (not os.path.exists("scrapped/"+species_name)):
        os.mkdir("scrapped/"+species_name)
    response = requests.get(download_page_url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    table_rows = (soup.findChildren('tr'))
    for row in table_rows:
        r = (row.find("a",{"target":"_blank"}))
        if (not r == None ):
            filepath= (r['href'])
            splits = filepath.split("/")
            filename = splits[len(splits)-1]
            download_file_url = (root_url + filepath)
            r = requests.get(download_file_url, allow_redirects=True)
            foldername = species_name + "/" + filename
            if(not os.path.exists("scrapped/"+foldername)):
                open("scrapped/"+foldername, 'wb').write(r.content)
                time.sleep(1)

getBestOfAudios()