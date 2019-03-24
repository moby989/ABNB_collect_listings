#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 17:11:41 2019

@author: moby
"""
from bs4 import BeautifulSoup
from file_writer import FileWriter
import time
import csv
import requests
from datetime import datetime,timedelta
import random
import sys
import statistics



class Spyder(object):

    def __init__(self):
        
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0)\
                   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 \
                   Safari/537.36'}        
        self.calls = 0
        self.today = datetime.today().date()
    
    def cont_flag_set(self):
       
        global cont_flag
        cont_flag = False
        
    def calc_av_median_mixed_list(self,list):
    
        cleaned_list = []
        
        for x in list:
            try:
                if isinstance(float(x), (int, float)):
                    cleaned_list.append(float(x))
            except ValueError:
                pass                  

        average = statistics.mean(cleaned_list)
        median = statistics.median(cleaned_list)
        
        return average,median
    
     
    def timer (self,delay):
        print('Just wait for '+str(delay)+' seconds between URL requests.')
        for i in range(delay,0,-1):

            sys.stdout.write(str(i)+' ')
            sys.stdout.flush()
            time.sleep(1)
        print ('Go!')
        
        
    def get_bool(self,value):
        while True:
            try:
               return {"true":True,"false":False}[input(value).lower()]
            except KeyError:
               print ("Invalid input please enter True or False!")
        
    def save_data(self,data,format,file_name,folder_name = None):
                
        writer = FileWriter(data)
        
        create_file_name = writer.output_file(format,file_name)
        
#        writer.upload_file_to_GoogleDrive(create_file_name,folder_name)
            
        return create_file_name        
        
    def get_data_from_file(self,file_name):        
        
        ###the file has to be in CSV format
        
        file_name = file_name

        data_extracted = []

        with open(file_name, mode='r') as csv_file:

            data = csv.DictReader(csv_file)
            for row in data:
                data_extracted.append(row)
                       
        return data_extracted       
    
    def get_r(self,url, payload = None):
        
        if self.calls > 100:
            self.timer(900)
            print ('DELAY AFTER 20 REQUESTS')
            self.calls = 0
        
        r = requests.get(url, cookies = self.cookies, headers = self.headers, params = payload)
        
        print('URL -> ' + str(r.url))
        self.calls +=1
#        with open ('html_page.html','w') as file:
#            file.write(self.get_script2(r))
        
        delay = random.randint(1,15)
        self.timer(delay)
        
        
        return r
    
    def get_script(self,url,payload = None):
          
        #[DEPRECIATED]
        
        #depreciated
        
        a = 0
        
        b = 2/a
           
        r = requests.get(url, headers = self.headers)
        page = BeautifulSoup(r.content,'lxml')
        time.sleep(self.delay)
        
        pass

    def get_script2 (self,r):
                        
        page = BeautifulSoup(r.content,'lxml')
        
#        print(page.find_all(attrs={"data-et-view":" eWHJbWPNZWEHXT:5"}[0]))        
        
        return page
    
    def booking_dates(self,period,length_stay):
    
        #returns - list of pairs (start,finish) dates for a booking
        # period and length_stay in days
        
        booking_dates = [] #list of dict each represening a pair of checkin/out days
        
        today = datetime.today()+timedelta(days=19)
        
        delta = timedelta(days=length_stay)
        
        for i in range (period):
            checkin_day = today + timedelta (days = i)
            checkout_day = checkin_day + delta
            dates = {}
            dates['n'] = str(i)
            dates['checkin'] = str(checkin_day.date())
            dates['checkout'] = str(checkout_day.date())
            booking_dates.append(dates)                    

        self.save_data(booking_dates,'csv','booking_dates','Helpers')
                    
        return booking_dates
    
    def cleanup_dates(self):

        dates = self.get_data_from_file('booking_dates{param1}.csv'.format(param1 = datetime.today().date()))

        dates.pop(0)
                        
        try:
            self.save_data(dates,'csv','booking_dates','Helpers')
        except IndexError:
            pass
        
        return dates
            
    def average_price_calc(self,property_list):
       
        #[DEPRECIATED]
        
        #gets property_list - list of dicts including info for different properties like id, name, price, etc.
        #returns av_price = int,calculated average price among different properties
        
        av_prices = []
        
        for property in property_list:
        
            if property['sleep_arrang'] == 1 or property['sleep_arrang'] == 'no data':
                k = 1
                if property['sleep_arrang'] == 'no data': 
                    print ('Property ID ' + str(property['id']) + ' doesnt have any sleeping arrangement info.')
            elif property['sleep_arrang'] > 1:        
                k = 0.9
            elif property['sleep_arrang'] > 2:
                k = 0.8
            elif property['sleep_arrang'] > 3:
                k = 0.7
            elif property['sleep_arrang'] > 4:
                k = 0.5                        
                    
            av_prices.append(property['d_price']*k)
            
        av_price = round(sum(av_prices)/len(av_prices))
        
        return av_price
    
    def average_price_by_groups(self,property_list):
        
        #[DEPRECIATED]
         
        #gets - property list of dict including info about properties with their IDs and daily prices 
        #returns - dict of av prices for different properties with different number of bedrooms               
        
        av_prices = []
        av_price = {}
        n_bedrooms = [i for i in range(1,6)]
        
        for n in n_bedrooms:

            for property in property_list:
            
                if property['sleep_arrang'] == n:
                    av_prices.append(property['d_price'])
        
            av_price[str(n)] = round(sum(av_prices)/len(av_prices))
        
        return av_price
        
    def txt_file_create(self,page):
       
        #makes a text file from Beautifulsoup object
        
        with open ('html_page.html','w') as file:
            file.write(page.prettify())
            
        return print ('file with name '+str(file.name) + ' saved.')
    
    def occupancy_calc(self,data,dates):
        
        #gets - 1) a database,list of dicts, where each dict represents a particular property with a relevant info and price for a particular date
        # 2) list of dates for which the availabilty and minimum price were checked
        #returns an amended database where each raw (a dict) is a separate property with estimated occupancy rate for each property and minimum prices for each date in the period
                        
        list_ids = []    
        npdb = []
        av_occupancy = []
        dates = [d['checkin'] for d in dates]
                
        #prepare data
        
        for property in data:
            list_ids.append(property['id'])
        
        cleaned_id = list(set(list_ids))
        

        for id in cleaned_id:        
            n_property = {}
            for property in data:
                if property['id'] == id:
                    n_property[property['date']] = float(property.pop('d_price'))
                    property.pop('date')
                    property.pop('price_format')
                    property.pop('price') 
                    n_property.update(property)
            npdb.append(n_property)
                                               
        #calculate occupancy 
                                
        for property in npdb:
            b_d = 0    #booked days counter                                     
            for i in range(1,len(dates)):
                if property.get(dates[i],'n/a') == 'n/a' and property.get(dates[i-1],'n/a') =='n/a':
                    b_d +=1
        
            occupancy_rate = b_d/(len(dates)-1) #deduct 1 becauese we don't assess the occupancy for the day 1 cause don't have data for the previous day            
            property['occupancy'] = '{:.0%}'.format(occupancy_rate)            
            av_occupancy.append(occupancy_rate)

        av_occy = self.calc_av_median_mixed_list(av_occupancy)
                                        
        #calculate total availability
        
        t_avail = len(cleaned_id) #total number of properties which pop up as available during the period at least one day                                                
         
        #calculate av_avail
        
        availability = []
              
        for date in dates:
            avail = 0
            for property in npdb:                
                if property.setdefault(date,'n/a') != 'n/a':
                    avail  +=1
            availability.append(avail)

        av_avail = int(self.calc_av_median_mixed_list(availability)[0])
        
        #saving data
        self.save_data(npdb,'excel','price_avail_occup_in_{param1}_for_{param2}_'.format(param1 = npdb[0]['city'], param2 = str(dates[0])+'_'+str(dates[-1])))  
        self.save_data(npdb,'csv','price_avail_occup_in_{param1}_for_{param2}_'.format(param1 = npdb[0]['city'], param2 = str(dates[0])+'_'+str(dates[-1])))  
                
        return npdb,av_occy, av_avail, t_avail
   
        
    def calc_av_median(self,data,dates):
        
        price_group = ['<70USD','70-120USD','120-150USD','150-200USD','>200USD']
        
        for id in data:            
            av_price = []
            for date in dates:
                av_price.append(id[date['checkin']])
            a,m = self.calc_av_median_mixed_list(av_price)            
                        
            id['av_price_property'] = int(a)
            if a < 70:
                id['price_group'] = price_group[0]
            elif 70 <= a < 120:
                id['price_group'] = price_group[1]
            elif 120 <= a < 150:
                id['price_group'] = price_group[2]
            elif 150 <= a < 200:
                id['price_group'] = price_group[3]
            else:
                id['price_group'] = price_group[4]
    

        av_price3 = {} #dict, where keys are price groups, values - average prices for that group
        for group in price_group:
            av_price1 = [] #list of average prices for particular dates for particualr price groups. len = len of dates
            for date in dates:
                av_price2 = [] #list of prices for all properties for each particular date. len = number of properties in particular price groups
                for id in data:                    
                    if id['price_group'] == group:#                        print(date)
                        av_price2.append(id[date['checkin']])#          
                a,m = self.calc_av_median_mixed_list(av_price2)
                av_price1.append((int(a),int(m)))
            av_price3[group] = av_price1
        
        self.save_data(data,'excel','price_groups_{param2}_{param1}'.format(param1 = data[0]['city'], param2 = str(dates[0]['checkin'])+'_'+str(dates[-1]['checkin'])))  
        
                
        return data,av_price3
    
    
        
        
        
        
        
        
        
        