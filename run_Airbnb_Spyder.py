#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby

"""

from Airbnb_Spyder import Airbnb_spyder
from URLs import URLs
from datetime import datetime

def collectNumberProp(url):
    
    histogram = my_spyder.getPriceRangeWrapper()
    print (histogram)
    #saving data
    xl_file = my_spyder.save_data(histogram,'excel','histogram_', 'Airbnb_data')
    my_spyder.file_uploadGDrive(xl_file)
    csv_file = my_spyder.save_data(histogram,'csv','histogram_', 'Airbnb_data')
    my_spyder.file_uploadGDrive(csv_file)
        
    return histogram

def collect_db(url,type,price_ranges = None):
    
    property_list = []
    histogram = []
    hist = {}
    total = 0
    
    for price in price_ranges:
        hist = {}
        number_t = 0
        number = 0
        ofs = 0
        last_page_flag = True
        
        while last_page_flag:        
#            print (price['maximum_price'])
            payload = {'price_min':price['minimum_price'],'price_max':price['maximum_price'],'items_offset':ofs}            
            data = my_spyder.getJson(payload)
            processed_data = my_spyder.parsePage(data)
            property_list.extend(processed_data[0])
            number = processed_data[1]            
            print('URL requested for prices from ' + str(price['minimum_price']) + ' until ' + str(price['maximum_price']))
            print('Got info for ' + str(number) + ' properties.')             
            ofs +=50
            last_page_flag = my_spyder.parserHelper(data,'explore_tabs',0,'pagination_metadata','has_next_page')   
            number_t += number
            total += number_t

        hist[number_t] = (price['minimum_price'],price['maximum_price'])
        histogram.append(hist)
   
        
    xl_file = my_spyder.save_data(property_list,'excel', '{type}_'.format(type = type), 'Airbnb_data')
    my_spyder.file_uploadGDrive(xl_file)
    csv_file = my_spyder.save_data(property_list,'csv','{type}_'.format(type = type),'Airbnb_data')
    my_spyder.file_uploadGDrive(csv_file)
            
    print (histogram)
    print('total number of properties -->'+str(total))
    txt_file = my_spyder.createTextFile ((histogram,str('total number of properties -->')+str(total)),'Parsed properties.txt')        
    my_spyder.file_uploadGDrive(txt_file)

    return None

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

    
"""
Schedule:
    
1) collect price_ranges - weekly
2) collect db - weekly
3) collect calendar - daily

Сделать имя в файле гистограмму     
Счетчик объектов неправильно работает
сделать загрузки в папки по дням
Добавить все прочие объекты
Сделать загрузку файла ошибок и добавление новых данных
    
"""

def scheduleRun(day,type):
              
#    if day == 6:
#        #collect price histogram
#        histogram = collectNumberProp(URLs[0])        
#
#    elif day == 7:
#        file_name = my_spyder.fileDownloadGdrive('histogram')
#        histogram = my_spyder.get_data_from_file(file_name)
#        collect_db(my_spyder.url,type,histogram)
#
#    elif day in [1,2,3,4,5,6,7]:
#        k = 1
#        print (k)        
#        #makeCalendarAvail()


    histogram = collectNumberProp(URLs[0])        
    file_name = my_spyder.fileDownloadGdrive('histogram')
    histogram = my_spyder.get_data_from_file(file_name)
    collect_db(my_spyder.url,type,histogram)

    return None

day = datetime.isoweekday(datetime.today())
for url in URLs:

    my_spyder = Airbnb_spyder(url['url'])
    scheduleRun(day,url['type'])
    
#my_spyder = Airbnb_spyder('http://booking.com')
#URLs = [my_spyder.url,1]
#scheduleRun(1,'villas')
