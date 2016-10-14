# Purpose: This module has functions that go to a URL and download 
# data from it
# Author:      Ram
# Created:     10/14/2016
# Copyright:   (c) Ram 2016
# Licence:     GPL
#-------------------------------------------------------------------------------
import requests
import urllib2
import urllib
import re
import sys
from bs4 import BeautifulSoup
import csv


def webpage_to_csv(url, csv_output_filename):

    r = requests.get(url)
    doc = r.text
    soup = BeautifulSoup(doc)

    table = soup.find('table')

        

    #rows = table.findAll('tr') #findAll returns a list
    #for tr in rows:
    #    cols = tr.findAll('td')
    #    for c in cols:
    #        print c.text,
    #    print 

    with open(csv_output_filename, 'w') as f:
        csvwriter = csv.writer(f)

        header_row = table.find('tr', attrs={'class': 'row_header'})
        hdrs = [h.text.encode('utf-8') for h in header_row.findAll('th')]
        csvwriter.writerow(hdrs)

        for row in table.findAll('tr'):
            cells = [c.text.encode('utf-8') for c in row.findAll('td')]
            csvwriter.writerow(cells)
    print("wrote to csv", csv_output_filename)            





if __name__ == '__main__':

    dl_flag = 1
    progress_flag = 0

    PROD_YEARS = "http://top250.info/stats/?8"
    csv_output_filename = 'data/PROD_YEARS.csv'

    current_url = PROD_YEARS

    #create a list of all the URLs to be downloaded...
    webpage_to_csv(current_url, csv_output_filename)

    print("Done")





