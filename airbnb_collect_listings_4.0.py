#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby

"""

"""
в гистограмме сделать диапазоные непрерывающимися

"""

from Airbnb_Spyder import Airbnb_spyder as AS
#from Airbnb_Spyder import db
from datetime import datetime
from pymongo import MongoClient,GEOSPHERE
from pymongo.errors import BulkWriteError

MC_l = MongoClient('mongodb+srv://moby:7IOMu3Xt8EWoabiU@test-cluster-khino.gcp.mongodb.net/test?retryWrites=true&w=majority')
db = MC_l['airbnb_test']

def collectHistogram(h_scrap_date):
    """
    calculate price ranges to get the number of properties in each close 
    to 300 or actual    
    """

    #load url list to parse    
    ptypes = db.VARIABLES.find_one()['url_ptype3']        
    
    #collect price ranges         
    for ptype in ptypes:
        ms = AS(ptypes[ptype].strip('﻿')) 
        
        print('ptype\n'+str(ptype))
        print('histogram scraping_date now\n'+ms.today.strftime('%Y-%m-%d'))
        histogram = ms.getPriceRangeWrapper()
        for p_range in histogram:
            p_range['ptype'] = ptype
            p_range['parsed'] = False

        #upload to the server 
        db.histogram.insert_many(histogram)
    
    #mark the histogram update date
    db.histogram.update_many(
                            {'scrap_date': {'$exists':False}},
                            {'$set':
                                    {'scrap_date':ms.today.strftime('%Y-%m-%d')}},
                            upsert = True)
      
    #mark the newest histogram
    db.histogram.update_many(
                            {'scrap_date': {'$lte':h_scrap_date}},
                            {'$set': {'update_status': 'old'}},
                            upsert = True)

    db.histogram.update_many(
                            {'scrap_date': {'$gt':h_scrap_date}},
                            {'$set': {'update_status': 'last'}},
                            upsert = True)        
                         
    return None    

   
def collectDb():
    """
    collects and uploads to the server "listings" data
    requests to Airbnb made for each price range (~300 properties per one request)
    
    property_types (collected separately):
    1) ENTIREHomeVILLAS - Villas only
    2) EntireHomeNONVILLAS - all private properties except Villas
    3) OTHER - other non-private properties        
    
    """   
    #interval to collect listings db    
    ldb_interval = 7

    #check the latest date when listings db was collected and decide if new collection is needed    
    try:
        l_scrap_date = db.listings.find({'ptype':'OTHER',
                                         'update_status':'last'}).\
                sort('scraping_date',-1)[0]['scraping_date']        

    except (IndexError,KeyError):
        l_scrap_date = '1900-01-01'

    dt_scrap_date = datetime.strptime(l_scrap_date,'%Y-%m-%d').date()
        
    ms = AS('url')         
    if (ms.today - dt_scrap_date).days < ldb_interval:
        print('listings db still up-to-date (from {d})'.format(d = l_scrap_date))
        return None
    
    ##below part of the code is only executed if listings db is too old
    #archive the old db
    if l_scrap_date!='1900-01-01':
        db.listings.update_many(
                            {'scraping_date': {'$lte':l_scrap_date}},
                            {'$set': {'update_status': 'old'}},
                            upsert = True)       
        db.listings.rename('listings_{date}'.format(date = l_scrap_date))

    #find the latest histogram/scrap_date            
    try:
        h_scrap_date = db.histogram.find({'ptype':'OTHER'}).\
            sort('scrap_date',-1)[0]['scrap_date']
        print ('histogram last scraping date --> '+str(h_scrap_date))
    
        dt_h_scrap_date = datetime.strptime(h_scrap_date,'%Y-%m-%d').date()
     
        if (ms.today - dt_h_scrap_date).days < (ldb_interval+13):
            print('histogram db still up-to-date (from {d}), continue \n\
                  with collecting listing db'.format(d = l_scrap_date))              
        else:
            collectHistogram(h_scrap_date)
            return None
    
    except (IndexError,KeyError):
        print ('No histogram to use. Collecting the new one')
        collectHistogram(h_scrap_date = '1990-12-01') 
        return None

    #load ptypes array
    ptypes = db.VARIABLES.find_one()['url_ptype3']                        

    #collect listings data for each property type
    for ptype in ptypes:
        ms = AS(ptypes[ptype].strip('﻿'))             
             
        #query for histogram      
        histogram_cursor  = db.histogram.find({'scrap_date':h_scrap_date,
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
                     'scrap_date':h_scrap_date},
                    {'$set': 
                            {'n_actual':raw['n_properties'],
                             'parsed':True}})
    #make geo index
    db.listings.create_index([("geo", GEOSPHERE)])
                                
    #clean histogram and listings                                                               
    db.histogram.update_many(
                    {'scrap_date':h_scrap_date},       
                    {'$set': 
                            {'parsed':False}})   
                    
    db.listings.update_many(
                            {'scraping_date':{'$gt':l_scrap_date}},
                            {'$set': 
                                {'update_status':'last',
                                 'cal_collected':'no',
                                 'reviews_col':'no',
                                 'scraping_date':scraping_date}},
                            upsert = True)                                   
  
    
    return print('Job done')


collectDb()


