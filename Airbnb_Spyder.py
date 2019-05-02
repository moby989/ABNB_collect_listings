#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 15:29:38 2019

@author: moby
"""

from Spyder import Spyder
from json import JSONDecodeError
import math


class Airbnb_spyder(Spyder):
 
    def __init__(self,url):
        
        Spyder.__init__(self)
        self.url = url                     
        
    def getNumberProp(self,data):
        
        """
        gets json array of data from API and returns number of properties
        for the search page
        
        """        
        number_prop = self.parserHelper(data,'explore_tabs',0,'home_tab_metadata','listings_count')        
                        
        return number_prop
    
    def getJson(self,payload,retry_count = 1):
        
        """
        HELPER FUNCTION
        retries requests if the previous attempt was unsuccessful
        
        """
        r = self.get_r(self.url,payload)          
        try:        
            data = r.json()
        except (JSONDecodeError,AttributeError):
            error_message = 'There was an error getting JSON object from URL {url} and {payload}'.format(url = self.url,payload = payload)
            text_file = self.createTextFile (error_message,'errors.txt')
            self.file_uploadGDrive(text_file)
            data = None
            
        print ('Retry getting JSON N '+str(retry_count))

        if isinstance(data,type(None)):
            retry_count +=1 
            if retry_count > 4:
                print("can't make the request to API")
                return data
            else:
                self.getJson(payload,retry_count)
        else:
            return data
                
    
    def getPriceRange(self,min,max,max_p = None):
        
        """
        defines the range of prices for URL request to get the maximum number 
        of propertes per request (close to 300)
        
        """
    
        payload = {'price_min':min,'price_max':max}
        
        data = self.getJson(payload)
        
        number = self.getNumberProp(data)        
        
        if isinstance(number,type(None)):
            return min,max,0
        
        if max_p == None:                                    
            delta = int((max-min)//2)
            if number  <= 300:
                return min,max,number
        else: 
            delta = int(math.fabs(max - max_p)//2)                               
        
        if delta > 0:
            if number > 300:
                min,max,number = self.getPriceRange(min,max-delta,max)
            elif (300 - number) > 10:
                min,max,number = self.getPriceRange(min,max+delta,max)
            else:
                return min,max,number                    
        else:
            if number > 300:
                min,max,number = self.getPriceRange(min,max-1,max)

        print(min,max,number)
        return min,max,number
    
    def getPriceRangeWrapper(self):
        
        """
        the function makes the list of price ranges(tuples) from 0 to the 
        maxumum price (10000USD) exising to include the maximum amount of properties in 
        each range
        
        """
        
        price_ranges = {}
        histogram = [{'number of properties':0,'minimum_price':0,'maximum_price':0}]
        min = 0
        max = 2000
            
        while min < max:
            
            min_max = self.getPriceRange(min,max)
            price_ranges['number of properties'] = min_max[2]
            price_ranges['minimum_price'] = min_max[0]
            price_ranges['maximum_price'] = min_max[1]
            histogram.append(price_ranges)
            min = min_max[1] + 1
            price_ranges = {}
            print(histogram)
  
        ##cover the properries which prices higher than 2000USD per night
        min_max = self.getPriceRange(min,10000)
        price_ranges['number of properties'] = min_max[2]
        price_ranges['minimum_price'] = min_max[0]
        price_ranges['maximum_price'] = min_max[1]
        histogram.append(price_ranges)
        
        return histogram
        
    def parserHelper(self,data,*args):

        """
        special helper functons which returns None value if it can't find the dict key 
        and returns the value of that key if the key exist (helps to avoid errors while parsing
        pages where some dict keys can be missing for some properties)
        
        """
                
        if args and data:
            element  = args[0]

            if isinstance(element,str):                
                value = data.get(element)
            else:
                value = data[element]                

            return value if len(args) == 1 else self.parserHelper(value, *args[1:])
        else:
            return None

    def parsePage(self,data):
        
        """
        gets dict/list of data (just a single page) and returns a list 
        of properties with relevant info on them
        
        """
        property_list = [{'id':0,'name':0,'dprice':0,'currency':0,'nreviews':0,\
        'area':0,'subdistrict':0,'lats':0,'lon':0,'nbedrooms':0,'max_guests':0,'url':0,\
        'instant_booking':0,'monthly_price_f':0,'weekly_price_f':0,'is_superhost':0,\
        'picture_count':0,'host_lang':0,'host_picture':0,'review_score':0,\
        'picture_colour':0,'privacy_type':0,'property type':0,'extra info':0}]
    
        data_s = self.parserHelper(data,'explore_tabs',0,'sections',0,'listings')
            
        if isinstance(data_s,type(None)): #returns empty list if the server response was empty
            numb_prop = 0
            error_message = "Can't retreive the data from the request (probably the response from the server was empty. URL -> {url}".format(url = self.url)
            text_file = self.createTextFile (error_message,'errors.txt')
            self.file_uploadGDrive(text_file)            
            
        else:            
            for i in range(len(data_s)):
                
                property = {}            
                
                property['id'] = self.parserHelper(data_s,i,'listing','id')
                property['name'] = self.parserHelper(data_s,i,'listing','name')
                property['dprice'] = self.parserHelper(data_s,i,'pricing_quote','rate','amount')
                property['currency'] = self.parserHelper(data_s,i,'pricing_quote','rate','currency')
                property['nreviews'] = self.parserHelper(data_s,i,'listing','reviews_count')
                property['area'] = self.parserHelper(data_s,i,'listing','city') 
                property['subdistrict'] = self.parserHelper(data_s,i,'listing','public_address')
                property['lats'] = str(self.parserHelper(data_s,i,'listing','lat'))
                property['lon'] = str(self.parserHelper(data_s,i,'listing','lng'))
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
                property['privacy_type'] = self.parserHelper(data_s,i,'listing','room_type_category')
                property['property type'] = self.parserHelper(data_s,i,'listing','space_type')
                property['extra info'] = ''            
    
                property_list.append(property)  
                numb_prop = len(data_s)

        return property_list,numb_prop
        
    def parsePageProperty(self,data):
        
        """
        gets a dict of data from Airbnb API and returns 
        info about availability and prices for selected period
        
        """
        
        property_calendar = {}        
        
        for month in range (0,11):                
    
            data_s = self.parserHelper(data,'calendar_months',month,'days')

            if data_s == 'no data':
                property_calendar['picture_colour'] = 'no calendar data for the property'

            else:                
                property_calendar['date_collected_at'] = self.parserHelper(data,'calendar_months',0,'dynamic_pricing_updated_at')            
                for i in range(len(data_s)):                                    
                    if self.parserHelper(data_s,i,'available'):
                        date = self.parserHelper(data_s,i,'date')             
                        price = self.parserHelper(data_s,i,'price','local_price')
                        min_nights = self.parserHelper(data_s,i,'min_nights')
                        max_nights = self.parserHelper(data_s,i,'max_nights')
                        price_method = self.parserHelper(data_s,i,'price','type')                                        
                       
                        property_calendar[date] = price
                        property_calendar['min_nights'] = min_nights
                        property_calendar['max_nights'] = max_nights
                        property_calendar['price_method'] = price_method
        
                    else:
                        date = self.parserHelper(data_s,i,'date')
                        property_calendar[date] = 'n/a'
                                        
        return property_calendar
                        