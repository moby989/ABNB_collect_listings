#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 17:11:41 2019

@author: moby
"""
from __future__ import print_function
from bs4 import BeautifulSoup
import time
import csv
import requests
from datetime import datetime,timedelta
import random
import sys
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.http
import io
from googleapiclient.http import MediaIoBaseDownload
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from pymongo import MongoClient



class Spyder(object):
    
    def __init__(self):
            
        self.calls = 0 ## counter for requests, later if the number of requests >200 
        #the code freezes for 200sec
        self.today = datetime.today().date()
        self.today_timestamp = datetime.today()    
        self.year = self.today.year
        self.month = self.today.month
        self.now = datetime.now()
        self.proxies = {"https" : "http://119.82.252.122:36182"}
    
    def td(self,days):
        period = timedelta(days)
        return period
                
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
    
    def get_r(self,url,payload = None,retry_count = 1,delay = 5, check_calc = False, proxies = None):
        
        """
        make requests with REQUESTS library
        
        """
                
        if self.calls > 100:
            self.timer(200)
            print ('DELAY AFTER 100 REQUESTS')
            self.calls = 0
        
        try:        
            r = requests.get(url, cookies = self.cookies, headers = self.headers, params = payload,timeout = 10, proxies = proxies)
            print(r.url)
            print('URL -> ' + str(r.url))    

        except (ConnectionError,Timeout,ReadTimeout):
            print ('Max retries or Timeout exceeded for URL {url}'.format(url = url))
#            error_message = 'Max retries or Timeout exceeded for URL {url}'.format(url = url)
#            text_file = self.createTextFile (error_message,'errors.txt')
#            self.file_uploadGDrive(text_file,'Errors')
            retry_count +=1
            print ('Retry getting URL # '+str(retry_count))
            if retry_count > 5:
                self.errors_URL +=1
                r = 1
            else:
                inc = random.randint(1,15)
                delay = delay + inc
                self.timer(delay)
                r = self.get_r(url,payload,retry_count,delay)                        
                
        self.calls +=1
                
        if check_calc:            
            delay = random.randint(0,15)
        else:
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
        
        today = datetime.today()+timedelta(days=1)
        
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
        
        """
        
        DEPRECIATED
        
        Shows basic usage of the Drive v3 API.
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
    
    def GDriveHelper(self,drive,*args,count = 1,**kwargs):
        """
        DEPRECIATED
        
        handles exceptions during requests to GoogleDrive
        
        """
        func =  kwargs.pop('func')

        try:                                        
            if func =='list':               
                result = drive.files().list(**kwargs).execute()
                return result
            
            if func =='get':                       
                result = drive.files().get(**kwargs).execute()
                return result
                
            if func =='create':                          
                result = drive.files().create(**kwargs)
                response = None

                while response is None:
                    status, response = result.next_chunk()
                    if status:
                        print ("Uploaded %d%%." % int(status.progress() * 100))
                    print ("Upload Complete!")
                return result
                
            if func =='get_media':   
                result = drive.files().get_media(**kwargs)  
                fh = io.FileIO(args[0],'wb') #file name
                downloader = MediaIoBaseDownload(fh, result) #downloading
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print ("Download '"+str(args[0])+"' %d%%." % int(status.progress() * 100)) 
                return result
            
            if func =='update':            
                result = drive.files().update(**kwargs).execute()                
                return result

        except HttpError as err:
            if err.resp.status in [403, 429, 500]:
                count +=1         
                if count < 5:
                    print ('try one more time to access Gdrive')
                    print ('count = '+str(count))
                    kwargs['func'] = func
                    time.sleep(5)
                    result = self.GDriveHelper(drive,*args,count,**kwargs)

            else: raise
            
            return result

    
    def file_uploadGDrive(self, name, folder_name = None):

        """
        
        DEPRECIATED
        
        upload a file to the authhenicated GoogleDrive
        
        """
        current_timezone = datetime.now()                            
        
        #authentication        
        drive = self.access_gDrive()

        #searching for folder name        
        try:
            folder_ID_list = self.GDriveHelper(drive,func = 'list',\
                q = "mimeType = 'application/vnd.google-apps.folder' \
                and name contains '{name}'".format(name = folder_name))
  
            folder_ID = folder_ID_list['files'][0]['id'] 
    
        except IndexError:
            folder_ID = 'root'
               
        media_body = googleapiclient.http.MediaFileUpload(
            name,            
            resumable=True,
            chunksize=1048576)       
        body = {
          'name': name,
          'parents': [folder_ID],
          'description': 'Upload time: '+str(current_timezone)}
        
        #Perform the request and print the result.
        self.GDriveHelper(drive,func = 'create',body=body, media_body=media_body)       
                
        return None
        
    def fileDownloadGdrive(self,name,folder_name = None):
        
        """
        DEPRECIATED
        
        
        download the most recent file from the authhenicated GoogleDrive
        
        """
             
        mod_date = []
        
        #authentication        
        drive = self.access_gDrive()
        
        #searching Folder_ID
        if folder_name:             
            try:
                folder_list = self.GDriveHelper(drive,func = 'list',q = "mimeType = 'application/vnd.google-apps.folder' and name contains '{name}'".format(name = folder_name))
                folder_ID = folder_list['files'][0]['id']
    
            except IndexError:
                print ('Folder is not found')
                print ('Cant download the file from that folder')    
                return None

            #search file name and getting list of files containing such name        )
            file_list = self.GDriveHelper(drive,func = 'list',q = "'{folder_ID}' in parents and name contains '{name}' and trashed=false".format(name = name, folder_ID = folder_ID))

        else:
            file_list = self.GDriveHelper(drive,func = 'list',q = "name contains '{name}' and trashed=false".format(name = name))
            
        #finding the latest file
        for file in file_list['files']:        
            metadata = self.GDriveHelper(drive,func = 'get',fileId = file['id'], fields = 'modifiedTime,id')
            mod_date.append(metadata['modifiedTime'])
       
        try:
            file_id_latest = mod_date.index(max(mod_date)) #index of the latest file
        except ValueError:
            return None
            
        file_id = file_list['files'][file_id_latest]['id'] #id of the latest file
        file_name = file_list['files'][file_id_latest]['name']

        #downloading the file
        
        self.GDriveHelper(drive,file_name,func = 'get_media',fileId=file_id)                                          
        
        return file_name
        
    
    def checkGdriveAndDownloand(self,folder_name,*args):
        
        "DEPRECIATED"
        
        #authentication        
        drive = self.access_gDrive()
        
        #search for FolderID            
        try:
            folder_list = self.GDriveHelper(drive,func = 'list',q = "mimeType = 'application/vnd.google-apps.folder' and name contains '{name}'".format(name = folder_name))
            folder_ID = folder_list['files'][0]['id'] 
    
        except IndexError:
            print ('Folder is not found')
            print ('Start to collect the calendar from the beggining')
            return None
        
        #files search and download
        files = []
        for name in args:
            try:
                self.GDriveHelper(drive,func = 'list',q = "'{folder_ID}' in parents and trashed=false and name contains '{name}'".format(folder_ID = folder_ID, name = name))
            
            except IndexError:
                print ('Temp files are not found')
                print ('Start to collect the calendar from the begining')
                return None
        
            #download the latest version of the file                        
            files.append(self.fileDownloadGdrive(name,folder_name))        
       
        return files     


    def cleanFolderGdrive(self,folder_name):

        """
        DEPRECIATED
        
        moves temporary files from Temp Folder into Trash Folder (Manual Trash)        
        """
        #authentication        
        drive = self.access_gDrive()
        
        #search for FolderID            
        try:
            folder_list = self.GDriveHelper(drive,func = 'list',q = "mimeType = 'application/vnd.google-apps.folder' and name contains '{name}'".format(name = folder_name))
            folder_ID = folder_list['files'][0]['id'] 
            
        except IndexError:
            print ('Folder is not found and not cleaned')
            return None
        
        #clean the folder        
        file_list = self.GDriveHelper(drive,func = 'list',q = "'{folder_ID}' in parents and trashed=false".format(folder_ID = folder_ID))
        for file in file_list['files']:
            file_ID = file['id']
            folder_ID = '1xmZaxmRIhFkBYbthTshl1TAuGeZAvzfe'
        
            # Retrieve the existing parents to remove
            file = self.GDriveHelper(drive,func = 'get',fileId=file_ID,
                                 fields='parents')
            previous_parents = ",".join(file.get('parents'))
            # Move the file to the new folder
            file = self.GDriveHelper(drive,func = 'update',fileId=file_ID,
                                    addParents=folder_ID,
                                    removeParents=previous_parents,
                                    fields='id, parents')
        
        return print ('Temp folder cleaned')

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
   
    def save_data(self,data,format,file_name,folder_name = None):
             
        """
        [DEPRECIATED]
        saves a data array into EXCEL/CSV file
        
        date is a list of dict where dict keys are the names of columns in the output file
        
        """
            
        writer = FileWriter(data)                
        
        file_name = writer.output_file(format,file_name,folder_name)
                    
        return file_name    
        
       