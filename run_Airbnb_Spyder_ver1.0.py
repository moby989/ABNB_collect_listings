#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby

"""

from Airbnb_Spyder import Airbnb_spyder as AS
#from Spyder import Spyder as S
import pandas as pd
#from datetime import datetime
from pymongo import MongoClient

    
"""
Schedule:
    
1) collect price_ranges - weekly
2) collect db - weekly
3) collect calendar - daily/different module


client session id убрать из запросов
сделать файл с отчетом и отсылку на емаэл в случае глобальной ошибки
текстовый файл загрузка в папку
проверить почему в гнистограмму попадает нулевой диапазон цен


"""
client = MongoClient('mongodb+srv://moby:bodgyw-mEppu2-kedmof@test-cluster-khino.gcp.mongodb.net/test?retryWrites=true&w=majority')
db = client['airbnb_test']
    
def collectDb(scrap_date,db = db):
    """
    collects and uploads to the server "listings" data
    requests to Airbnb made for each price range (~300 properties per one request)
    
    """   
    #load variables
    collection = db.VARIABLES            
    ptypes = collection.find_one()['url_ptype']


    for ptype in ptypes:
        ms = AS(ptypes[ptype].strip('﻿')) 
             
        #query for histogram
        collection = db.histogram
        histogram_cursor  = collection.find({'scrap_date':scrap_date,
                                             'parsed':False})
        histogram = [h for h in histogram_cursor]   
#        print(histogram)                  

        #collect property db
        scraping_results = ms.collect_db(ptype,histogram)
        listings = scraping_results[0]
        
        hist_actual = scraping_results[1]
        for h in hist_actual:
            h['ptype'] = ptype
        print(hist_actual)
        
#        return (hist_actual)
    
        #upload to the server
        collection = db.listings
        collection.insert_many(listings)

        #updating histogram on the server
        collection = db.histogram
        for raw in hist_actual:                    
            collection.find_one_and_update(
                    {'minimum_price':raw['minimum_price'],'ptype':ptype},
                    {'$set': 
                            {'n_actual':raw['n_properties'],
                             'parsed':True                          }
                                                                     }
                                            )
        
    return print('Job done')


def collectHistogram():
    """
    calculate price ranges to get the number of properties in each close 
    to 300 or actual    
    """
    #load url list to parse    
    collection = db['VARIABLES']
    
    #return collection
    ptypes = collection.find_one()['url_ptype']
 
    #collect price ranges         
    for ptype in ptypes:
        ms = AS(ptypes[ptype].strip('﻿')) 
        histogram = ms.getPriceRangeWrapper()
        for p_range in histogram:
            p_range['ptype'] = ptype
            p_range['scrap_date'] = ms.today.strftime('%Y-%m-%d')
            p_range['parsed'] = False

        #upload to the server 
        db['histogram'].insert_many(histogram)
                         
    return None    

df = collectDb('2019-08-05')

#hist = collectHistogram()

