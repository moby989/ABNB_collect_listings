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
url_other_properties = 'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=2&allow_override%5B%5D=&auto_ib=false&children=0&client_session_id=2c6fc2ba-1145-4bae-8699-8dd160d6efdf&currency=USD&display_currency=USD&experiences_per_grid=20&fetch_filters=true&guests=2&guidebooks_per_grid=20&has_zero_guest_treatment=true&infants=0&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&place_id=ChIJoQ8Q6NNB0S0RkOYkS7EPkSQ&property_type_id%5B%5D=2&property_type_id%5B%5D=3&property_type_id%5B%5D=4&property_type_id%5B%5D=60&property_type_id%5B%5D=40&property_type_id%5B%5D=42&property_type_id%5B%5D=65&property_type_id%5B%5D=38&property_type_id%5B%5D=22&property_type_id%5B%5D=53&property_type_id%5B%5D=45&property_type_id%5B%5D=35&property_type_id%5B%5D=36&property_type_id%5B%5D=1&property_type_id%5B%5D=43&query=Bali%2C%20Indonesia&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&room_types%5B%5D=Entire%20home%2Fapt&s_tag=EuRdFAxG&satori_version=1.1.0&screen_size=small&search_type=UNKNOWN&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&toddlers=0&version=1.4.8'


"""
Reviews API
https://www.airbnb.ru/api/v2/homes_pdp_reviews?currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id=5749962&_format=for_p3&limit=7&offset=14&order=language_country


"""

headers = {
'authority': 'www.airbnb.com',
'method': 'GET',
'scheme': 'https',
'accept': 'application/json, text/javascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
'cache-control': 'no-cache',
'pragma': 'no-cache',
'referer': 'https://www.airbnb.com/s/Bali--Indonesia/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJoQ8Q6NNB0S0RkOYkS7EPkSQ&query=Bali%2C%20Indonesia&search_type=FILTER_CHANGE&allow_override%5B%5D=&s_tag=ReRM3Y7C',
'save-data': 'on',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
'x-csrf-token': 'V4$.airbnb.com$V5KUmGhJ0AQ$yjbviXB2lQjGp5qffckUt_0dU4TTOiQrQ-ZL9OsFBCM=',
'x-requested-with': 'XMLHttpRequest'}
          


#headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}

cookies = [
{
    "domain": ".airbnb.com",
    "expirationDate": 1682432511,
    "hostOnly": False,
    "httpOnly": False,
    "name": "__ssid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "ee48d1e2c3a16381870573a4e00df8d",
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
    "value": "V4%24.airbnb.com%24sDM1DtADn-s%24M0zFDRNzC8J3ZYDKQBGA3L7uuh_uT-s7VU8AMJSoY84%3D",
    "id": 2
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1619274109,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_ga",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "GA1.2.1575555834.1556202109",
    "id": 3
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1556202169,
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
    "expirationDate": 1563978107,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_gcl_au",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "1.1.46133464.1556202108",
    "id": 5
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1556288509,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_gid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "GA1.2.456133054.1556202109",
    "id": 6
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1619360503.026049,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_user_attributes",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "%7B%22curr%22%3A%22CAD%22%2C%22guest_exchange%22%3A1.346555%2C%22device_profiling_session_id%22%3A%221556202102--78970eb11f207ff2e9a62272%22%2C%22giftcard_profiling_session_id%22%3A%221556202102--9ed77de742abee650789f37d%22%2C%22reservation_profiling_session_id%22%3A%221556202102--3cb1588cb3b2f3d4753d2a6a%22%7D",
    "id": 7
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1561386102.521808,
    "hostOnly": False,
    "httpOnly": False,
    "name": "016951b48",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "treatment",
    "id": 8
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1556205709,
    "hostOnly": False,
    "httpOnly": False,
    "name": "AMP_TOKEN",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "%24NOT_FOUND",
    "id": 9
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1619274108.089433,
    "hostOnly": False,
    "httpOnly": False,
    "name": "bev",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "1556202102_1oOehBMRaW2DUUKy",
    "id": 10
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
    "id": 11
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1642515707,
    "hostOnly": False,
    "httpOnly": False,
    "name": "cbkp",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "3",
    "id": 12
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1561386102.521669,
    "hostOnly": False,
    "httpOnly": False,
    "name": "cdn_exp_c93eb6109a0d84ec9",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "control",
    "id": 13
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1587824522,
    "hostOnly": False,
    "httpOnly": False,
    "name": "currency",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "USD",
    "id": 14
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
    "id": 15
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1556288503.025779,
    "hostOnly": False,
    "httpOnly": False,
    "name": "jitney_client_session_created_at",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "1556202102",
    "id": 16
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1556288503.025667,
    "hostOnly": False,
    "httpOnly": False,
    "name": "jitney_client_session_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "66745624-d90e-4df6-acfe-f69b6e2d6c6b",
    "id": 17
},
{
    "domain": ".airbnb.com",
    "expirationDate": 1556288516.666799,
    "hostOnly": False,
    "httpOnly": False,
    "name": "jitney_client_session_updated_at",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "1556202116",
    "id": 18
},
{
    "domain": ".airbnb.com",
    "expirationDate": 2186922105,
    "hostOnly": False,
    "httpOnly": False,
    "name": "sdid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "",
    "id": 19
}
]




