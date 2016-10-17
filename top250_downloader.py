# Purpose: This module has functions that go to a URL and download 
# data from it
# Author:      Ram
# Created:     10/14/2016
# Copyright:   (c) Ram 2016
# Licence:     GPL
#-------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import csv
import re

import utils

def webtable_to_csv(url, csv_output_filename, table_num=1):

    def add_year_column(cells):
        yr = ""
        if len(cells)>=3:
            yr = utils.get_text_inside_parenthesis(cells[2])
        return yr

    def clean_up_title(cells):

        if len(cells)>=3:
            title = cells[2].split(',')   
            print title.reverse()
            cells[2] = "".join(title)                       
            cells[2]= re.sub(r'\([^)]*\)', '', cells[2]) #drop the yr inside parenthesis
            
        print cells
        return cells


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
            hdrs.append("Year")
            csvwriter.writerow(hdrs)
            
            for row in table.findAll('tr'):
                cells = [c.text.encode('utf-8') for c in row.findAll('td')]                
                #Parse out the year and make it a new element
                cells.append(add_year_column(cells)) #add year column
                cells = clean_up_title(cells) # reverse as needed, and drop year                
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





