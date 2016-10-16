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


def webtable_to_csv(url, csv_output_filename, table_num=1):

    r = requests.get(url)
    doc = r.text
    soup = BeautifulSoup(doc)

    tables = soup.find('body').find_all('table')
    print "Total of ", len(tables), "tables"
    #table = soup.find('table')
    table = soup.findAll('table')[table_num-1]
    
    def write_table_to_file(table, csv_output_filename):
        with open(csv_output_filename, 'wb') as fp:
            csvwriter = csv.writer(fp, delimiter=',')
    
            header_row = table.find('tr', attrs={'class': 'row_header'})
            hdrs = [h.text.encode('utf-8') for h in header_row.findAll('th')]
            csvwriter.writerow(hdrs)
            
            for row in table.findAll('tr'):
                cells = [c.text.encode('utf-8') for c in row.findAll('td')]
                csvwriter.writerow(cells)
                
        print("wrote to csv", csv_output_filename)            


    write_table_to_file(table, csv_output_filename)


if __name__ == '__main__':

    dl_flag = 1
    progress_flag = 0

    PROD_YEARS = "http://top250.info/stats/?8"
    csv_output_filename = 'data/PROD_YEARS.csv'
    
    CURRENT_250 = "http://top250.info/charts/"
    csv_output_filename = 'data/current_top250.csv'
    table_num =2

    current_url = CURRENT_250

    #create a list of all the URLs to be downloaded...
    webtable_to_csv(current_url, csv_output_filename, table_num)

    print("Done")





