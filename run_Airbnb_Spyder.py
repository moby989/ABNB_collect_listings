#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby

"""

from Airbnb_Spyder import Airbnb_spyder
from Spyder import Spyder
import pandas as pd
#import numpy as np
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
текстовый файл загрузка в папку
переделать запись в HDF

"""
day = datetime.isoweekday(Spyder().today)
today = datetime.isocalendar(Spyder().today)
timestamp = datetime.today().strftime('%Y-%m-%d, %H:%M:%S')


def collectDb():
    """
    collect all properties available for pre-defined price ranges and all types
    returns a database WITHOUT calendar
    """   
    
    #reading the list of URL to parse from GD
    file_URL = Spyder().fileDownloadGdrive('URL_list_ABNB','URL_LIST')
    URLs = pd.read_excel(file_URL,index_col = 0)
    df_all = pd.DataFrame()
    hist_all = pd.DataFrame()
    ptype_df = []
    histogram_df=[]
    

    for URL in URLs.index:
        ms = Airbnb_spyder(URLs.URL[URL].strip('﻿'))
        ptype = URLs.TYPE[URL]
     
        #download and prepare histogram array for prices
        file_HIST = ms.fileDownloadGdrive('HISTOGRAM.xlsx','HISTOGRAM')
        df_hist = pd.read_excel(file_HIST,sheet_name = 'HIST',index_col = [0,1])
        r_date = df_hist.index.droplevel(1)[-1]
        histogram = df_hist.loc[r_date] #slicing only recent data for histogram        

        #collect property db   
        db = ms.collect_db(ptype,histogram)
        df_list =  pd.DataFrame(db[0])
        hist_actual =  pd.DataFrame(db[1])

        #creating level 1 and 0 of MultiIndex for db and Index for Hist
        df_list['date_col'] = timestamp
        df_list['ptype'] = ptype
        
        hist_actual['ptype'] = ptype
        
        #save intermidiate data
        file_name = '{ptype}_db.xlsx'.format(ptype = ptype)
        df_list.to_excel(file_name)
        df2 = pd.read_excel(ms.fileDownloadGdrive(file_name,'INTERMIDIATE_DATA'),
            index_col = 0) ##previous db to use later before we uploaded the new one
        Spyder().file_uploadGDrive(file_name,'INTERMIDIATE_DATA')
        
        ptype_df.append(df_list)
        histogram_df.append(hist_actual)
        
        #save statistics
        df1 = df_list       
        df_stat = ms.collectStat(df1,df2,timestamp)

    #saving final data    
    
    df_all = pd.concat(ptype_df)
    hist_all = pd.concat(histogram_df)
    

    df_all = df_all.set_index(['ptype','id']).sort_index(level =\
                                     'ptype')
    
    hist_all = hist_all.set_index('ptype')    
    
    df_groups1= hist_all.groupby(level = 0).sum()['n_properties']    

    file_name = 'db_all.xlsx'
    
    with pd.ExcelWriter(file_name) as writer:
        df_all.to_excel(writer, sheet_name='db_all_without_cal')
        hist_all.to_excel(writer, sheet_name='HIST_ACTUAL')
        df_groups1.to_excel(writer, sheet_name='GROUPS_BY_TYPE')       
    
    ms.file_uploadGDrive(file_name,'PROPERTY_DB')

    return df_all,hist_all,df_groups1,df_stat


def collectHistogram():
    """
    calculate price ranges to get the number of properties in each close 
    to 300 or actual    
    """
    file_URL = Spyder().fileDownloadGdrive('URL_list_ABNB','URL_LIST')
    URLs = pd.read_excel(file_URL,index_col = 0)
    file_HIST = Spyder().fileDownloadGdrive('HISTOGRAM.xlsx','HISTOGRAM')
    df_hist = pd.read_excel(file_HIST,sheet_name = 'HIST',index_col = [0,1])
        
    for URL in URLs.index:
        ms = Airbnb_spyder(URLs.URL[URL].strip('﻿'))
        ptype = URLs.TYPE[URL]
        df_hist1 = pd.DataFrame(ms.collectNumberProp(ptype))
        df_hist1['date_col'] = timestamp
        df_hist1['ptype'] = ptype
        df_hist1 = df_hist1.set_index(['date_col','ptype']).sort_index(level =\
                                     'date_col')
        df_hist = df_hist.append(df_hist1, sort = False)

    df_groups1= df_hist.groupby(level = [0,1]).sum()['number of properties']
    df_groups2= df_hist.groupby(level = 0).sum()['number of properties']    
    
    with pd.ExcelWriter('HISTOGRAM.xlsx') as writer:
        df_groups1.to_excel(writer, sheet_name='GROUPS_BY_TYPE')
        df_groups2.to_excel(writer, sheet_name='GROUPS_BY_DATE')
        df_hist.to_excel(writer, sheet_name='HIST')      
        
    Spyder().file_uploadGDrive('HISTOGRAM.xlsx','HISTOGRAM')
    
    return df_hist    

df = collectDb()

#df_hist = collectHistogram()

def StartFromInterrupt():
    """
    """
    
    pass 
    
    