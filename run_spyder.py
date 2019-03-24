#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 21:13:18 2019

@author: moby
"""

from spyder_booking_com import Booking_com_spyder
import math
#from bs4 import BeautifulSoup

def cont_flag_set(value):
   
    global cont_flag
    cont_flag = value

            
def run_price_avail_analysis(city, accomodation_type, period, length_stay):

    #returns list of dict containing:
    #1) date 
    #2) average_price for that date
    #3) availability in the area for that date        
    
    main_db = []
    
    main_url = 'https://www.booking.com/searchresults.en-gb.html? \
    &dest_id=835&dest_type=region&group_adults=2&no_rooms=1\
    &raw_dest_type=region'
    
    my_spyder = Booking_com_spyder(main_url)    

    if cont_flag:                        
            booking_dates = my_spyder.get_data_from_file('booking_dates{param1}.csv'.format(param1 = my_spyder.today))
            main_db = my_spyder.get_data_from_file('main_db_temp{param1}.csv'.format(param1 = my_spyder.today))
            print('Continue to crawl pages from the dates '+str((booking_dates[0]['checkin'], booking_dates[1]['checkin'])))
#        except IndexError:
#            print("We couldn't retrive the info from the file with dates (prbably its empty). Lets just start from the beggining")
#            booking_dates = my_spyder.booking_dates(period,length_stay)
#            cont_flag_set(False)

    else:
        booking_dates = my_spyder.booking_dates(period,length_stay)
    
    try:                    
        for date in booking_dates:
            dates = (date['checkin'],date['checkout'])
            print('')
            print('Starting to parse pages')
            print ('Checkin/out dates = ' + str(dates))                        
            urls,first_page,avail = my_spyder.make_url_list_prices_trend\
            (city,accomodation_type,dates,2,3)               
            property_list, properties_number = my_spyder.parse_price_avail(first_page)
            p_n_total = properties_number        
            print('Parsed:')
            print(str('1 page. '+'Got info for '+str(p_n_total)+' properties.'))     
                            
            for url in urls[1:]:                
                page = my_spyder.get_script2(my_spyder.get_r(url['url']))   
                
#                with open ('html_page.html','w') as file:
#                    file.write(str(page.prettify()))
                                    
                property_list2, properties_number = my_spyder.parse_price_avail(page)                
                print ('Parsed:')                                        
                p_n_total += properties_number
                print(str(urls.index(url)+1)+' pages. '+'Got info for '+str(p_n_total)+' properties.')     
                property_list.extend(property_list2)         
            
            for property in property_list:               
                property['date'] = dates[0] #appending each property record with dates
            print ('For checkin dates ' + str(dates)+' collected info for '+str(p_n_total)+' properties')   
                                                                    
            if p_n_total == 0 or math.fabs(p_n_total - avail) > 5:            
                    print ('Number of parsed properties is not equal to the total available propertes')
                    print ('Number of pp =' + str(p_n_total))
                    print ('Available in ' + str(city) + ' = ' + str(avail))
                    raise Exception            
                        
            main_db.extend(property_list) #main file where each line is property min pricerinfo for a particular date 
            cont_flag_set(False)
            dates_remain = my_spyder.cleanup_dates()
            print('')
            print('Dates remain to scrape '+str(len(dates_remain)))
            
            
        print('JOB DONE')                    

        my_spyder.save_data(main_db,'excel','price_avail_check_{param1}_'.\
                           format(param1 = main_db[0]['city']),'Booking_com')

        my_spyder.save_data(main_db,'csv','price_avail_check_{param1}_'.\
                           format(param1 = main_db[0]['city']),'Booking_com')
        
        my_spyder.save_data(booking_dates,'csv','checkin_dates_{param1}_'.\
                            format(param1 = main_db[0]['city']),'Booking_com')
    
               
    except:            
        if cont_flag ==True:
            print ("Something went wrong.\
                   Please debug the code and save main_db_temp file first")
        else:        
            my_spyder.save_data(main_db,'csv','main_db_temp')
            print("Something went wrong. Intermidiate results have been saved.")        
        
        cont_flag_set(True)
                
    return main_db,booking_dates
    

def maximum_avail_check(min,max):
#    avail = []
#    for i in range (min,max):        
#        a,b = run_price_avail_analysis('Seminyak', 'Villas',1, i)
#        for item in a:
##            item[]
#        
#            avail.append(d)
#            #some code following
    pass


#### 1. COLLECT THE INFO  ######    
 
main_url = 'https://www.booking.com/searchresults.en-gb.html? \
&dest_id=835&dest_type=region&group_adults=2&no_rooms=1&raw_dest_type=region'            
my_spyder = Booking_com_spyder(main_url)

#parameters 
#1) city
#2) accomodation_type
#3) period
#4) length_stay

city = 'Seminyak'
type = 'Villas'
number_of_days_to_check = 10
duration_of_stay = 2
#
#cont_flag = my_spyder.get_bool('Please enter True (continue the process) or False (start from the begining) \n')
#
#if isinstance(cont_flag,(bool)):
#    if cont_flag:
#        print('The spyder will continue from the last stop. Are you sure? \n')
#        conf = input('y/n? \n')
#        if conf =='y':
#            a,b = run_price_avail_analysis(city,type,number_of_days_to_check,duration_of_stay)                
#        else:
#            print('Spyder stopped')
#    if cont_flag == False:
#        print('The spyder will continue from the beggining . Are you sure? \n')
#        conf = input('y/n? \n')
#        if conf =='y':
#            a,b = run_price_avail_analysis(city,type,number_of_days_to_check,duration_of_stay)
#        else: 
#            print('Spyder stopped')               
#else:
#    print('Please enter a correct value and start again')
#


#### 2.ANALYSE THE INFO
    

file_name = 'price_avail_check_Seminyak_2019-03-16.csv'
data = my_spyder.get_data_from_file(file_name)
print(data[1])
file_name2 = 'booking_dates2019-03-15.csv'
dates = my_spyder.booking_dates(number_of_days_to_check,duration_of_stay)
a1,b1,c1,d1 = my_spyder.occupancy_calc(data,dates)
print ('average occupancy = '+str(b1),'\naverage availabilty = '+str(c1),'\ntotal availabilty = '+str(d1))

a,b = my_spyder.calc_av_median(a1,dates)
print('Average prices for diff price groups ->',b)








'''''''''''''''''
Улучшалки:

1) Для списка кодов по фильтрам лучше сделать отдельную функцию которая будет 
    брать их из файла и если его нет то делать запрос к серверу и обновлять его.
    Как в данном случае работать с версиями файлов - например, если файл старый 
    и возможно ли проверить его версию и в зависимости от этого делать новый запрос.
2) Такая же ситуация с тегами для поиска данных - как запилить их в отдельный файл 
    и брать оттуда.
5) Сделать проверочную функцию на выходящие данные - те если 'no data' то чтобы было предупреждение  

        

    
4) параметры в момент ввода (может создать файл с требованиями)
5) заточить под airbnb
6) повесить на сеть??
7) в поля добавить адрес объекта, airport shuttle разбивку по странам сколько людей смотрит данный район 
10) тип комнат и цены по отдельным объектам (может только виллы?)
11) политику отмен по отдельным объектам
14) какой минимальный stay??
15) условия бронирования
16) какие дисконты?
16) как сделать с прокси?
20) как сделать загрузку на гугл драйв опциональной
21) гугл драйв требует подтверждения всегда    
22) добавить дату в поля
    
    
    для параметров
    
    район
    даты
    валюта
    сколько страниц качать
    
    
Сбор доп данных

2) Популярность разных дат (возможно сделать список вилл по которым пробить)
3) Ценник на разные даты (может сделать гистограмму и посмотреть по каким ценам сдается большинство и какова средняя)


    
    
    
    
'''''''''''''''''


###############
###CODE TESTING
###############
#

#main_url = 'https://www.booking.com/searchresults.en-gb.html? &dest_id=835&dest_type=region&group_adults=2&no_rooms=1&raw_dest_type=region'

##### 1) Make list of pages to parse
#################################
#
#my_spyder = Booking_com_spyder(main_url)
##FTF_codes,FTF_names,FTF_numbers = my_spyder.get_name_filters("uf")
##urls = my_spyder.make_url_list(FTF_codes,FTF_names)
###print (urls)
#
##### 2) Save data to file
#################################
#
##urls = [{'rt':1,'ee':2},{'rt':6,'ee':4}]
#
##print(my_spyder.self.data)
##file_name = my_spyder.save_data(urls, "excel", 'urls_to_parse','URL')
##file_name = my_spyder.save_data(urls, "csv", 'urls_to_parse','URL')
#
##### 3) Process pages and get the final data
##############################################
#
#file_name = 'urls_to_parse2019-03-06.csv'
#urls = my_spyder.get_data_from_file(file_name)
#properties_db = my_spyder.collect_data(urls)
#my_spyder.save_data(properties_db,'excel','properties_in_Bali_', 'Booking_com')
#



