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
from Cookies import headers,cookies



class Spyder(object):

    def __init__(self):
        
        self.headers = headers #taken from cookies files  
        self.calls = 0 ## counter for requests, later if the number of requests >200 
        #the code freezes for 200sec
        self.today = datetime.today().date()
    
    def makeCookiesDict(self,cookies):
        
        """
        transforms cookies from JSON (as created by GChrome ext) into the dict
        
        """
                
        cookies_dict = {}
        
        for cookie in cookies:
            name = cookie['name']
            value = cookie['value']    
            cookies_dict[name] = value
    
        return cookies_dict        
       
    def timer (self,delay):        

        """
        prints the countdown for delay between requests
        
        """
        print('Just wait for '+str(delay)+' seconds between URL requests.')
        
        for i in range(delay,0,-1):
            sys.stdout.write(str(i)+' ')
            sys.stdout.flush()
            time.sleep(1)
 
        print ('Go!')
        
        
    def get_bool(self,value):
       
        """
        HELPER FUNCTION - makes sure that the input is correct
        
        """
        
        while True:
            try:
               return {"true":True,"false":False}[input(value).lower()]
            except KeyError:
               print ("Invalid input please enter True or False!")
        
    def save_data(self,data,format,file_name,folder_name = None):
             
        """
        saves data array into EXCEL/CSV file
        
        date is a list of dict where dict keys are the names of columns in the output file
        
        """
            
        writer = FileWriter(data)                
        
        create_file_name = writer.output_file(format,file_name,folder_name)
        
#        writer.upload_file_to_GoogleDrive(create_file_name,folder_name)
            
        return create_file_name        
        
    def get_data_from_file(self,file_name):        
        
        """
        reads the data from CSV file into the list of data where each items is a dict

        """

        data_extracted = []

        with open(file_name, mode='r') as csv_file:

            data = csv.DictReader(csv_file)
            for row in data:
                data_extracted.append(row)
                       
        return data_extracted       
    
    def get_r(self,url, payload = None):
        
        """
        make requests with REQUESTS library
        
        """
                
        if self.calls > 100:
            self.timer(200)
            print ('DELAY AFTER 20 REQUESTS')
            self.calls = 0
        
        r = requests.get(url, cookies = self.makeCookiesDict(cookies), headers = self.headers, params = payload)
        
        print('URL -> ' + str(r.url))
        self.calls +=1
        
        delay = random.randint(1,15)
        self.timer(delay)
                
        return r
    
    
    def get_script2 (self,r):
                        
        """
        makes a Beatuful soup object from r object provided by REQUESTS
                
        """
                
        page = BeautifulSoup(r.content,'lxml')
                
        return page
    
    def booking_dates(self,period,length_stay):
    
        """            
        prepared the list of pairs (start,finish) dates for a booking
        period and length_stay in days
        
        """        
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

        """
        HELPER FUNCTION
        
        gets checkin/our dates list from the file, deletes the last processed 
        date and writes it back to the file. Used to continue the code running 
        in case of error or prior stop
        
        """        
        
        dates = self.get_data_from_file('booking_dates{param1}.csv'.format(param1 = datetime.today().date()))

        dates.pop(0)
                        
        try:
            self.save_data(dates,'csv','booking_dates','Helpers')
        except IndexError:
            pass
        
        return dates
            
    def cont_flag_set(self):
       
        """
        DEPRECIATED
        
        HELPER FUNCTION - cont_flag is FALSE when the last code run was successful 
        and next run has to be from the beggining. Otherwise the code extract 
        the data from the file with intermidiare results and continies execution
        
        """
        
        global cont_flag
        cont_flag = False
        
    def get_script(self,url,payload = None):
          
       """
       [DEPRECIATED]      
       """        
       a = 0
        
       b = 2/a
           
       r = requests.get(url, headers = self.headers)
       page = BeautifulSoup(r.content,'lxml')
       time.sleep(self.delay)
        
       pass
        
       