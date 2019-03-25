#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 15:29:38 2019

@author: moby
"""

from spyder_main import Spyder
import math

class Airbnb_spyder(Spyder):
 
    def __init__(self,url):
        
        Spyder.__init__(self)
        self.url = url
        self.cookies = {'bev':'1547156014_VrXrRUfcBGnBPRQk','_gcl_au':'1.1.298100599.1547156017',\
        'ftv':'1547156016784', '_ga':'GA1.2.1375804564.1547156017',\
        '__ssid':'85521ba0b8c68562a734ddfd0f0d2c3', 'sdid':'', 'cereal_exp':'2',\
        '_csrf_token':'V4%24.airbnb.com%245G3lzK7SnKw%24UkERm1LaEa-diDxONzni-lMPOhVh6kqAznVb4nbWG3M%3D',\
        'flags':'0', 'cdn_exp_c93eb6109a0d84ec9':'control', 'e34ba1aae':'treatment', \
        '016951b48':'control', 'hyperloop_explore_exp_v2':'2',\
        'jitney_client_session_id':'f8427140-7a2a-4926-9ae1-8f30b03b5433',\
        'jitney_client_session_created_at':'1553092611', 'AMP_TOKEN':'4NOT_FOUND',\
        '_gid':'GA1.2.1007818538.1553092612', '_user_attributes':'%7B%22curr%22%3A%22USD%22%2C%22guest_exchange%22%3A1.0%2C%22device_profiling_session_id%22%3A%221552855316--c232954733f7e47b91033b8d%22%2C%22giftcard_profiling_session_id%22%3A%221553092611--3ac719930588468e04f898f1%22%2C%22reservation_profiling_session_id%22%3A%221553092611--762a09682b3b44e278aeed78%22%7D',\
        'cache_state':'0', 'currency':'USD', '66bf01231':'treatment', \
        '_gat':'1','jitney_client_session_updated_at':'1553092762','cbkp':'1'}
            
    def getNumberProp(self,data):
        
        """
        gets json array of data and returns number of properties in the request
        
        """
        try:         
            number_prop = data['explore_tabs'][0]['home_tab_metadata']['listings_count']        
                
        except (KeyError, TypeError):
            return None
        
        return number_prop
    
    def getPriceRange(self,min,max,url,max_p = None):
        
        """
        defines the range of prices for URL request to get the maximum number 
        of propertes per request (close to 300)
        
        """
    
        payload = {'price_min':min,'price_max':max}
        
        r = self.get_r(url,payload)
        
        data = r.json()
          
        number = self.getNumberProp(data)
        
#        print(min,max,'-->',number)

        if max_p == None:                                    
            delta = int((max-min)//2)
            if number  <= 300:
                return min,max,number
        else: 
            delta = int(math.fabs(max - max_p)//2)                        
       
#        print (delta)
        
        if delta > 0:
            if number > 300:
                min,max,number = self.getPriceRange(min,max-delta,url,max)
            elif (300 - number) > 10:
                min,max,number = self.getPriceRange(min,max+delta,url,max)
            else:
                return min,max,number
                    
        else:
            if number > 300:
                min,max,number = self.getPriceRange(min,max-1,url,max)
#                print('понижение на 1 пункт')
#            else:
#                print('окончание поиска')
        print(min,max,number)
        return min,max,number
    
    def getPriceRangeWrapper(self,url):
        
        price_ranges = []
        min = 0
        max = 2000
            
        while min < max:
            min_max = self.getPriceRange(min,max,url)
            price_ranges.append(min_max)
            min = min_max[1] + 1
        
        price_ranges.append(self.getPriceRange(min,10000,url))
        
        return price_ranges
    
    
    def parserHelper(self,data,*args):
        
        if args and data:
            element  = args[0]
  #          print(element)
            if isinstance(element,str):                
                value = data.get(element)
 #               print('dict')
            else:
                value = data[element]                
#                print('list')

            return value if len(args) == 1 else self.parserHelper(value, *args[1:])
        else:
            return 'no data'

    def parsePage(self,data):
        
        """
        gets dict/list of data (just a single page) and returns a list of properties with relevant info on them
        
        """
        property_list = []
#        print (data['explore_tabs'][0]['sections'][0]['listings'][0])
        data_s = self.parserHelper(data,'explore_tabs',0,'sections',1,'listings')
       # print(data_s[1])
        
        for i in range(len(data_s)):
            
            property = {}            
            
            property['id'] = self.parserHelper(data_s,i,'listing','id')
            property['name'] = self.parserHelper(data_s,i,'listing','name')
            property['dprice'] = self.parserHelper(data_s,i,'pricing_quote','rate','amount')
            property['currency'] = self.parserHelper(data_s,i,'pricing_quote','rate','currency')
            property['nreviews'] = self.parserHelper(data_s,i,'listing','reviews_count')
            property['area'] = self.parserHelper(data_s,i,'listing','city') 
            property['subdistrict'] = self.parserHelper(data_s,i,'listing','public_address')
            property['llcord'] = str(self.parserHelper(data_s,i,'listing','lat'))+','+str(self.parserHelper(data_s,i,'listing','lng'))
            property['nbedrooms'] = self.parserHelper(data_s,i,'listing','bedrooms')
            property['max_guests'] = self.parserHelper(data_s,i,'listing','person_capacity')
            property['url'] = self.parserHelper(data_s,i,'listing','picture_url')
            
            "optional info"
            
            property['instant_booking'] = self.parserHelper(data_s,i,'pricing_quote','can_instant_book')
            property['monthly_price_f'] = self.parserHelper(data_s,i,'pricing_quote','monthly_price_factor')
            property['weekly_price_f'] = self.parserHelper(data_s,i,'pricing_quote','weekly_price_factor')
            property['is_superhost'] = self.parserHelper(data_s,i,'listing','is_superhost')
            property['picture_count'] = self.parserHelper(data_s,i,'listing','picture_count')
            property['host_lang'] = '/'.join(self.parserHelper(data_s,i,'listing','host_languages')) #joined into one string for correct export to excel cell
            property['host_picture'] = self.parserHelper(data_s,i,'listing','user','picture_url')            
            property['review_score'] = self.parserHelper(data_s,i,'listing','avg_rating')
            property['picture_colour'] = self.parserHelper(data_s,i,'listing','picture','dominant_saturated_color')

            property_list.append(property)                

        return property_list
        
        
