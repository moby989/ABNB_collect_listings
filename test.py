#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 23:20:06 2019

@author: moby
"""

from Airbnb_Spyder import Airbnb_spyder
from Cookies import url_other_properties
from file_writer import FileWriter
#from requests_html import HTMLSession



url2 = 'https://www.whatismybrowser.com'


spyder = Airbnb_spyder(url_other_properties)
#spyder2 = Airbnb_spyder(url2)


#payload = {'price_min':10,'price_max':11}
#session = HTMLSession()

r = spyder.get_r(spyder.url)          

data = r.json()


#r2 = spyder2.get_r(spyder2.url)
#r2_text = str(r2.content)
#name  = spyder2.makeTextFile(r2_text)
#writer = FileWriter(name)
#writer.file_uploadGDrive_token(name)




#print (r.url)
#print (dict(r.cookies))
print (r.headers)
property = data['explore_tabs'][0]['sections'][0]
property2 = data['explore_tabs'][0]['sections'][1]['listings'][0]['pricing_quote']
property3 = data['explore_tabs'][0]['sections']
#property4 = data['explore_tabs'][0]['sections'][2]
print (property)
print (property2)
print (len(property3))
print (property4)

name  = spyder.makeTextFile(str(data))
writer = FileWriter(name)
writer.file_uploadGDrive_token(name)

#k = r.cookies

 
#print (dict(k))
#print (r2.content)
