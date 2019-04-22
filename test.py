#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 23:20:06 2019

@author: moby
"""

from Airbnb_Spyder import Airbnb_spyder
from Cookies import url_other_properties


url2 = 'https://www.whatismybrowser.com'


url_other_properties = 'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=2&allow_override%5B%5D=&auto_ib=false&children=0&client_session_id=2c6fc2ba-1145-4bae-8699-8dd160d6efdf&currency=USD&display_currency=USD&experiences_per_grid=20&fetch_filters=true&guests=2&guidebooks_per_grid=20&has_zero_guest_treatment=true&infants=0&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&place_id=ChIJoQ8Q6NNB0S0RkOYkS7EPkSQ&property_type_id%5B%5D=2&property_type_id%5B%5D=3&property_type_id%5B%5D=4&property_type_id%5B%5D=60&property_type_id%5B%5D=40&query=Bali%2C%20Indonesia&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&room_types%5B%5D=Entire%20home%2Fapt&s_tag=EuRdFAxG&satori_version=1.1.0&screen_size=small&search_type=UNKNOWN&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&toddlers=0&version=1.4.8'

spyder = Airbnb_spyder(url_other_properties)
spyder2 = Airbnb_spyder(url2)


#payload = {'price_min':10,'price_max':11}

r = spyder.get_r(spyder.url)          
data = r.json()



r2 = spyder.get_r(spyder2.url)



print (r.url)
#print (dict(r.cookies))
print (r.headers)
property = data['explore_tabs'][0]['sections'][1]['listings'][0]['pricing_quote']
property2 = data['explore_tabs'][0]['sections'][0]
print (property)

k = r.cookies

 
print (dict(k))
#print (r2.content)
print (property2)

        
