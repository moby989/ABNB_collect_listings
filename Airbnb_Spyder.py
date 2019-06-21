#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 15:29:38 2019

@author: moby
"""

from Spyder import Spyder
from json import JSONDecodeError
import math
import pandas as pd
from Cookies import headers_ABNB,cookies_ABNB
import sys

class Airbnb_spyder(Spyder):
 
    def __init__(self,url):
        
        Spyder.__init__(self)
        self.url = url                     
        self.cookies = Spyder().makeCookiesDict(cookies_ABNB)
        self.headers = headers_ABNB
        self.errors_JSON = 0
        self.errors_URL = 0
        
    def getNumberProp(self,data):
        
        """
        gets json array of data from API and returns number of properties
        for the search page
        
        """        
        number_prop = self.parserHelper(data,'explore_tabs',0,'home_tab_metadata','listings_count')        
                        
        return number_prop
    
    def getJson(self,payload = None,retry_count = 1, check_calc = False):
        
        """
        HELPER FUNCTION
        retries requests if the previous attempt was unsuccessful
        
        """
        
        if check_calc == True:
            r = self.get_r(self.url,payload, check_calc = True)
        
        else:
            r = self.get_r(self.url,payload)

        try:        
            data = r.json()
        except (JSONDecodeError,AttributeError) as e:
            print(e.__class__)
            error_message = 'There was an error getting JSON object from URL {url} and {payload}'.format(url = self.url,payload = payload)
            text_file = self.createTextFile (error_message,'errors.txt')
            self.file_uploadGDrive(text_file,'Errors')
            data = None
            
        print ('Retry getting JSON N '+str(retry_count))

        if isinstance(data,type(None)):
            retry_count +=1             
            if retry_count > 4:
                self.errors_JSON +=1
                print("can't make the request to API")
                return data
            else:
                self.getJson(payload,retry_count)
        else:
            return data
                
    
    def getPriceRange(self,min,max,max_p = None):
        
        """
        defines the range of prices for URL request to get the maximum number 
        of propertes per request (close to 300)
        
        """
    
        payload = {'price_min':min,'price_max':max}
        
        data = self.getJson(payload)
        
        number = self.getNumberProp(data)  
        print ('number '+str(number)+' min '+str(min)+' max '+str(max))
        
        if isinstance(number,type(None)):
            return min,max,0
        
        if max_p == None:                                    
            delta = int((max-min)//2)
            if number  <= 300:
                return min,max,number
        else: 
            delta = int(math.fabs(max - max_p)//2)                               
        
        if delta > 0:
            if number > 300:
                min,max,number = self.getPriceRange(min,max-delta,max)
            elif (300 - number) > 10:
                min,max,number = self.getPriceRange(min,max+delta,max)
            else:
                return min,max,number                    
        else:
            
            if number > 300:
                if max <=min:
                    return min,max,number
                else:
                    min,max,number = self.getPriceRange(min,max-1,max)

        print(min,max,number)
        return min,max,number
    
    def getPriceRangeWrapper(self):
        
        """
        the function makes the list of price ranges(tuples) from 0 to the 
        maxumum price (10000USD) exising to include the maximum amount of properties in 
        each range
        
        """
        
        price_ranges = {}
        histogram = [{'number of properties':0,'minimum_price':0,'maximum_price':0}]
        min = 0
        max = 1250
            
        while min < max:
            
            min_max = self.getPriceRange(min,max)
            price_ranges['number of properties'] = min_max[2]
            price_ranges['minimum_price'] = min_max[0]
            price_ranges['maximum_price'] = min_max[1]
            histogram.append(price_ranges)
            min = min_max[1] + 1
            price_ranges = {}
            print(histogram)
  
        ##cover the properries which prices higher than 2000USD per night
        min_max = self.getPriceRange(min,10000)
        price_ranges['number of properties'] = min_max[2]
        price_ranges['minimum_price'] = min_max[0]
        price_ranges['maximum_price'] = min_max[1]
        histogram.append(price_ranges)
        
        return histogram
        
    def parserHelper(self,data,*args):

        """
        special helper functons which returns None value if it can't find the dict key 
        and returns the value of that key if the key exist (helps to avoid errors while parsing
        pages where some dict keys can be missing for some properties)
        
        """
        try: 
            if args and data:
                element  = args[0]
    
                if isinstance(element,str):                
                    value = data.get(element)
                else:
                    value = data[element]                
    
                return value if len(args) == 1 else self.parserHelper(value, *args[1:])
            else:
                return None
       
        except (KeyError,IndexError):
            return None

    def parsePage(self,data):
        
        """
        gets dict/list of data (just a single page) and returns a list 
        of properties with relevant info on them
        
        """
        property_list = [{'id':0,'name':0,'localized_city':0,'localized_neighborhood':0,'dprice':0,'currency':0,'nreviews':0,\
        'area':0,'subdistrict':0,'lats':0,'lon':0,'nbedrooms':0,'max_guests':0,'url':0,\
        'instant_booking':0,'monthly_price_f':0,'weekly_price_f':0,'is_superhost':0,\
        'picture_count':0,'host_lang':0,'host_picture':0,'review_score':0,\
        'picture_colour':0,'privacy_type':0,'property type':0,'extra info':0}]
        

        data_s = self.parserHelper(data,'explore_tabs',0,'sections',0,'listings')

        if isinstance(data_s,type(None)):
            data_s = self.parserHelper(data,'explore_tabs',0,'sections',1,'listings')

        if isinstance(data_s,type(None)) or len(data_s) == 0: #returns empty list if the server response was empty
            numb_prop = 0
            error_message = "Can't retreive the data from the request (probably the response from the server was empty. URL -> {url}".format(url = self.url)            
            text_file = self.createTextFile (error_message,'errors.txt')
            self.file_uploadGDrive(text_file,'Errors')
            self.errors_JSON +=1
            
        else:            
            for i in range(len(data_s)):
                
                property = {}            
                
                property['id'] = self.parserHelper(data_s,i,'listing','id')
                property['name'] = self.parserHelper(data_s,i,'listing','name')
                property['localized_city'] = self.parserHelper(data_s,i,'listing','localized_city')
                property['localized_neighborhood'] = self.parserHelper(data_s,i,'listing','localized_neighborhood')
                property['dprice'] = self.parserHelper(data_s,i,'pricing_quote','rate','amount')
                property['currency'] = self.parserHelper(data_s,i,'pricing_quote','rate','currency')
                property['nreviews'] = self.parserHelper(data_s,i,'listing','reviews_count')
                property['area'] = self.parserHelper(data_s,i,'listing','city') 
                property['subdistrict'] = self.parserHelper(data_s,i,'listing','public_address')
                property['lats'] = str(self.parserHelper(data_s,i,'listing','lat'))
                property['lon'] = str(self.parserHelper(data_s,i,'listing','lng'))
                property['nbedrooms'] = self.parserHelper(data_s,i,'listing','bedrooms')
                property['max_guests'] = self.parserHelper(data_s,i,'listing','person_capacity')
                property['url'] = self.parserHelper(data_s,i,'listing','picture_url')
                
                "optional info"
                
                property['instant_booking'] = self.parserHelper(data_s,i,'pricing_quote','can_instant_book')
                property['monthly_price_f'] = self.parserHelper(data_s,i,'pricing_quote','monthly_price_factor')
                property['weekly_price_f'] = self.parserHelper(data_s,i,'pricing_quote','weekly_price_factor')
                property['is_superhost'] = self.parserHelper(data_s,i,'listing','is_superhost')
                property['picture_count'] = self.parserHelper(data_s,i,'listing','picture_count')
                property['host_lang'] = '/'.join(self.parserHelper(data_s,i,'listing','host_languages')) #joined into one string for correct export to excel cell
                property['host_picture'] = self.parserHelper(data_s,i,'listing','user','picture_url')            
                property['review_score'] = self.parserHelper(data_s,i,'listing','avg_rating')
                property['picture_colour'] = self.parserHelper(data_s,i,'listing','picture','dominant_saturated_color')
                property['privacy_type'] = self.parserHelper(data_s,i,'listing','room_type_category')
                property['property type'] = self.parserHelper(data_s,i,'listing','space_type')
                property['extra info'] = ''            
    
                property_list.append(property)  
                numb_prop = len(data_s)
                
        
        print(numb_prop)
        
        return property_list,numb_prop
        
    def parsePageProperty(self,data):
        
        """
        gets a dict of data from Airbnb API and returns 
        info about availability and prices for selected period
        
        """
        
        property_calendar = {}        
        
        for month in range (0,12):                
    
            data_s = self.parserHelper(data,'calendar_months',month,'days')

            if isinstance(data_s,type(None)): #returns empty list if the server response was empty
                error_message = "Can't retreive the data from the request (probably the response from the server was empty. URL -> {url}".format(url = self.url)
                text_file = self.createTextFile (error_message,'errors.txt')
                self.file_uploadGDrive(text_file)
                property_calendar['extra info'] = 'no calendar data for the property'

            else:                
                property_calendar['date_collected_at'] = self.parserHelper(data,'calendar_months',0,'dynamic_pricing_updated_at')            
                for i in range(len(data_s)):                                    
                    if self.parserHelper(data_s,i,'available'):
                        date = self.parserHelper(data_s,i,'date')             
                        price = int(self.parserHelper(data_s,i,'price','local_price'))
                        min_nights = self.parserHelper(data_s,i,'min_nights')
                        max_nights = self.parserHelper(data_s,i,'max_nights')
                        price_method = self.parserHelper(data_s,i,'price','type')                                        
                       
                        property_calendar[date] = price
                        property_calendar['min_nights'] = min_nights
                        property_calendar['max_nights'] = max_nights
                        property_calendar['price_method'] = price_method
        
                    else:
                        date = self.parserHelper(data_s,i,'date')
                        property_calendar[date] = -1
                                        
        return property_calendar
    
    def checkDbAddDisp(self,df1,df2):
        """
        compares the current db with the previous to identify added or disposed
        properties        
        """
        df1 = df1.set_index('id')
        df2 = df2.set_index('id')
        
        additions = df1.index.difference(df2.index)
        disposals = df2.index.difference(df1.index)
                    
        df_additions = pd.DataFrame()
        df_disposals = pd.DataFrame()

        try:
            if len(additions) ==0:
                pass
            else:
                df_additions = df1.loc[additions]
        except AttributeError:
             pass   
        try:
            if len(disposals) == 0:
                pass
            else:
                df_disposals = df2.loc[disposals]                     
        except AttributeError:
            pass
                                        
        return df_additions,df_disposals          
    
    def collectNumberProp(self,ptype):

        """
        collects the number of properties for each price range to get the number close to 300
        """
        
        histogram = self.getPriceRangeWrapper()
        name_histogram = '{ptype}_histogram'.format(ptype = ptype)
    
        #saving data
        xl_file = self.save_data(histogram,'excel',name_histogram)
        self.file_uploadGDrive(xl_file,'OTHER_DATA')
        csv_file = self.save_data(histogram,'csv',name_histogram)
        self.file_uploadGDrive(csv_file,'OTHER_DATA')
                        
        return histogram
    
    def collect_db(self,ptype,histogram):
    
        """
        collects all the properties for each price range into the list of dicts 

        """                
        property_list = []
        hist_actual = []
        hist = {}
        total = 0        
        
        for row in histogram.loc[ptype].iterrows():
     
            hist = {}
            number_t = 0
            number = 0
            ofs = 0
            last_page_flag = True        
            
            while last_page_flag:        
                payload = {'price_min':row[1][1],'price_max':row[1][2],'items_offset':ofs}                        
                data = self.getJson(payload)
                print ('Ptype -->'+str(ptype))
                processed_data = self.parsePage(data)
                property_list.extend(processed_data[0][1:])
                number = processed_data[1]         
                print('URL requested for prices from ' + str(payload['price_min']) + ' until ' + str(payload['price_max']))
                print('Got info for ' + str(number) + ' properties.')             
                ofs +=50
                last_page_flag = self.parserHelper(data,'explore_tabs',0,'pagination_metadata','has_next_page')   
                number_t += number
            
            total += number_t
    
            hist['n_properties'] = number_t
            hist['minumum_price'] = payload['price_min']
            hist['maximum_price'] = payload['price_max']

            hist_actual.append(hist)
       
        print('total number of properties collected-->'+str(total))

    
        return property_list,hist_actual
    
    def collectStat(self,df1,df2,timestamp):
        """
        collect metrics for the last session of AirbnbSpyder (number of collected prop,
        addded properries, disposed properties, etc)
        
        """
        
        #downloading historical data
        file_STATS = self.fileDownloadGdrive('STATS.xlsx','STATS')
        df_stat = pd.read_excel(file_STATS,sheet_name = 'STATS',index_col = [0,1]).sort_index(level =\
                                     'date_col')
        try:
            df_add = pd.read_excel(file_STATS,sheet_name='ADDITIONS').set_index('date_col').loc[timestamp]   
        except KeyError:
            df_add = pd.DataFrame()
        try:
            df_disp = pd.read_excel(file_STATS,sheet_name='DISPOSALS').set_index('date_col').loc[timestamp]
        except KeyError:
            df_disp = pd.DataFrame()
        
        #updating the df with a new statistics
        n_prop = len(df1.index.drop_duplicates())
        ptype = df1['ptype'][0]
    
        AddDisp = self.checkDbAddDisp(df1,df2)
        
        n_additions = len(AddDisp[0])
        n_disposals = len(AddDisp[1])
        
        df_add = df_add.append(AddDisp[0])
        df_disp = df_disp.append(AddDisp[1])
        
        dict = {'date_col':timestamp,
                'ptype':ptype,
                'prop_collected':n_prop,
                'new_properties':n_additions,
                'disp_properties':n_disposals,
                'errors_URL':self.errors_URL,
                'errors_JSON':self.errors_JSON}
        
        stat = pd.DataFrame(dict,index = [1]).set_index(['date_col','ptype']).\
                                sort_index(level =\
                                     'date_col')
                
        print (stat)
        df_stat = pd.concat([df_stat,stat]).sort_index(level =\
                                     'date_col')
        
        print (df_stat)
#        .loc[timestamp,ptype] = [n_prop,n_additions,n_disposals,\
#              self.errors_URL,self.errors_JSON]
    
        file_name = 'STATS.xlsx'
        with pd.ExcelWriter(file_name) as writer:
            df_stat.to_excel(writer, sheet_name='STATS')
            df_add.to_excel(writer, sheet_name='ADDITIONS')
            df_disp.to_excel(writer, sheet_name='DISPOSALS')    
        
        self.file_uploadGDrive(file_name,'STATS')
        
        return df_stat
    
    def StartFromInterrupt(self,timestamp):
        """
        Checker 
        In case of early interrupt continues running the code from the point 
        where last time it was aborted
        """
        timestamp = timestamp.split(',')[0]
        file_URL = self.fileDownloadGdrive('URL_list_ABNB','URL_LIST')
        URLs = pd.read_excel(file_URL,index_col = 0)
        
        file_STATS = Spyder().fileDownloadGdrive('STATS.xlsx','STATS')
        df_stat = pd.read_excel(file_STATS,sheet_name = 'STATS',index_col = [0,1]).sort_index(level =\
                                     'date_col')    
        
        last_date = df_stat.index.droplevel(1)[-1]
        
        if last_date.split(',')[0]!=timestamp:
            return URLs,[],[]
        
        df_stat = df_stat.loc[last_date]

#        print (df_stat)
        if len(df_stat.index) == 3:
            sys.exit()                      
    
        URLs = URLs.set_index('TYPE')
#        print (URLs)
        unparsed_ptypes = URLs.index.difference(df_stat.index)
        URLs = URLs.loc[unparsed_ptypes].reset_index().rename(index = str,columns = {'index':'TYPE'})
        
#        print (URLs)
        
        #updating list with df which has been collected already today
        ptype_df = []
        histogram_df = []
        for ptype in df_stat.index:
            file_name = '{ptype}_db.xlsx'.format(ptype = ptype)
            file_name2 = '{ptype}_hist.xlsx'.format(ptype = ptype)
            df_list = pd.read_excel(self.fileDownloadGdrive(file_name,'INTERMIDIATE_DATA'),index_col = 0)
            hist_actual = pd.read_excel(self.fileDownloadGdrive(file_name2,'INTERMIDIATE_DATA'),index_col = 0)
            ptype_df.append(df_list)
            histogram_df.append(hist_actual)

        return URLs,ptype_df,histogram_df
                                   