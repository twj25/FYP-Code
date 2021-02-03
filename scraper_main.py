import requests
from bs4 import BeautifulSoup
import pprint
import database_helper
import re

def populate_places(headings):
    # The first data extracted is the headings - these correspond to place names
    heads = []
    for heading in headings:
        head = heading.next
        heads.append(head)
    heads.remove('Location ')

    database_helper.delete_all_places()
    database_helper.places_load(heads)
    return len(heads)

def disect_tables(tables):
    elements = tables.find_all('td')
    samples = []
    for element in elements:
        try:
            year = int(element.text)
            samples.append(year)
        except:
            frequency = element.text
            try:
                link = element.next.attrs['href']
            except:
                link = 'NULL'
            sample = [frequency,link]
            samples.append(sample)
    return samples

def obtain_1st_layer_links(num_places, tables):
    # The code below calls a function which disects the tables (extracting frequencys and corresponding links)
    # Then the data is commited to the database
    database_helper.delete_all_samples()
    for id in range(1,num_places+1):
        samples = disect_tables(tables[id-1])  
        database_helper.samples_load(samples,id)
    
    return

def obtain_2nd_layer_links(baseURL):
    # function inputs: data required (specified by year, frequency ect.)
    # - function deletes current contents from data table
    # - function requests all the links required 
    # - function loops through links, calling function which retrieve new links 
    # - function saves new links to data table
    # return: nothing
    database_helper.delete_all_data()
    samples = database_helper.return_all_samples()
    print(len(samples), 'samples to process')
    for sample in samples:
        print(round((int(sample[0])/len(samples))*100,2),'%')
        if sample[1] != 'NULL':
            link = URL + sample[1]
            links_2nd_layer = getLinks(link)
            database_helper.data_load(links_2nd_layer,sample[0])
    return

def getLinks(url):
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    table = soup.find(class_= 'data')
    links = []
    month = 1
    prev_day = 1
    for entry in table.findAll('a'):
        day = int(entry.text)
        # print(day)
        # if day == 25 or day == 26 or day == 27 or day == 28 or day == 1:
        #     x = 1
        #     pass
        if day < prev_day:
            month += 1
        links.append([day,month,entry.get('href')])
        prev_day = day
    return links

# URL of the webpage being scraped
URL = 'http://sirius.bu.edu/data/'

# Following code extracts the useful blocks of content from the page
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id= 'content')
headings = results.find_all('strong', style = "color:navy")
tables = results.find_all(class_= 'data')

num_places = populate_places(headings)

obtain_1st_layer_links(num_places, tables)

# now i need to call the database and request links
# for each link requested i will call a general function which will populate the data table with the links for the link given
obtain_2nd_layer_links(URL)



