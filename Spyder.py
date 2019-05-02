#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 17:11:41 2019

@author: moby
"""
from __future__ import print_function
from bs4 import BeautifulSoup
from file_writer import FileWriter
import time
import csv
import requests
from datetime import datetime,timedelta
import random
import sys
from Cookies import headers,cookies
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.http
#import pprint
#import httplib2
import io
from googleapiclient.http import MediaIoBaseDownload
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout


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
        saves a data array into EXCEL/CSV file
        
        date is a list of dict where dict keys are the names of columns in the output file
        
        """
            
        writer = FileWriter(data)                
        
        create_file_name = writer.output_file(format,file_name,folder_name)
        
#        writer.upload_file_to_GoogleDrive(create_file_name,folder_name)
            
        return create_file_name    

    def createTextFile (self,data,name):
        
        """
        creates a text file with some supplemental info for parsing
        
        """        
        with open(name, mode='w') as f:
            for item in data:
                f.write(str(item))            
        return name
        
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
    
    def get_r(self,url, payload = None, retry_count = 1):
        
        """
        make requests with REQUESTS library
        
        """
                
        if self.calls > 100:
            self.timer(200)
            print ('DELAY AFTER 20 REQUESTS')
            self.calls = 0
        
        try:        
            r = requests.get(url, cookies = self.makeCookiesDict(cookies), headers = self.headers, params = payload,timeout = 10)
            print('URL -> ' + str(r.url))    

        except (ConnectionError,Timeout,ReadTimeout):
            print ('Max retries or Timeout exceeded for URL {url}'.format(url = url))
            error_message = 'Max retries or Timeout exceeded for URL {url}'.format(url = url)
            text_file = self.createTextFile (error_message,'errors.txt')
            self.file_uploadGDrive(text_file)
            retry_count +=1
            print ('Retry # '+str(retry_count))
            if retry_count > 3:
                r = 1
            else:
                r = self.get_r(url,payload,retry_count)                        
                
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
    
    def makeTextFile(self,data):
        
        """
        HELPER FUNCTION
        makes a text file from html content
        """
        
        file_name = 'data_text.html'
        with open(file_name, mode='w+') as html_file:

            html_file.write(data)

        return file_name
            
    def access_gDrive(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
#                http = httplib2.Http()
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server()    
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
       #authenticated GoogleDrive object
        drive = build('drive', 'v3', credentials = creds)
        
        return drive
    
    def file_uploadGDrive(self, file_name, folder_name = None):

        """
        upload a file to the authhenicated GoogleDrive
        
        """
        
        #authentication        
        drive = self.access_gDrive()
        
        # Insert a file. Files are comprised of contents and metadata.
        # MediaFileUpload abstracts uploading file contents from a file on disk.
        media_body = googleapiclient.http.MediaFileUpload(
            file_name,
            resumable=False)
        # The body contains the metadata for the file.
        body = {
          'name': file_name,
          'description': 'scraped data'}
        
        # Perform the request and print the result.
        drive.files().create(body=body, media_body=media_body).execute()
#        pprint.pprint(new_file)
        
    def fileDownloadGdrive(self,name):
        
        """
        download a file from the authhenicated GoogleDrive
        
        """
             
        mod_date = []
#        print(name)
        
        #authentication        
        drive = self.access_gDrive()

        #search file name and getting list of files containing such name        
        file_list = drive.files().list(q = "name contains '{name}'".format(name = name)).execute()
#        print (file_list['files'])
        #finding the latest file
        for file in file_list['files']:        
            metadata = drive.files().get(fileId = file['id'], fields = 'modifiedTime,id').execute()
            mod_date.append(metadata['modifiedTime'])
       
#        print (mod_date)
        file_id_latest = mod_date.index(max(mod_date)) #index of the latest file
        file_id = file_list['files'][file_id_latest]['id'] #id of the latest file
        file_name = file_list['files'][file_id_latest]['name']
#        print (file_id)

        #downloading the file
        
#        print (file_list['files'][file_id_latest]['name'])
        request = drive.files().get_media(fileId=file_id)
#        request2 = drive.files().get_media(fileId=file_id).execute()
#        print(request)
        fh = io.FileIO(file_name,'wb') #file name
        downloader = MediaIoBaseDownload(fh, request) #downloading
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))            
               
        return file_name
        
            
    
    

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
        
       