#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 14:28:11 2019

@author: moby
"""

"""
1) добавить в базу время scraping
2) тип объекта
3) cделать класс подключений в MongoDb

"""
#Доделки

"""

    полная цена и ее разбивка
    куда то пропадают картинки с виллой из базы
    проверить ли есть там дома из категоии +
    добавить прогресс по скачиванию
    для ошибочных объектов запустить повторную проверку
    
"""

from Airbnb_Spyder import Airbnb_spyder as AS
from Airbnb_Spyder import db
from Spyder import Spyder

def makeCalendarAvail(area_db = None, ptype = None, length = 351):    
    """    
    gets index of id of properties to collect the calendar
    upload calendar values into MongoDb
    """           
    #create Spyder instance
    S = Spyder()

    #record the starting point of the Spyder
    start = Spyder().now
  
    #download variables (URLS)
    url_calendar = db.VARIABLES.find_one()['url_calendar1']
    url_reviews = db.VARIABLES.find_one()['url_reviews']
    
    #find the latest listings db to parse
    try:
        l = db.listings.find({'update_status':'last',
                              'cal_collected':'no'})
        
    except (IndexError,KeyError):
         print ('No listigns db to parse. Please run airbnb_collect_listings spyder')
         
    l = [l for l in l]
    scraping_date = S.today.strftime('%Y-%m-%d')
                   
    for listing in l[:10]:
        id = listing['_id']
        url_calendar = url_calendar.format(property_id = id, year = S.year, month = S.month)
        ms = AS(url_calendar)

        #collect calendar
        data_cal = ms.getJson(check_calc = True) 
        calendar = {}
        calendar['_id'] = id
        calendar['url'] = 'https://www.airbnb.com/rooms/{}'.format(id)
        calendar.update(ms.parsePageProperty(data_cal))
        ms.uploadMDB(calendar,'calendar_{}'.format(scraping_date))
                   
        #collect reviews
        ms = AS(url_reviews.format(id = id))
        data_reviews = ms.getJson()
        reviews = {}
        reviews['_id'] = id
        reviews['reviews'] = ms.parserHelper(data_reviews,'reviews')
        reviews['reviews_count'] = ms.parserHelper(data_reviews,'metadata','reviews_count')                       
        db.listings.update_one({'_id':id},
                               {'$set':
                                   {'reviews':reviews['reviews'],
                                       'reviews_count':reviews['reviews_count']}},
                                upsert = True)            
            
        #cleaning
        db.listings.update_one({'_id':id},
                               {'$set':
                                   {'cal_collected':'yes'}},
                                       upsert = True)        
        
        #print status of scraping
        print ('Current bunch:')
        print ('Checked '+str(l[:1000].index(listing)+1)+' out of '+'1000 properties to check in the current round.')
        print ('Total:')            
        print ('Checked '+str(l.index(listing)+1)+' out of '+str(len(l))+' properties to check.')
        print ('Left '+str(len(l) - l.index(listing)-1)+' properties to check.')        
        
    end = Spyder().now
    
    #update statistic about the timing
    l_count = db.listings.count_documents({'update_status':'last',
                      'cal_collected':'yes'})
    stat = {'scraping_date_cal':scraping_date,
            'starting_time':start,
            'ending_time':end,
            'total_time':str(int(((end - start).seconds)//60))+' min',
            'properties_parsed':l_count}    

    ms.uploadMDB(stat,'stat_cal')
                                 
    return None    

makeCalendarAvail()
    


