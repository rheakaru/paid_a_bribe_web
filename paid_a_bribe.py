from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
from os.path import exists, join
import csv
from csv import DictReader
from datetime import datetime
from time import sleep
from twython import Twython
import tweepy

import json

#DIR_NAME = 'tempdata'
#DATA_FNAME = join(DIR_NAME, 'creds-twitter.json')
#with open('creds.json') as f:
#    creds = json.load(f)

#client = Twython(creds['consumer_key'], creds['consumer_secret'],

#                 creds['access_token'], creds['access_token_secret'])




url = 'http://www.ipaidabribe.com/reports/paid#gsc.tab=0'
DIR_NAME = 'tempdata'
#DATA_FNAME = join(DIR_NAME, 'state_cm_twitter.csv')
DATA_FNAME = 'state_cm_twitter.csv'
pmo_handle = '@PMOIndia'


def get_cm_data():
    thefile = open(DATA_FNAME, 'r')
    rawtxt = thefile.read()
    thefile.close()
    csv_raw = rawtxt.splitlines()
    csv_data = list(csv.DictReader(csv_raw))
    return csv_data

def get_cm_name():
    data = get_cm_data()
    msgs = []
    for entry in data:
        state = entry['State']
        cm = entry['Chief Minister']
        twitter_handle = entry['Twitter']
        if twitter_handle == '':
            twitter_handle = pmo_handle
        msg_template = 'hi {name}! you are the cm of {state} and your twitter handle is {handle}'
        msg = msg_template.format(name = cm, state= state, handle = twitter_handle)
        msgs.append(msg)
    return msgs


def get_all_fields(soup):
    msgs = []
    reports = soup.find_all("section", class_ = "ref-module-paid-bribe")
    for r in reports:
        heading = r.find_all("h3", class_="heading-3")
        link = heading[0].a["href"]
        department_clearfix = r.find_all("ul", class_="department clearfix")[0]
        department_elem = department_clearfix.find_all("li", class_= "name")
        department = department_elem[0].a["title"]
        amount_elem = department_clearfix.find_all("li", class_= "paid-amount")[0]
        amount_list = amount_elem.select('span')[0]
        amount_full = amount_list.text.strip()
        searchObj_amount = re.match(r'Paid (INR .*)',amount_full)
        amount = searchObj_amount.group(1)
        key = r.find_all("div", class_="key")[0]
        date_elem = key.find_all("span", class_= "date")[0]
        date = date_elem.text
        location = key.a['title']
        searchObj = re.match(r'(.*),(.*)',location)
        city = searchObj.group(1).strip()
        state = searchObj.group(2).strip()
        msg_dict= {'date': date, 'amount':amount , 'location':city , 'link':link }
        mydict= {'state': state, 'message_dict': msg_dict}
        msgs.append(mydict)
    return msgs

def get_soup():
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    return soup

def get_cm_info(state):
    data = get_cm_data()
    for entry in data:
        currState = entry['State']
        if currState == state:
            mydict = {}
            mydict['name'] = entry['Chief Minister']
            mydict['twitter_handle'] = entry['Twitter']
            return mydict

def get_num_bribes_from(state,soup):
    numOfBribes = 0;
    reports = soup.find_all("section", class_ = "ref-module-paid-bribe")
    for r in reports:
        key = r.find_all("div", class_="key")[0]
        location = key.a['title']
        searchObj = re.match(r'(.*),(.*)',location)
        bribe_state = searchObj.group(2).strip()
        if bribe_state == state:
            numOfBribes+=1
    return numOfBribes

def is_a_state(state):
    states = []
    soup = get_soup()
    reports = soup.find_all("section", class_ = "ref-module-paid-bribe")
    for r in reports:
        key = r.find_all("div", class_="key")[0]
        location = key.a['title']
        searchObj = re.match(r'(.*),(.*)',location)
        bribe_state = searchObj.group(2).strip()
        states.append(bribe_state)
    if state in states:
        return True
    else:
        return False

def web_app(state):
    if (is_a_state(state)):
        soup = get_soup()
        mydict = get_cm_info(state)
        numOfBribes = get_num_bribes_from(state,soup)
        bribe_msg_template = 'We recieved {amount_of_bribes} reports of bribes in {state} recently. The Chief Minister of {state} is {name}. You can reach {name} on Twitter at {twitter_handle}.'
    #msg1 = accountable_msg_template.format(state= state, name = mydict['name'], twitter_handle = twitter_handle)
        msg = bribe_msg_template.format(amount_of_bribes = numOfBribes , state = state, name = mydict['name'], twitter_handle = mydict['twitter_handle'])
    else:
        msg = ' That is not a valid state in India. Try "Karnataka" or "Assam" '
    return msg


def make_msg(msg_dict, twitter_handle):
    msg_template = 'Hi {twitter_handle}! On {date}, a bribe of {amount} was paid in {location}. Read more at: {link}'
    msg = msg_template.format(twitter_handle = twitter_handle, date = msg_dict['date'], amount = msg_dict['amount'] , location = msg_dict['location'] , link = msg_dict['link'] )
    return msg

def main():
    soup = get_soup()
    messages = get_cm_name()
    #for message in messages:
    #    print (message)

    #all_msgs = get_all_fields(soup)
    #for m in all_msgs:
    #    state = m['state']
    #    msg_dict = m['message_dict']
    #    cm_info_dict = get_cm_info(state)
    #    twitter_handle = cm_info_dict['twitter_handle']
    #    rtext = make_msg(msg_dict, twitter_handle)
    #    sleep(3)
    # actually send the reply
    #    client.update_status(status=rtext)

        #print('i am here')
    #print()

main()
