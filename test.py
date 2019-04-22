#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 23:20:06 2019

@author: moby
"""

from Airbnb_Spyder import Airbnb_spyder
from Cookies import url_other_properties

spyder = Airbnb_spyder(url_other_properties)

payload = {'price_min':10,'price_max':11,'adults':2}

r = spyder.get_r(spyder.url)          
data = r.json()


print (r.url)
#print (dict(r.cookies))
print (r.headers)
property = data['explore_tabs'][0]['sections'][1]['listings'][0]['pricing_quote']
print (property)
# print (data)


        
