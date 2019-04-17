#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 20:18:55 2019

@author: moby
"""

from __future__ import print_function
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import date
import csv
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.http
import pprint
import httplib2

class FileWriter(object):

    def __init__(self, data):

        self.data = data #amke sure the data is in proper format eg list of dict
#        self.fields=list(fields.keys())             
        self.today = str(date.today())
        self.scopes = ['https://www.googleapis.com/auth/drive']

    def output_file(self,out_format,file_name,folder_name = None):

        format = out_format
                
#        if format == 'json' or format is None:
#            import json
#            file_name = 'hotels-in-{country}.txt'.format(
#                country=self.country.replace(" ", "-"))
#            with open(file_name, 'w', encoding='utf-8') as outfile:
#                json.dump(list(self.data), outfile, indent=2, ensure_ascii=False)

        if format == 'excel':

            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            fieldnames = list(self.data[0].keys())
            
            for i in range (1,len(self.data)+2): #iterating via rows
                for j in range (1,len(fieldnames)+1):  #iteration via coloumns
                    if i == 1:
                        ws.cell(row=i, column=j).value = fieldnames[j-1]
                    else:
                        ws.cell(row=i, column=j).value = self.data[i-2].get(fieldnames[j-1])       
                                                                            
            file_to_create_name = '{name}{today}.xlsx'.format(name=file_name,today=self.today)
            
            save_path = os.path.join(os.getcwd(),folder_name)

            complete_name = os.path.join(save_path, file_to_create_name)

            wb.save(complete_name)
                    
        else:

            file_to_create_name = '{name}{today}.csv'.format(name = file_name,today = self.today)

            save_path = os.path.join(os.getcwd(),folder_name)
            complete_name = os.path.join(save_path, file_to_create_name)

            with open(complete_name, mode='w') as csv_file:

                fieldnames = self.data[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
                writer.writeheader()
                writer.writerows(self.data)

            self.file_uploadGDrive_token(complete_name)                            
        
        print ('File -> '+str(file_to_create_name)+' is saved in '+str(complete_name)+' folder')
        
        return file_to_create_name
    
    def file_uploadGDrive_token(self, file_name, folder_name = None):

        #authentication        
        drive = self.access_gDrive()
        
        # Insert a file. Files are comprised of contents and metadata.
        # MediaFileUpload abstracts uploading file contents from a file on disk.
        media_body = googleapiclient.http.MediaFileUpload(
            file_name,
            mimetype='text/csv',
            resumable=True)
        # The body contains the metadata for the file.
        body = {
          'name': 'scraped_info',
          'description': 'db with details about properties'}
        
        # Perform the request and print the result.
        new_file = drive.files().create(body=body, media_body=media_body).execute()
        pprint.pprint(new_file)
                
    def upload_file_to_GoogleDrive_Oath(self, file_name, folder_name):

        id = '1mnTwirEO0jUXGoZgiD9AkUc5LfGaxrWZ' #ID of folder 'Scraped_data'     
    
#        drive = self.access_gDrive()

        g_login = GoogleAuth()  
        g_login.LocalWebserverAuth()
        drive = GoogleDrive(g_login)         

        #get list of folders in the main_folder to upload (id above, folder name 'Scraped_data')

        file_list = drive.ListFile({'q': "'1UN_U6lgrFFHQ1booBtB90FSkWM_ZnohO' in parents and trashed=false"}).GetList()
        
        folder_names = []

        for file in file_list:
        
            folder_names.append(file['title']) #collect names of folders into the list
        
        if folder_name not in folder_names: #check if the upload folder doesn't exist, if not exist create new
        
        #create folder to upload the files on GoogleDrive    

            work_folder = drive.CreateFile({'title': folder_name, \
                "parents":  [{"id": id}], \
                "mimeType": "application/vnd.google-apps.folder"})
            work_folder.Upload()
        
        file_list = drive.ListFile({'q': "'1UN_U6lgrFFHQ1booBtB90FSkWM_ZnohO' in parents and trashed=false"}).GetList()

        #get id of the folder to upload
        
        for file in file_list:
            
            if file['title'] == folder_name:
                
                folder_id = file['id']

        #upload file to the destination folder
            
        with open(file_name,"r") as file:
            file_drive = drive.CreateFile({'title':file_name,\
                "parents": [{"kind": "drive#fileLink","id": folder_id}]})
            file_drive.SetContentFile(file_name) 
            file_drive.Upload()
            print ("The file: " + file_name + " has been uploaded to GoogleDrive into the folder " +str(folder_name))    
            
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
    
        
#data = [{'k':1},{'k':2}]
#file = FileWriter(data)
#file.output_file('excel','test','Data')

#file.file_uploadGDrive_token('price_avail_check_Seminyak_2019-03-16.csv','test_folder')