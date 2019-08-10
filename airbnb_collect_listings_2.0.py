#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby

"""

"""
в гистограмме сделать диапазоные непрерывающимися
класс для подсоюдинения к СУБД

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
    ptypes = collection.find_one()['url_ptype3']
    
    #find the latest histogram/scrap_date
    scrap_date = db.histogram.find({'ptype':'OTHER'}).\
        sort('scrap_date',-1)[0]['scrap_date']
    print (scrap_date)
    

    #collect listings data for each property type
    for ptype in ptypes:
        ms = AS(ptypes[ptype].strip('﻿')) 
             
        #query for histogram      
        histogram_cursor  = db.histogram.find({'scrap_date':scrap_date,
                                                  'parsed':False,
                                                  'ptype':ptype})
    
        histogram = [h for h in histogram_cursor]
        if histogram == []:
            continue 
 
        #collect property db and real histogram
        scraping_results = ms.collect_db(ptype,histogram)                        

        listings = scraping_results[0]        
        for l in listings:
            scraping_date = ms.today.strftime('%Y-%m-%d')
            l['scraping_date'] = scraping_date
            l['ptype'] = ptype
        
        hist_actual = scraping_results[1]        
        for h in hist_actual:
            h['ptype'] = ptype
            
        #upload to the server
        try:
            db.listings.insert_many(listings,ordered = False)
        except BulkWriteError as e:
            print('Error name\n'+str(e.__class__))

        #updating histogram collection on the server
        for raw in hist_actual:                    
            db.histogram.find_one_and_update(
                    {'minimum_price':raw['minimum_price'],
                     'ptype':ptype,
                     'scrap_date':scrap_date},
                    {'$set': 
                            {'n_actual':raw['n_properties'],
                             'parsed':True}})                
                                
    #clean histogram and listings                                                               
    db.histogram.update_many(
                    {'scrap_date':scrap_date},
                    {'$set': 
                            {'parsed':False}})   

    db.listings.update_many(
                            {'scrap_date': {'$lt':scraping_date}},
                            {'$set': {'update_status': 'old'}},
                            upsert = True)                       
    
    db.listings.update_many(
                            {'scrap_date': scraping_date},
                            {'$set': {'update_status': 'last'}},
                            upsert = True)                       
    
    
    return print('Job done')


def collectHistogram():
    """
    calculate price ranges to get the number of properties in each close 
    to 300 or actual    
    """

    #load url list to parse    
    ptypes = db['VARIABLES'].find_one()['url_ptype3']
        
    #check the latest date when histogram was reloaded (only the last ptype 
    #to make sure the db is full) 
    try:
        l_scrap_date = db.histogram.find({'ptype':'OTHER'}).\
                sort('scrap_date',-1)[0]['scrap_date']
    except IndexError:
        l_scrap_date = '1900-01-01'
            
    db.histogram.delete_many({'scrap_date':
                                           {'$gt':l_scrap_date}})
    dt_scrap_date = datetime.strptime(l_scrap_date,'%Y-%m-%d').date()    
    
    #collect price ranges         
    for ptype in ptypes:
        ms = AS(ptypes[ptype].strip('﻿')) 
        if (ms.today - dt_scrap_date).days < 7:
            print('histogram db still up-to-date (from {d}), continue \n\
                  with collecting listing db'.format(d = l_scrap_date))
            return None
        print('ptype\n'+str(ptype))
        print('histogram scrapping_date\n'+ms.today.strftime('%Y-%m-%d'))
        histogram = ms.getPriceRangeWrapper()
        for p_range in histogram:
            p_range['ptype'] = ptype
            p_range['scrap_date'] = ms.today.strftime('%Y-%m-%d')
            p_range['parsed'] = False

        #upload to the server 
        db.histogram.insert_many(histogram)
        
    #mark the newest histogram
    db.histogram.update_many(
                            {'scrap_date': {'$lte':l_scrap_date}},
                            {'$set': {'update_status': 'old'}},
                            upsert = True)

    db.histogram.update_many(
                            {'scrap_date': {'$gt':l_scrap_date}},
                            {'$set': {'update_status': 'last'}},
                            upsert = True)        
                         
    return None    


collectHistogram()
#collectDb()


