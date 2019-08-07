#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby

"""

"""
добавить дату скрейпинга в листинг объектов
"""

from Airbnb_Spyder import Airbnb_spyder as AS
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

    
#initialise Mongodb
client = MongoClient('mongodb+srv://moby:bodgyw-mEppu2-kedmof@test-cluster-khino.gcp.mongodb.net/test?retryWrites=true&w=majority')
db = client['airbnb_test']
    
def collectDb(db = db):
    """
    collects and uploads to the server "listings" data
    requests to Airbnb made for each price range (~300 properties per one request)
    
    property_types (collected separately):
    1) ENTIREHomeVILLAS - Villas only
    2) EntireHomeNONVILLAS - all private properties except Villas
    3) OTHER - other non-private properties        
    
    """   
    #load variables (URLs)
    collection = db.VARIABLES            
    ptypes = collection.find_one()['url_ptype2']
    
    #find the latest histogram/scrap_date
    collection_hist = db.histogram
    scrap_date = collection_hist.find().sort('scrap_date',-1)[0]['scrap_date']
    print (scrap_date)
    

    #collect listings data for each property type
    for ptype in ptypes:
        ms = AS(ptypes[ptype].strip('﻿')) 
             
        #query for histogram
       
        histogram_cursor  = collection_hist.find({'scrap_date':scrap_date,
                                                  'parsed':False,
                                                  'ptype':ptype})

        histogram = [h for h in histogram_cursor]

        #collect property db and real histogram
        scraping_results = ms.collect_db(ptype,histogram)

        listings = scraping_results[0]        
        for l in listings:
            l['scraping_date'] = ms.today.strftime('%Y-%m-%d')
        
        hist_actual = scraping_results[1]        
        for h in hist_actual:
            h['ptype'] = ptype
            
        #upload to the server
        collection_listings = db.listings
        try:
            collection_listings.insert_many(listings,ordered = False)
        except BulkWriteError as e:
            print('Error name\n'+str(e.__class__))

        #updating histogram collection on the server
        for raw in hist_actual:                    
            collection_hist.find_one_and_update(
                    {'minimum_price':raw['minimum_price'],
                     'ptype':ptype},
                    {'$set': 
                            {'n_actual':raw['n_properties'],
                             'parsed':True}}
                                            )
    #clean histogram                                                                
    collection_hist.update_many(
                    {'scrap_date':scrap_date},
                    {'$set': 
                            {'parsed':False}})     
        
    #update listings
    collection_listings.update_many(
                    {'scrap_date':scrap_date},
                    {'$set': 
                            {'timestamp':ms.today}}) 
        
    return print('Job done')


def collectHistogram():
    """
    calculate price ranges to get the number of properties in each close 
    to 300 or actual    
    """

    #load url list to parse    
    collection = db['VARIABLES']
    
    #return collection
    ptypes = collection.find_one()['url_ptype3']
    
    #check the latest date when histogram was reloaded    
    collection_hist = db.histogram
    l_scrap_date = collection_hist.find().sort('scrap_date',-1)[0]['scrap_date']
    l_scrap_date = datetime.strptime(l_scrap_date,'%Y-%m-%d').date()
         
    #collect price ranges         
    for ptype in ptypes:
        ms = AS(ptypes[ptype].strip('﻿')) 
        if (ms.today - l_scrap_date).days < 7:
            break
        print(ptype)
        histogram = ms.getPriceRangeWrapper()
        for p_range in histogram:
            p_range['ptype'] = ptype
            p_range['scrap_date'] = ms.today.strftime('%Y-%m-%d')
            p_range['parsed'] = False

        #upload to the server 
        db['histogram'].insert_many(histogram)
                         
    return None    


collectHistogram()
collectDb()

