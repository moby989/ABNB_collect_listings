#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby

"""

from Airbnb_Spyder import Airbnb_spyder
from URLs import URLs
from datetime import datetime

def collectNumberProp():
    
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
            property_list.extend(processed_data[0][1:])
            number = processed_data[1]            
            print('URL requested for prices from ' + str(price['minimum_price']) + ' until ' + str(price['maximum_price']))
            print('Got info for ' + str(number) + ' properties.')             
            ofs +=50
            last_page_flag = my_spyder.parserHelper(data,'explore_tabs',0,'pagination_metadata','has_next_page')   
            number_t += number
        
        total += number_t

        hist[number_t] = (price['minimum_price'],price['maximum_price'])
        histogram.append(hist)
   
    property_list.insert(0,processed_data[0][0])
#    print (property_list[0])
    xl_file = my_spyder.save_data(property_list,'excel', '{type}_'.format(type = type), 'Airbnb_data')
    my_spyder.file_uploadGDrive(xl_file)
    csv_file = my_spyder.save_data(property_list,'csv','{type}_'.format(type = type),'Airbnb_data')
    my_spyder.file_uploadGDrive(csv_file)
            
    print (histogram)
    print('total number of properties -->'+str(total))
    txt_file = my_spyder.createTextFile ((histogram,str('total number of properties -->')+str(total)),'Parsed properties.txt')        
    my_spyder.file_uploadGDrive(txt_file)

    return None



    
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
client session id убрать из запросов

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


    histogram = collectNumberProp()        
    file_name = my_spyder.fileDownloadGdrive('histogram')
    histogram = my_spyder.get_data_from_file(file_name)
    collect_db(my_spyder.url,type,histogram)

    return None

day = datetime.isoweekday(datetime.today())
#for url in URLs[:1]:
url = {'type':'private_room', 'url': 'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=2&allow_override%5B%5D=&auto_ib=false&checkin=2019-05-30&checkout=2019-06-02&children=0 &currency=USD&experiences_per_grid=20&fetch_filters=true&guests=2&guidebooks_per_grid=20&has_zero_guest_treatment=true&ib=true&infants=1&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&map_toggle=false&metadata_only=false&place_id=ChIJyY4rtGcX2jERIKTarqz3AAQ&query=Singapore&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&room_types%5B%5D=Private%20room&s_tag=SMrEDHBi&satori_version=1.1.0&screen_height=721&screen_size=small&screen_width=611&search_type=FILTER_CHANGE&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&toddlers=0&version=1.4.8'}    
my_spyder = Airbnb_spyder(url['url'])
#    my_spyder = Airbnb_spyder('http://book22ing.com')
scheduleRun(day,url['type'])
    
#my_spyder = Airbnb_spyder('http://booking.com')
#URLs = [my_spyder.url,1]
#scheduleRun(1,'villas')

#my_spyder = Airbnb_spyder(url['url'])



#histogram = [{'number of properties':0,'minimum_price':10,'maximum_price':10}]
#collect_db(my_spyder.url,url['type'],histogram)
#shared_prop_hist = [372,346,442,1184,1358,1959,2103,1929,1398,1095,919,820,614,543,582,611,406,356,329,259,255,144,149,80,111,82,82,97,47,41,55,32,39,32,23,28,21,17,22,10,9,11,6,11,15,15,6,3,4,80]