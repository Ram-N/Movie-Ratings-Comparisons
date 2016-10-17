# Purpose: This module has functions that go to a URL and download 
# data from it
# Author:      Ram
# Created:     10/15/2016
# Copyright:   (c) Ram 2016
# Licence:     GPL
#-------------------------------------------------------------------------------
import requests
import re
import sys, os
from bs4 import BeautifulSoup
import pandas as pd


def clean_text(text):
    """
    remove blanks, punctuation, % sign
    """ 
    #print repr(text), type(text)
    return(re.sub('[\n(){}<> %]', '', text))

def get_text_inside_parenthesis(s):
    """
    Returns text within parenthesis
    """    
    return(s[s.find("(")+1:s.find(")")])


def construct_valid_movie_url(rt_BASE, rt_search_BASE, movie_name, movie_year):
    """
    In Rotten Tomatoes, the movie URL is not obvious
    A way around that is to first search for term and then to extract the URL
    That is what this function does
    """
        
    def get_coda_if_year_matches(litag, movie_year):
            yr = litag.find('span', {'class':'movie_year'})
            yr= re.sub('[\n(){}<> ]', '', yr.text)
            yr = int(yr)
            if  movie_year in [yr-1, yr, yr+1]:
                atag = litag.find('a')
                return(atag['href']) #coda
            return ""

    movie_year = int(movie_year)
    search_url = rt_BASE+search_BASE+movie_name
    #print search_url    
    r = requests.get(search_url)
    doc = r.text
    soup = BeautifulSoup(doc)
    
    #search through the results
    res = soup.find_all('ul', {'class': 'results_ul'})
    coda=""
    for r in res:
        links = r.find_all('div', {'class':'bold'})
        for idx, litag in enumerate(links):                    
            coda = get_coda_if_year_matches(litag, movie_year)
            if coda!="":
                return rt_BASE+coda
            
    return None    



def get_rt_ratings(rt_url):
 
    tomatometer, audience = 0,0
        
    try:
        r = requests.get(rt_url)
        doc = r.text
        soup = BeautifulSoup(doc)

        title = soup.find('meta', {'property' : 'og:title'})['content']
        #print title
        if title: 
            tomatometer = soup.find('a', {'id' : 'tomato_meter_link'}).text
            audience = soup.find('div', {'class' : 'meter-value'}).text
    except:
        print "URL not right", rt_url
        pass

    tomatometer = clean_text(tomatometer)
    audience = clean_text(audience)
         
    return((tomatometer, audience))

if __name__ == '__main__':


    rt_BASE = "https://www.rottentomatoes.com"
    search_BASE = "/search/?search="

    print(os.getcwd())
    data_dir = "data"
    filename = "current_top250.csv"
    csv_filename = os.path.join(data_dir,filename)
    imdb_ratings = pd.read_csv(csv_filename)
    
    for index, row in imdb_ratings.iloc[20:50].iterrows():    
        movie_name = row['Title']
        movie_year = get_text_inside_parenthesis(movie_name)    
        movie_name = re.sub(r'\(.*?\)', "", movie_name) #get rid of the year
        rt_url = construct_valid_movie_url(rt_BASE, search_BASE, movie_name, movie_year)   
        if rt_url is not None:
            ratings = get_rt_ratings(rt_url)
            print movie_name, movie_year, ratings[0], ratings[1]
        else:
            print "!!!   Unable to find URL for", movie_name, movie_year
            
    print("Done")





