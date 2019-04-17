#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 23:40:41 2019

@author: moby
"""

###URLS

### API search results in Airbnb - Villas
url_villas = 'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=1&allow_override%5B%5D=&auto_ib=false&children=1&fetch_filters=true&guests=2&has_zero_guest_treatment=true&infants=0&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&place_id=ChIJoQ8Q6NNB0S0RkOYkS7EPkSQ&property_type_id%5B%5D=11&query=Bali%2C%20Indonesia&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&room_types%5B%5D=Entire%20home%2Fapt&satori_version=1.1.0&screen_size=small&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&timezone_offset=180&toddlers=0&version=1.4.5'

### API search - other property types (except for villas) but private
url_other_properties = 'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=0&allow_override%5B%5D=&auto_ib=false&children=0&client_session_id=069cd99b-7ccd-4f9d-a119-c12d2100ea6a&currency=USD&display_currency=USD&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&infants=0&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&place_id=ChIJoQ8Q6NNB0S0RkOYkS7EPkSQ&property_type_id%5B%5D=2&property_type_id%5B%5D=1&property_type_id%5B%5D=53&property_type_id%5B%5D=40&property_type_id%5B%5D=45&property_type_id%5B%5D=42&property_type_id%5B%5D=35&property_type_id%5B%5D=3&property_type_id%5B%5D=43&property_type_id%5B%5D=38&property_type_id%5B%5D=36&property_type_id%5B%5D=65&property_type_id%5B%5D=4&property_type_id%5B%5D=22&property_type_id%5B%5D=60&query=Bali%2C%20Indonesia&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&room_types%5B%5D=Entire%20home%2Fapt&s_tag=CscW1mGQ&satori_version=1.1.0&screen_size=small&search_type=UNKNOWN&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&toddlers=0&version=1.4.8'


"""
Reviews API
https://www.airbnb.ru/api/v2/homes_pdp_reviews?currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id=5749962&_format=for_p3&limit=7&offset=14&order=language_country


"""




headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0)\
          AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 \
          Safari/537.36'}        

#update cookies to use in cloud version

cookies = [
{
    "domain": ".airbnb.com",
    "expirationDate": 1681721174,
    "hostOnly": False,
    "httpOnly": False,
    "name": "__ssid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "742b75970e8208a0cef96da0b3c0d7c",
    "id": 1
},
{
    "domain": ".airbnb.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "_csrf_token",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": True,
    "storeId": "0",
    "value": "V4%24.airbnb.com%24J9dZlEcE6ZM%24Ckio3dohdESr-kEhsZiCjOaZdrwdP4UGWr1YuOxzOqA%3D",
    "id": 2
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1618562792,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_ga",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "GA1.2.322154298.1555490777",
    "id": 3
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1555490836,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_gat",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "1",
    "id": 4
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1563266774,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_gcl_au",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "1.1.1233365001.1555490774",
    "id": 5
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1555577192,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_gid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "GA1.2.1828193638.1555490777",
    "id": 6
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1618649177.259369,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_user_attributes",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "%7B%22curr%22%3A%22CAD%22%2C%22guest_exchange%22%3A1.337225%2C%22device_profiling_session_id%22%3A%221555490777--62730dd53471f17858310067%22%2C%22giftcard_profiling_session_id%22%3A%221555490777--daae8eb961df41d13b414ea9%22%2C%22reservation_profiling_session_id%22%3A%221555490777--a0ae78119a71028c286ea5ab%22%7D",
    "id": 7
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1555494376,
    "hostOnly": False,
    "httpOnly": False,
    "name": "AMP_TOKEN",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "%24NOT_FOUND",
    "id": 8
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1618562797.561908,
    "hostOnly": False,
    "httpOnly": False,
    "name": "bev",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "1555490773_QY9Bs5aYI0qCQZhS",
    "id": 9
},
{
    "domain": ".airbnb.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "cache_state",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": True,
    "storeId": "0",
    "value": "0",
    "id": 10
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1641804393,
    "hostOnly": False,
    "httpOnly": False,
    "name": "cbkp",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "3",
    "id": 11
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1560674791.158182,
    "hostOnly": False,
    "httpOnly": False,
    "name": "cdn_exp_c93eb6109a0d84ec9",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "control",
    "id": 12
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1560674791.158049,
    "hostOnly": False,
    "httpOnly": False,
    "name": "cdn_exp_ea80bc3c056098b3b",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "treatment",
    "id": 13
},
{
    "domain": ".airbnb.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "flags",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": True,
    "storeId": "0",
    "value": "0",
    "id": 14
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1555577176.854079,
    "hostOnly": False,
    "httpOnly": False,
    "name": "jitney_client_session_created_at",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "1555490776",
    "id": 15
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1555577176.853941,
    "hostOnly": False,
    "httpOnly": False,
    "name": "jitney_client_session_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "eef5337d-7810-49c9-b68e-61f4e3a5d294",
    "id": 16
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1555577197.562035,
    "hostOnly": False,
    "httpOnly": False,
    "name": "jitney_client_session_updated_at",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "1555490797",
    "id": 17
},
{
    "domain": ".airbnb.com",
    "expirationDate": 2185894381,
    "hostOnly": False,
    "httpOnly": False,
    "name": "sdid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "",
    "id": 18
}
]
