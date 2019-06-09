#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby

"""

from Airbnb_Spyder import Airbnb_spyder
from Spyder import Spyder
import pandas as pd
#from URLs import URLs
from datetime import datetime

    
"""
Schedule:
    
1) collect price_ranges - weekly
2) collect db - weekly
3) collect calendar - daily/different module


Сделать загрузку файла ошибок и добавление новых данных
client session id убрать из запросов
сделать файл с отчетом и отсылку на емаэл в случае глобальной ошибки
добавить счетчики 
текстовый файл загрузка в папку
переделать запись в HDF

"""

def scheduleRun():
     
    day = datetime.isoweekday(Spyder().today)
    today = datetime.isocalendar(Spyder().today)
    #print (today)
    
    #reading the list of URL to parse from GD
    file_URL = Spyder().fileDownloadGdrive('URL_list_ABNB')
    URLs = pd.read_excel(file_URL,sheet = 'Bali',index_col = 0)

    for URL in URLs.index[:1]:
        ms = Airbnb_spyder(URLs.URL[URL].strip('﻿'))
        ptype = URLs.TYPE[URL]
        columns = ['Date','P_type','N_collected','New_properties',
                   'Properties_disposed','Errors_URL','Errors_JSON']
        ms.stats = pd.DataFrame(columns = columns)
#        ms.stats.append({'Date':today,'P_type':ptype},ignore_index = True)
#        print (ms.stats)    
        if day == 7:
            #collect price histogram
            histogram = ms.collectNumberProp(ptype)        
       
        #collect property db   
        hist_file = ms.fileDownloadGdrive('{ptype}_histogram'.format(ptype=ptype))
        histogram = pd.read_csv(hist_file)
        ms.collect_db(ptype,histogram)


    return None

def collectHistogram():
    
    file_URL = Spyder().fileDownloadGdrive('URL_list_ABNB')
    URLs = pd.read_excel(file_URL,sheet = 'Bali',index_col = 0)

    
    for URL in URLs.index[:1]:
        ms = Airbnb_spyder(URLs.URL[URL].strip('﻿'))
        ptype = URLs.TYPE[URL]
        histogram = ms.collectNumberProp(ptype)        

    return histogram
    


#scheduleRun()
collectHistogram()
    



#histogram = [{'number of properties':0,'minimum_price':10,'maximum_price':10}]
#collect_db(my_spyder.url,url['type'],histogram)
#shared_prop_hist = [372,346,442,1184,1358,1959,2103,1929,1398,1095,919,820,614,543,582,611,406,356,329,259,255,144,149,80,111,82,82,97,47,41,55,32,39,32,23,28,21,17,22,10,9,11,6,11,15,15,6,3,4,80]