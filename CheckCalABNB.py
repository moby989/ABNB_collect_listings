#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 14:28:11 2019

@author: moby
"""

import pandas as pd
from Airbnb_Spyder import Airbnb_spyder
from Spyder import Spyder
from datetime import datetime, timedelta
import time


def makeCalendarAvail(area_db = None, ptype = None, length = 351):
    
    """
    gets list of properties
    returns same list but updated with prices for future dates (calendar) for each property
    
    """           
    start = time.time()
    
    #collecting data range

    

    today = datetime.today()    
    year = today.year
    month = today.month
    end = datetime.today()+timedelta(days=length)    
    dates = pd.period_range(start=today.strftime('%Y-%m-%d'), end=end, freq='D')    
    files = Spyder().checkGdriveAndDownloand('Temp','temp_pindex.csv','temp_pcal')                
#    files = None
    if isinstance(files[0],type(None)):
        print('Начинаем проверку календаря объектов сначала')
        df = pd.read_excel('Airbnb_current.xlsx')   
        df = df.set_index('id')
        df_index = df.index
        new_columns = ['localized_neighborhood','localized_city','privacy_type','property type','name','dprice','currency','review_score','nreviews','url','area','subdistrict','lats','lon','nbedrooms','max_guests','instant_booking','is_superhost','monthly_price_f','weekly_price_f','price_method','min_nights','max_nights','picture_count','picture_colour','host_lang','host_picture','date_collected_at','extra info']
        df.reindex(columns = new_columns)
        
        #making list of column headers with dates in the main dataframe
        
        text_fields = pd.Series(['date_collected_at','min_nights','max_nights','price_method',\
                                 'url'])
    
        dates = pd.Series(dates)
        
        new_fields = pd.concat([text_fields,dates])

        for nf in new_fields:
            df[str(nf)] = 0
        
        df = df.apply(pd.to_numeric,errors = 'ignore')
        df.info(memory_usage = 'deep')            

    else:        
        print ('берем из архива')
        df = pd.read_csv(files[1],index_col = 'id')
        df_index = pd.read_csv(files[0],index_col ='id').index
                
    #collecting info about prices        
    try:    
        df_index2 = df_index.copy()
        for id in df_index2[:100]:
            url = 'https://www.airbnb.ru/api/v2/calendar_months?_format=with_conditions&count=12&currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id={property_id}&locale=en&month={month}&year={year}'.format(property_id = id, year = year, month = month)
            my_spyder = Airbnb_spyder(url)    
            data = my_spyder.getJson(check_calc = True)
            calendar = my_spyder.parsePageProperty(data)
            calendar_df = pd.DataFrame(calendar, index=[id])  
            date_df = pd.DataFrame({'time_data_collected': [datetime.today()]}, index=[id])
            url_df = pd.DataFrame({'url': ['https://www.airbnb.com/rooms/{property_id}?&adults=2&infants=1&guests=1&toddlers=0&home_collection=1&source_impression_id=p3_1557415334_ZiMEi2ijYDtLV1MY&children=0'.format(property_id = id)]}, index=[id])
            df.update(calendar_df)
            df.update(date_df)
            df.update(url_df)
            df_index = df_index.delete([0])
            print ('Current bunch:')
            print ('Checked '+str(df_index2[:100].get_loc(id)+1)+' out of '+str(df_index2[:100].size)+' properties to check.')
            print ('Total:')            
            print ('Checked '+str(df.index.get_loc(id)+1)+' out of '+str(df.index.size)+' properties to check.')
            print ('Left '+str(df_index.size)+' properties to check.')
               
        assert (df_index2[:100][-1] == df_index2[-1]),"Will continue after a short break" #make sure that we are not checking the last bunch of properties and save intermidiate results
                  
#    except ValueError as e:
    except (BaseException,Exception) as e:        
        if AssertionError: 
            print ("Cохраняем промежуточные результаты")
        else:            
            print ('There was an error during calendar check. Temporary results saved in TEMP folder')
        print(e.__class__)
        file_name = 'temp_pcal'
        df.to_csv(file_name+'.csv')
        Spyder().file_uploadGDrive(file_name+'.csv','Temp')
        pd.DataFrame(df_index).to_csv('temp_pindex.csv',index = False)
        Spyder().file_uploadGDrive('temp_pindex.csv','Temp')
        
    else:
        print("Заканчиваем обработку и сохраняем результаты")        
        file_name = 'db_all_calendar'
        df.to_excel(file_name+'.xlsx')
        df.to_csv(file_name+'.csv')
        Spyder().file_uploadGDrive(file_name+'.xlsx','PROPERTY_CAL_DB')
        Spyder().file_uploadGDrive(file_name+'.csv','PROPERTY_CAL_DB')
        Spyder().cleanFolderGdrive('Temp')
        
    end = time.time()
    print ('Total time the process running is '+str(int((end - start)//60))+' min.')
                                
    return df
    
def aggregateDb():
    
    """
    makes one file for all the properties in the area

    """    
    
    #reading the list of URL to parse from GD
    file_URL = Spyder().fileDownloadGdrive('URL_list_ABNB')
    URLs = pd.read_excel(file_URL,sheet = 'Bali',index_col = 0)
    
    db_list = []
    
    for URL in URLs.index:        
        ptype = URLs.TYPE[URL]  
        db_type = Spyder().fileDownloadGdrive('{ptype}_db.csv'.format(ptype = ptype))    
        db_list.append(pd.read_csv(db_type))

    area_db = pd.concat(db_list)
    area_db.to_excel('test_file.xlsx',index = False)
    
    return area_db



df = makeCalendarAvail()
    
#df = aggregateDb()

"""
    1) timestamp криво показывается
    3) полная цена и ее разбивка
    4) В сообщении об ошибке обращения к серверу надо собрать больше инфы для посдеж проверки
    6) сократить срок чтобы не было пустых дат - 9 дней
    куда то пропадают картинки с виллой из базы
    проверить ли есть там дома из категоии +
    сделать время выполнения (может добавить в отчет)
    добавить прогресс по скачиванию
    для ошибочных объектов запустить повторную проверку
    
"""

