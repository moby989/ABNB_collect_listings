#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 23:20:06 2019

@author: moby
"""

from Airbnb_Spyder import Airbnb_spyder
from Cookies import url_other_properties


url2 = 'https://www.whatismybrowser.com'


spyder = Airbnb_spyder(url_other_properties)
spyder2 = Airbnb_spyder(url2)


#payload = {'price_min':10,'price_max':11}

r = spyder.get_r(spyder.url)          
data = r.json()



r2 = spyder.get_r(spyder2.url)



print (r.url)
#print (dict(r.cookies))
print (r.headers)
property = data['explore_tabs'][0]['sections'][0]['listings'][0]['pricing_quote']
print (property)

k = r.cookies

 
print (dict(k))
print (r2.content)

        
