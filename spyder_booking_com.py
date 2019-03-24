#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:46:02 2019

@author: moby
"""

import requests
from bs4 import BeautifulSoup
import re
import time
#import csv
from spyder_main import Spyder
#from file_writer import FileWriter

class Booking_com_spyder(Spyder):
 
    def __init__(self,url):
        
        Spyder.__init__(self)
       
        self.url = url   
#        self.session = requests.Session()        
        self.field = "uf" #"uf" stands for cities in booking.com        
        self.delay = 10 #set delay to call url to avoid blocking from website        
        self.tags={ \
        'name':'sr-hotel__name',\
        'type':'sr-hotel__type',\
        'price_format':'price',\
        'cur':'price',\
        'price':'price',\
        'd_price':'price',\
        'room_type':'room_link',\
        'extras':'sr_room_reinforcement',\
        'mark':'bui-review-score__badge',\
        'n_reviews':'bui-review-score__text',\
        'n_lookers':'sr_no_desc_users',\
        'demand':'rollover-s1',\
        'demand3':'rollover-s2',\
        'area3':'sr_card_address_line',\
        'area':'distfromdest',\
        'area2':'pub_trans',\
        'max_pax':'sr_max_occupancy',\
        'room_size':'sr-rt-size',\
        'address':'data-coords',\
        'link':'hotel_name_link',\
        'stars':'bk-icon-wrapper',\
        'promo':'bk-icon -iconset-thumbs_up',\
        'promo2':'ranking_vb_tag'}        
    
        self.filter_codes = {'ht_id': ['Villas', 'Guest houses', 'Hotels', 'Homestays', 'Holiday parks', 'Resorts', 'Bed and breakfasts', 'Hostels', 'Apartments', 'Holiday homes', 'Lodges', 'Campsites', 'Country houses', 'Luxury tents', 'Boats', 'Capsule hotels', 'Farm stays', 'Economy hotels', 'Motels'], 
        'concise_unit_type': [], 'class': ['1 star', '2 stars', '3 stars', '4 stars', '5 stars', 'Unrated'],
        'popular_activities': ['Massage', 'Bicycle rental (additional charge)', 'Diving', 'Hiking', 'Cycling'], 
        'hr_24': ['Front desk open 24/7'], 'ht_beach': ['Beachfront'], 
        'popular_nearby_landmarks': ['Ubud Market', 'Ubud Palace', 'Lotus Cafe', 'Sarong Restaurant', 'Bebek Bengil', 'Ku De Ta', 'Ubud Monkey Forest', 'Bridges Restaurant', 'Potato Head Beach Club', 'Metis Restaurant', 'Kuta Square', 'Legian Art Market', 'Batu Jimbar Café', 'Poppies Lane 1', 'Hard Rock Cafe', 'Poppies Lane 2', 'Vue Beach Club', 'Echo Beach', 'Mushroom Bay', 'Dream Beach', 'Sky Garden', 'Cocoon Beach Club', 'Le Mayeur Museum', 'Jimbaran Corner', 'Padang Padang Beach', 'Yellow Bridge', 'Padangbai Bay', 'Pasifika Museum', 'Bali Collection', 'Elephant Cave', 'Blue Lagoon', 'Geger Beach', 'Uluwatu Temple', 'Lake Batur', 'Krisna Funtastic Land', 'Gamat Bay', 'Bebek Bengil Nusa Dua', 'Pandawa Beach', 'The Rock Bar', 'Krisna Water Sports', 'Pulaki Temple', 'Bali Museum', 'Aling Aling Waterfall', 'Bali Zoo', 'Tanah Lot Temple', 'Art Centre', 'Sekumpul Waterfall', 'Goa Giri Putri Temple', 'Atuh Beach', 'Kintamani', 'Tegenungan Waterfall', "Angel's Billabong"], 
        'review_score': ['Superb: 9+', 'Very good: 8+', 'Good: 7+', 'Pleasant: 6+', 'No rating'], 
        'hotelfacility': ['Parking', 'Restaurant', 'Pets allowed', 'Room service', 'Fitness centre', 'Non-smoking rooms', 'Airport shuttle', 'Facilities for disabled guests', 'Family rooms', 'Spa and wellness centre', 'BBQ facilities', 'Free WiFi', 'Electric vehicle charging station', 'Swimming pool'],
        'uf': ['Ubud', 'Seminyak', 'Canggu', 'Sanur', 'Kuta', 'Jimbaran', 'Uluwatu', 'Nusa Lembongan', 'Legian', 'Denpasar', 'Nusa Penida', 'Nusa Dua', 'Amed', 'Lovina', 'Kerobokan', 'Pemuteran', 'Candidasa', 'Tabanan', 'Munduk', 'Gianyar', 'Sidemen', 'Tanah Lot', 'Tejakula', 'Tegalalang', 'Kintamani', 'Tulamben'],
        'accessible_facilities': ['Wheelchair accessible', 'Toilet with grab rails', 'Higher level toilet', 'Lower bathroom sink', 'Emergency cord in bathroom', 'Visual aids: Braille', 'Visual aids: Tactile signs', 'Auditory guidance'], 
        'chaincode': ['Airy Rooms', 'Aston International Hotels, Resorts & Residences', 'Avilla Hospitality', 'Elite Havens', 'HARRIS Hotels & Resorts', 'RedDoorz', 'Santika Indonesia Hotels & Resorts', 'Swiss-Belhotel International', 'ZEN Premium', 'ZEN Rooms'], 
        'accessible_room_facilities': ['Entire unit located on ground floor', 'Upper floors accessible by lift', 'Entire unit wheelchair accessible', 'Toilet with grab rails', 'Adapted bath', 'Roll in shower', 'Walk in shower', 'Raised toilet', 'Lowered sink', 'Emergency cord in bathroom', 'Shower chair']}
        
        self.cookies = {'bkng':'11UmFuZG9tSVYkc2RlIyh9YfDNyGw8J7nzPnUG3Pr%2Bfv6cIBgOuhXRxiGbDY%2BvrMf9UxnBcXoi8bNMyvHmlJl3OQxV%2B9SZ3u0vW%2FXNv6X%2BCI2o4C%2BokDk4%2BSkGBbrbMnaw8jW4L5vyHygjIdJXtcj7xJD259qe7iF1EM5PS6gR76Q5r91bsFdwn9LseUHPqrh%2B76m4SQsy2niTRCFKXHxJxw%3D%3D'}     
    
    def filter_codes(self):
    
        ######Result
        
        """"""""""""
        {'ht_id': ['Villas', 'Guest houses', 'Hotels', 'Homestays', 'Holiday parks', 'Resorts', 'Bed and breakfasts', 'Hostels', 'Apartments', 'Holiday homes', 'Lodges', 'Campsites', 'Country houses', 'Luxury tents', 'Boats', 'Capsule hotels', 'Farm stays', 'Economy hotels', 'Motels'], 
        'concise_unit_type': [], 'class': ['1 star', '2 stars', '3 stars', '4 stars', '5 stars', 'Unrated'],
        'popular_activities': ['Massage', 'Bicycle rental (additional charge)', 'Diving', 'Hiking', 'Cycling'], 
        'hr_24': ['Front desk open 24/7'], 'ht_beach': ['Beachfront'], 
        'popular_nearby_landmarks': ['Ubud Market', 'Ubud Palace', 'Lotus Cafe', 'Sarong Restaurant', 'Bebek Bengil', 'Ku De Ta', 'Ubud Monkey Forest', 'Bridges Restaurant', 'Potato Head Beach Club', 'Metis Restaurant', 'Kuta Square', 'Legian Art Market', 'Batu Jimbar Café', 'Poppies Lane 1', 'Hard Rock Cafe', 'Poppies Lane 2', 'Vue Beach Club', 'Echo Beach', 'Mushroom Bay', 'Dream Beach', 'Sky Garden', 'Cocoon Beach Club', 'Le Mayeur Museum', 'Jimbaran Corner', 'Padang Padang Beach', 'Yellow Bridge', 'Padangbai Bay', 'Pasifika Museum', 'Bali Collection', 'Elephant Cave', 'Blue Lagoon', 'Geger Beach', 'Uluwatu Temple', 'Lake Batur', 'Krisna Funtastic Land', 'Gamat Bay', 'Bebek Bengil Nusa Dua', 'Pandawa Beach', 'The Rock Bar', 'Krisna Water Sports', 'Pulaki Temple', 'Bali Museum', 'Aling Aling Waterfall', 'Bali Zoo', 'Tanah Lot Temple', 'Art Centre', 'Sekumpul Waterfall', 'Goa Giri Putri Temple', 'Atuh Beach', 'Kintamani', 'Tegenungan Waterfall', "Angel's Billabong"], 
        'review_score': ['Superb: 9+', 'Very good: 8+', 'Good: 7+', 'Pleasant: 6+', 'No rating'], 
        'hotelfacility': ['Parking', 'Restaurant', 'Pets allowed', 'Room service', 'Fitness centre', 'Non-smoking rooms', 'Airport shuttle', 'Facilities for disabled guests', 'Family rooms', 'Spa and wellness centre', 'BBQ facilities', 'Free WiFi', 'Electric vehicle charging station', 'Swimming pool'],
        'uf': ['Ubud', 'Seminyak', 'Canggu', 'Sanur', 'Kuta', 'Jimbaran', 'Uluwatu', 'Nusa Lembongan', 'Legian', 'Denpasar', 'Nusa Penida', 'Nusa Dua', 'Amed', 'Lovina', 'Kerobokan', 'Pemuteran', 'Candidasa', 'Tabanan', 'Munduk', 'Gianyar', 'Sidemen', 'Tanah Lot', 'Tejakula', 'Tegalalang', 'Kintamani', 'Tulamben'],
        'accessible_facilities': ['Wheelchair accessible', 'Toilet with grab rails', 'Higher level toilet', 'Lower bathroom sink', 'Emergency cord in bathroom', 'Visual aids: Braille', 'Visual aids: Tactile signs', 'Auditory guidance'], 
        'chaincode': ['Airy Rooms', 'Aston International Hotels, Resorts & Residences', 'Avilla Hospitality', 'Elite Havens', 'HARRIS Hotels & Resorts', 'RedDoorz', 'Santika Indonesia Hotels & Resorts', 'Swiss-Belhotel International', 'ZEN Premium', 'ZEN Rooms'], 
        'accessible_room_facilities': ['Entire unit located on ground floor', 'Upper floors accessible by lift', 'Entire unit wheelchair accessible', 'Toilet with grab rails', 'Adapted bath', 'Roll in shower', 'Walk in shower', 'Raised toilet', 'Lowered sink', 'Emergency cord in bathroom', 'Shower chair']}
        
        """"""""""""
        
        filter_dict = {}

        
        page = self.get_script(self.url)
    
        fields = ['ht_id','concise_unit_type',
                  'class','popular_activities',
                  'hr_24','ht_beach','ht_id',
                  'popular_nearby_landmarks',
                  'review_score','hotelfacility','uf','accessible_facilities',
                  'chaincode','accessible_room_facilities']
                                
        for field in fields:
            
            item_names = []
            filters = page.find_all(attrs={"data-name":field})
            
            for filter in filters:
            
                try:
                
                    item_names.append(filter.find('span',class_= re.compile('filter_label')).get_text().strip())
            
                except AttributeError:
                
                    'nothing'
            
            filter_dict[field] = item_names
            
        return filter_dict
    
    def get_name_filters(self, field, url = None):
        
        #FTF = fields to filter
        # need to break down the whole search into pieces eg cities names
        #    Booking.com only allows to get 1000 results

        page = self.get_script2(self.get_r(self.url))
                
        FTF_list = page.find_all(attrs={"data-name":field}) #find info about cities in the area. returns list with different info for each city
        
        FTF_numbers = []
        FTF_names = []
        FTF_codes = []
        
        for FTF in FTF_list:
            FTF_codes.append(FTF['data-value']) ##'data-value' is a code for a specific city in booking.com
            name_string = FTF.get_text().strip().split()
            FTF_names.append(''.join(filter(str.isalpha, name_string))) ##make list of names to use after
            FTF_numbers.append(int(FTF.get_text().strip().split()[-1])) ##take the number of properties which exist for a particular code
        
        return FTF_codes,FTF_names,FTF_numbers


    def make_url_list(self,FTF_codes,FTF_names):
    
        #make the list of urls to iterate later. booking.com allows only 1000 properties in one search so need the whole db to break down in small pieces and find urls lists for these small groups

        urls = []   #list of dictionaries to make (number,city,url). later write into file and use for parsing.
        number = 1    #use later to count the name of pages to parse

    
        for i in range(len(FTF_codes)): #iterate through cities
    
            payload = {'nflt':'uf%3D'+str(FTF_codes[i])+'%3B'} #iterate through codes ('cities')
            r = requests.get(self.url, params=payload)
#            print(r.url)
            time.sleep(self.delay)
            soup = BeautifulSoup(r.content,'lxml')
#            text = soup.find('h1',class_='sorth1').get_text() #get total quantiry of properties for this code
#            number_properties = int(''.join(re.findall(r'\d+', text)))
#            print (number_properties)            
#            if number_properties > 1000:  #for big groups drill down in smaller groups by another filter field
               
            classes = self.get_name_filters("class", r.url)[0]
            n_classes = len(classes)

            for n in range(n_classes):
                payload = {'nflt':'uf%3D'+str(FTF_codes[i])+'%3B'+'class%3D'+str(n)+'%3B'} #iterate through codes ('classes')
                r2 = requests.get(self.url, params=payload)
#                    print(r2.url)
                time.sleep(self.delay)
                soup = BeautifulSoup(r2.content,'lxml')
                text2 = soup.find('h1',class_='sorth1').get_text() #!!!! call the function instead!!! get total quantiry of properties for this code
                number_properties2 = int(''.join(re.findall(r'\d+', text2)))

                if number_properties2 > 1000:                    
                    print('number of properties in this class > 1000') ##if number of properties >1000 in the class need to drill down the groups deeper. 
                    
                number_pages2 = number_properties2//50 + 1 #number of pages to parse for the group
                for c in range(number_pages2):
                    url = r2.url +';rows=50'+';offset='+str(c*50) #make list of urls for the group
                    urls.append({'number': number, 'class':n,'city': FTF_names[i], 'url': url})
                    number += 1
                
#            else:   #collect URLs for cities groups where number of properries less than 1000
    
#            number_pages = number_properties//50 + 1        
#            for j in range(number_pages):
#                url = r.url +';rows=50'+';offset='+str(j*50)
#                urls.append({'number': number, 'class':n, 'city':  FTF_names[i], 'url': url})
#                number += 1
#    
        return urls

        
    def parse_single_page(self,page,star = None):
    
        
        property_list = []
        properties_number = []
        properties = page.find_all(attrs={"data-et-view": " eWHJbWPNZWEHXT:5"})
        properties_number = len(properties)
        
#        print(properties_number)
                            
        for property in properties:
            
            s_property = {}
    ##################################   ID  ######################################
            s_property['id'] = property['data-hotelid'].strip()
    ##################################   NAME  ####################################
            s_property['name'] = property.find('span',class_=re.compile(self.tags['name'])).contents[0].strip()
    ##################################   EXTRA  ###################################
            try:
                s_property['extras'] = property.find('sup',class_=re.compile(self.tags['extras'])).contents[0].strip()
            except AttributeError:
                s_property['extras'] = 'no data'
    ##################################   LINK  ####################################
            s_property['link'] = 'https://www.booking.com'+str(property.find('a',class_=re.compile(self.tags['link']))['href'].strip())
    ##################################   TYPE  ####################################    
            try:
                s_property['type'] = property.find('span',class_=re.compile(self.tags['type'])).contents[0].strip()
            except AttributeError:
                s_property['type'] = 'no data'
    ##########################   GPS  #################################
            s_property['address'] = property.find(attrs={self.tags['address']: True})[self.tags['address']]
    ##################################   AREA  ####################################    
            try:
#                s_property['area3'] = property.find('a',class_=re.compile(self.tags['area3'])).get_text().strip()[:-14]
                s_property['area3'] = property.find(class_ = self.tags['area3']).get_text().replace('Show on map','').strip()
            except AttributeError:
                s_property['area3'] = 'no data'
            try:
                s_property['area'] = property.find('span',class_=re.compile(self.tags['area'])).contents[0].strip()
            except AttributeError:
                s_property['area'] = 'no data'
            try:
                s_property['area2'] = property.find('span',class_=re.compile(self.tags['area2'])).contents[0].strip()
            except AttributeError:
                s_property['area2'] = 'no data'
    ##############################   DEMAND INFO  ##@@@@@##########################    
            try:
                s_property['n_lookers'] = property.find('div',class_=re.compile(self.tags['n_lookers'])).contents[0].strip()
            except AttributeError:
                s_property['n_lookers'] = 'no data'
            try:
                s_property['demand'] = property.find('div',class_=re.compile(self.tags['demand'])).get_text().strip()
            except AttributeError:
                s_property['demand'] = 'no data'
            try:
                s_property['demand3'] = property.find('div',class_=re.compile(self.tags['demand3'])).contents[0].strip()
            except AttributeError:
                s_property['demand3'] = 'no data'
    ##################################   REVIEWS  #################################
            try:
                s_property['mark'] = property.find('div',class_=re.compile(self.tags['mark'])).contents[0]
                s_property['n_reviews'] = property.find('div',class_=re.compile(self.tags['n_reviews'])).contents[0]
            except AttributeError:
                s_property['mark'] = 'no data'
                s_property['n_reviews'] = 'no data'
    ##################################   ROOM TYPE  ###############################
            try:
                s_property['room_type'] = property.find('span',class_=re.compile(self.tags['room_type'])).contents[0].strip()
            except AttributeError:
                s_property['room_type'] = 'no data'
            try:
                s_property['max_pax'] = property.find('div',class_=re.compile(self.tags['max_pax'])).get_text().strip()
            except AttributeError:
                s_property['max_pax'] = 'no data'                                
            try:
                s_property['room_size'] = property.find('span',class_=re.compile(self.tags['room_size'])).contents[0].strip()
            except AttributeError:                                
                s_property['room_size'] = 'no data'                                
    ##################################   PRICE  ###################################    
            try:
                s_property['price_format'] = property.find('strong',class_=re.compile(self.tags['price_format']))['aria-label']
                s_property['cur'] = property.find('strong',class_=re.compile(self.tags['price'])).contents[1].contents[0].strip()[:4]
                s_property['price'] = property.find('strong',class_=re.compile(self.tags['price'])).contents[1].contents[0].strip()[4:].replace(',','')
                s_property['d_price'] = int(int(s_property['price'])/int(s_property['price_format'][10:11].strip()))
            except (AttributeError,TypeError):
                s_property['price_format'] = 'sold out'
                s_property['cur'] = 'sold out'
                s_property['price']='sold out'
                s_property['d_price'] = 'sold out'                    
    
    ##################################   OTHER INFO  ##############################

            try:
                s_property['stars'] = property.find('i',class_=re.compile(self.tags['stars'])).get_text().strip()
            except AttributeError:
                s_property['stars'] = 'no data'
            try:
                s_property['promo'] = property.find('svg',class_=re.compile(self.tags['promo'])).next.next.next.get_text()
            except AttributeError:
                s_property['promo'] = 'no data'
            try:
                s_property['promo2'] = property.find('span',class_=re.compile(self.tags['promo2'])).get_text().strip()
            except AttributeError:
                s_property['promo2'] = 'no data'                
            try:
                s_property['promo2'] = property.find('span',class_=re.compile(self.tags['promo2'])).get_text().strip()
            except AttributeError:
                s_property['promo2'] = 'no data'
                
                s_property['class'] = star
                                
    
    #filling up the dictionary for properties
            
            property_list.append(s_property)
#    
#            for tag in self.tags.keys():
#    
#                property_list.setdefault(id[-1],[])
#                property_list[id[-1]].append(locals()[tag])
#       
        return property_list,properties_number    
    
    def parse_price_avail(self, page):
                      
    ###gets - page (Beautifulsoup object)
    ###returns - dicts with prices&number of properties for which the info is collected on the page
    
        tags={ \
        'name':'sr-hotel__name',
        'type':' sr-hotel__type ',
        'price_format':'price',
        'cur':'price',
        'price':'price',
        'd_price':'price',
        'room_type':'room_link',
        'mark':'bui-review-score__badge',
        'n_reviews':'bui-review-score__text',
        'address':'address',
        'max_pax':'bui-u-sr-only',
        'sleep_arrang':'bui-u-full-width',
        'link':'hotel_name_link'}
          

        property_list = []
        properties_number = []
        price_range = ''
#        properties = page.find_all(attrs={"data-et-view":"cJaQWPWNEQEDSVWe:1"})        
        properties = page.find_all('div', class_=re.compile('sr_item txp-pmc-prop'))
        properties_number = len(properties)
        city = page.find(attrs={"data-name":"uf",'aria-checked':"true"}).get_text().strip()        
        group = page.find_all(attrs={"data-name":"pri",'aria-checked':"true"})
        for g in group:
            price_range += g.get_text().strip()
                            
        for property in properties:
            s_property = {}
            s_property['city'] = city
            s_property['group'] = price_range
            s_property['id'] = property['data-hotelid'].strip() ##id in booking.com
            s_property['name'] = property.find('span',class_=re.compile(tags['name'])).contents[0].strip()#name

            try:
                s_property['type'] = property.find('span',class_=re.compile(tags['type'])).contents[0].strip()#type - villa, hotel, etc.
            except AttributeError:
                s_property['type'] = 'no data'    
            try:
                number_bedrooms = property.find('div',class_=re.compile(tags['sleep_arrang'])).get_text().split('and')[0]
                s_property['sleep_arrang'] = int(''.join(re.findall(r'\d+', number_bedrooms)))
            except (AttributeError, ValueError):
                s_property['sleep_arrang'] = 'no data'

#                max_pax = property.find('span',class_=re.compile(tags['max_pax'])).get_text()
#                s_property['sleep_arrang'] = int(''.join(re.findall(r'\d+', max_pax)))//2
    
            try:
                s_property['room_type'] = property.find('span',class_=re.compile(tags['room_type'])).strong.get_text().strip()
            except AttributeError:
                s_property['room_type'] = 'no data'
    
            try:
                s_property['price_format'] = property.find('strong',class_=\
                          re.compile(tags['price_format']))['aria-label']
                price = s_property['price_format'].split(':')[1]
                days = s_property['price_format'].split(':')[0]
                s_property['cur'] = (''.join(re.findall(r'\D+', price)))
                s_property['price'] = int(''.join(re.findall(r'\d+', price)))
                s_property['d_price'] = int(s_property['price'])/int(''.\
                          join(re.findall(r'\d+', days)))
            except (AttributeError,TypeError):
                s_property['price_format'] = 'sold out'
                s_property['cur'] = 'sold out'
                s_property['price']='sold out'
                s_property['d_price'] = 'sold out'                    
    
            #Other info (optional)
    
            try:           
                s_property['address'] = property.find('div',class_ =\
                          re.compile(tags['address'])).get_text().\
                          replace('Show on map','').replace('Beach nearby','')\
                          .strip()#street name                
            except AttributeError:
                s_property['address'] = 'no data'
            try:
                s_property['mark'] = property.find('div',class_=\
                          re.compile(tags['mark'])).contents[0].strip()#review score
                s_property['n_reviews'] = property.find('div',class_=\
                          re.compile(tags['n_reviews'])).contents[0].\
                          strip()#number of reviews
            except AttributeError:
                s_property['mark'] = 'no data'
                s_property['n_reviews'] = 'no data'
                
            s_property['link'] = 'https://www.booking.com'+str(property.find\
                      ('a',class_=re.compile(self.tags['link']))['href'].strip())                                
                              
            #filling up the dictionary for properties
            
            property_list.append(s_property)
        
        return property_list,properties_number  


    def properties_counter (self,page):
        
        #gets Beautifulsoup object - page
        #returns Total number of properties which booking.com indicates as available on that page
        
        text = page.find('div',class_=re.compile('sr_header')).h1.get_text()
        text2 = text.split('including')[0] #gets the string 'Bali:X properties including' but drops everything after including
        avail = int(''.join(re.findall(r'\d+', text2))) #gets all the numbers from the string and combines them together

        print ('avail = ' + str(avail))
        
        return avail
    
    def make_url_list_prices_trend(self,city,type, dates, price_group1,price_group2):
        
        #returns - urls_list for pages to parse and the first page to parse, avail - number of properties available for these days 
     
        print('Getting codes for city names')                  
        (a1,b1,c1) = self.get_name_filters("uf") #find code for city name eg Seminyak
        print('Getting codes for hotel accomodations types')
        (a2,b2,c2) = self.get_name_filters("ht_id") #find code for property type eg villa or hotel
        

        code_city = a1[b1.index(city)]
        code_type = a2[b2.index(type)]                        
        
        start_date = dates[0]
        finish_date = dates[1]
                            
        nflt = 'ht_id%3D{param0}%3Buf%3D{param1}%3Boos%3D1%3B'.format(param0 = code_type, param1 = code_city)
        
#        pri%3D{param2}%3Bpri%3D{param3}%3B    
        
        payload = {'checkin':start_date,'checkout':finish_date,'nflt':nflt,'rows':50}
        
        r = self.get_r(self.url, payload)        
        
        first_page = self.get_script2(r)
                
        avail = self.properties_counter(first_page)
        if avail > 1000:
            raise Exception('The number of pages in this property group is {}. Can miss some properties'.format(avail)) 

        n_pages = avail//50 + 1
                
        url_list = [{'number':'1','city':city,'url':r.url}]
        
        for i in range(1,n_pages):

            url = {}            
            url['number'] = i + 1
            url['city'] = city            
            url['url'] = r.url + '&offset='+str(i*50) #make list of urls for the group
            
            url_list.append(url)                                    
        
        return url_list, first_page, avail

        
    def collect_data(self,urls,max_page = None):
    
        final_db = []
                  
        for url in urls[:]:  
    
            page_url = url.get('url')
            page = self.get_script(page_url)
            data_from_one_page,number_properties = self.parse_page_price_selected(page)
            print(number_properties)
            final_db += data_from_one_page             
            print ('parsed '+str(urls.index(url)+1)+' pages.'+'\n Got info for '+str(number_properties)+' properties')     

       
        return final_db             

