#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby
"""

from Airbnb_Spyder import Airbnb_spyder
from Cookies import url_villas,url_other_properties

def collectNumberProp(url):
    
    my_spyder = Airbnb_spyder(url)
    price_ranges = my_spyder.getPriceRangeWrapper()
    print (price_ranges)
    return price_ranges

def collect_db(url,price_ranges = None):

    my_spyder = Airbnb_spyder(url)
    
    property_list = []
    hist = {}
    number_t = 0
    
    for price in price_ranges:
        number_t = 0
        number = 0
        ofs = 0
        last_page_flag = True
        
        while last_page_flag:        

            payload = {'price_min':price[0],'price_max':price[1],'items_offset':ofs}            
            data = my_spyder.getJson(payload)
            processed_data = my_spyder.parsePage(data)
            property_list.extend(processed_data[0])
            number = processed_data[1]            
            print('URL requested for prices from ' + str(price[0]) + ' until ' + str(price[1]))
            print('Got info for ' + str(number) + ' properties.')             
            ofs +=50
            last_page_flag = data['explore_tabs'][0]['pagination_metadata']['has_next_page']    
            number_t += number

        hist[str(number_t)] = (price[0],price[1])
        
    my_spyder.save_data(property_list,'excel','properties_Bali_', 'Data')
    my_spyder.save_data(property_list,'csv','properties_Bali_','Data')
    print (hist)
    total = 0
    for i in hist.keys():
        total += int(i)
    print('total number of properties -->'+str(total))
    
    return property_list

def makeCalendarAvail():
    
    my_spyder = Airbnb_spyder()
    
    db = my_spyder.get_data_from_file('villas_Bali_2019-03-23.csv')

    for property in db[0:3]:
        print(property)
        url = 'https://www.airbnb.ru/api/v2/calendar_months?_format=with_conditions&count=12&currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id={property_id}&locale=en&month=4&year=2019'.format(property_id = property['id'])
        r = my_spyder.get_r(url)
        data = r.json()
        calendar = my_spyder.parsePageProperty(data)
        property.update(calendar)
        
    my_spyder.save_data(db,'excel','avail_',folder_name = None)
    my_spyder.save_data(db,'csv','avial_',folder_name = None)
        
    return db

        
#makeCalendarAvail()
#my_spyder = Airbnb_spyder(url)
#print(my_spyder.cookies)

## info about other private properties (except villas)
url = url_other_properties
#price_ranges = collectNumberProp(url)
price_ranges = [(0, 17, 278), (18, 20, 204), (21, 24, 242), (25, 27, 241), (28, 31, 240), (32, 34, 146), (35, 38, 226), (39, 44, 283), (45, 51, 298), (52, 61, 289), (62, 74, 293), (75, 89, 248), (90, 109, 290), (110, 144, 290), (145, 193, 299), (194, 309, 299), (310, 2000, 248), (2001, 10000, 16)]

db = collect_db(url,price_ranges)
    
    
