#!/usr/bin/env python2

import pycurl, json
from StringIO import StringIO
from bs4 import BeautifulSoup

import boto3
import botocore.session
import os.path
from requests import ConnectionError

from googlez import search

import random, string


# NOTE: need to get AWS access key from Pierreu

BUCKET_NAME = 'pepper-arx'

s3 = boto3.resource('s3')
session = botocore.session.get_session()
client = session.create_client('s3')
bucket = s3.Bucket(name=BUCKET_NAME)

s3_url_format = 'http://{0}.s3.amazonaws.com/{{0}}'.format(BUCKET_NAME)

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

## given image_path on local computer
## uploads image to s3 and gives url
def upload_to_s3(image_path):
    f = open(image_path,'rb')
    # key = os.path.basename(image_path)
    key = randomword(30)
    obj = bucket.put_object(Key=key, Body=f, ACL='public-read')
    obj.wait_until_exists()
    print(obj.get())
    # obj.put(ACL='public-read')
    return s3_url_format.format(key)
    

## given an image path, this should search and find some website
def get_website(image_path):
    # upload image to s3, get url
    image_url = upload_to_s3(image_path)
    print(image_url)

    # google reverse image search
    code = retrieve(image_url)
    parsed = google_image_results_parser(code)

    print(parsed)
    title = parsed['title'][0]
    print(title)
    
    gen = search('site:wikipedia.org ' + title)
    wiki_link = next(gen)
    
    print(wiki_link)
    # get some wikipedia linked from the parsed result
    ## get first title
    ## look it up on wikipedia.org
    
    return wiki_link

def get_image_search_results(image_path):
    image_url = upload_to_s3(image_path)
    print(image_url)

    # google reverse image search
    code = retrieve(image_url)
    parsed = google_image_results_parser(code)

    return parsed

def get_card_section(image_path):
    image_url = upload_to_s3(image_path)
    print(image_url)

    # google reverse image search
    code = retrieve(image_url)
    print('got code')

    soup = BeautifulSoup(code, 'lxml')
    print('got soup')

    div = soup.find('div', attrs={'class', 'card-section'})
    print(div)
    
    guess = div.find(attrs={'class': '_gUb'})
    if guess:
       guess = guess.text
       
    print(guess)

    return guess

# retrieves the reverse search html for processing. This actually does the reverse image lookup
def retrieve(image_url):
    returned_code = StringIO()
    full_url = 'https://www.google.com/searchbyimage?&image_url=' + image_url
    conn = pycurl.Curl()
    conn.setopt(conn.URL, str(full_url))
    conn.setopt(conn.FOLLOWLOCATION, 1)
    conn.setopt(conn.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')
    conn.setopt(conn.WRITEFUNCTION, returned_code.write)
    conn.perform()
    conn.close()
    return returned_code.getvalue()

# Parses returned code (html,js,css) and assigns to array using beautifulsoup
def google_image_results_parser(code):
    soup = BeautifulSoup(code, 'lxml')

    # initialize 2d array
    whole_array = {'links':[],
                   'description':[],
                   'title':[],
                   'result_qty':[]}


    div = soup.find('div', attrs={'class', 'card-section'})
    print(div)
    
    guess = div.find(attrs={'class': '_gUb'})
    if guess:
       whole_array['guess'] = guess.text
    else:
       whole_array['guess'] = None

    
    # Links for all the search results
    for li in soup.findAll('li', attrs={'class':'g'}):
        sLink = li.find('a')
        whole_array['links'].append(sLink['href'])

    # Search Result Description
    for desc in soup.findAll('span', attrs={'class':'st'}):
        whole_array['description'].append(desc.get_text())

    # Search Result Title
    for title in soup.findAll('h3', attrs={'class':'r'}):
        whole_array['title'].append(title.get_text())

    # Number of results
    for result_qty in soup.findAll('div', attrs={'id':'resultStats'}):
        whole_array['result_qty'].append(result_qty.get_text())

    return whole_array


# path  = '/home/pierre/downloads/penguin.jpg'
# print(get_website(path))
