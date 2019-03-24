#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 19:39:41 2019

@author: moby
"""

from spyder_Airbnb import Airbnb_spyder


def collect_db(url,price_ranges = None):

    my_spyder = Airbnb_spyder(url)
    
#    price_ranges = my_spyder.getPriceRangeWrapper(url)
    print(price_ranges)
    
    property_list = []
    hist = {}
    number_t = 0
    
    for price in price_ranges:
        number = 0
        ofs = 0
        last_page_flag = True
        
        while last_page_flag:        

            payload = {'price_min':price[0],'price_max':price[1],'items_offset':ofs}
            
            r = my_spyder.get_r(url,payload)    
            data = r.json()                                                                                                    
            print(r.text())
            number = my_spyder.getNumberProp(data)            
            print('Parsing pages for prices from ' + str(price[0]) + ' until ' + str(price[1]))
            print('Getting info for ' + str(number) + ' properties.')
            
            hist[str(number)] = (price[0],price[1])
            print (data['explore_tabs'][0]['sections'][0]['listings'][0])            
            property_list.extend(my_spyder.parsePage(data))
                            
            ofs +=50
            last_page_flag = data['explore_tabs'][0]['pagination_metadata']['has_next_page']
    
        number_t += number
    
    
    my_spyder.save_data(property_list,'excel','villas_Bali_',folder_name = None)
    my_spyder.save_data(property_list,'csv','villas_Bali_',folder_name = None)
    print (hist)
    print('total number of properties -->'+str(number_t))
    
    return property_list
#    return price_ranges


url = 'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=1&allow_override%5B%5D=&auto_ib=false&children=1&fetch_filters=true&guests=2&has_zero_guest_treatment=true&infants=0&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&place_id=ChIJoQ8Q6NNB0S0RkOYkS7EPkSQ&property_type_id%5B%5D=11&query=Bali%2C%20Indonesia&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&room_types%5B%5D=Entire%20home%2Fapt&satori_version=1.1.0&screen_size=small&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&timezone_offset=180&toddlers=0&version=1.4.5'

price_ranges = [(0, 41, 306), (42, 51, 266), (52, 59, 267), (60, 66, 280), (67, 70, 445), (71, 74, 359), (75, 79, 401), (80, 84, 224), (85, 88, 619), (89, 91, 600), (92, 96, 493), (97, 99, 709), (100, 104, 535), (105, 107, 617), (108, 112, 404), (113, 117, 614), (118, 121, 521), (122, 126, 438), (127, 130, 374), (131, 137, 328), (138, 141, 408), (142, 145, 318), (146, 151, 359), (152, 159, 327), (160, 167, 274), (168, 174, 311), (175, 179, 333), (180, 188, 241), (189, 197, 259), (198, 204, 321), (205, 214, 297), (215, 228, 309), (229, 245, 298), (246, 254, 311), (255, 274, 312), (275, 289, 271), (290, 309, 290), (310, 335, 298), (336, 355, 290), (356, 390, 293), (391, 424, 310), (425, 474, 293), (475, 530, 307), (531, 613, 292), (614, 734, 290), (735, 899, 290), (900, 1210, 291), (1211, 2000, 239), (2001, 10000, 56)]

data = collect_db(url, price_ranges[:2])

#my_spyder = Airbnb_spyder(url)

#payload = {'price_min':0,'price_max':41}
        
#r = my_spyder.get_r(url,payload)
        
#data = r.json()
          
#dict = my_spyder.parsePage(data)


#url_property = 'https://www.airbnb.com/api/v2/pdp_listing_booking_details?_format=for_web_with_date&_intents=p3_book_it&_interaction_type=pageload&_p3_impression_id=p3_1553199852_mWV1RBQF73GRuS8K&_parent_request_uuid=d6eb13d2-b6bb-4ce6-bad4-04a18906a1ff&check_in=2019-03-29&check_out=2019-03-30&currency=USD&force_boost_unc_priority_message_type=&guests=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id=8692788&locale=en&number_of_adults=2&number_of_children=0&number_of_infants=0&show_smart_promotion=0'
#range = my_spyder.getPriceRangeWrapper(url)
#print(range)

        
            
        

                
        
        
    
    
    
