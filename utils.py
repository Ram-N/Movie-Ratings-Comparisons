# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 23:05:28 2016

@author: Ram
"""

def get_text_inside_parenthesis(s):
    """
    Returns text within parenthesis
    """    
    return(s[s.find("(")+1:s.find(")")])
