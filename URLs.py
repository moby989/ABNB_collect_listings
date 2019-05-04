#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:16:10 2019

@author: moby
"""
"""
URLS FOR APIs
"""
### VILLAS

URL_API_villas ={'type':'Villas', 'url':'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=1&allow_override%5B%5D=&auto_ib=false&children=1&fetch_filters=true&guests=2&has_zero_guest_treatment=true&infants=0&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&place_id=ChIJoQ8Q6NNB0S0RkOYkS7EPkSQ&property_type_id%5B%5D=11&query=Bali%2C%20Indonesia&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&room_types%5B%5D=Entire%20home%2Fapt&satori_version=1.1.0&screen_size=small&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&timezone_offset=180&toddlers=0&version=1.4.5'}

### OTHTER PROPERTIES

URL_API_other_properties = {'type':'OtherProperties', 'url':'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=2&allow_override%5B%5D=&auto_ib=false&children=0&client_session_id=2c6fc2ba-1145-4bae-8699-8dd160d6efdf&currency=USD&display_currency=USD&experiences_per_grid=20&fetch_filters=true&guests=2&guidebooks_per_grid=20&has_zero_guest_treatment=true&infants=0&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&place_id=ChIJoQ8Q6NNB0S0RkOYkS7EPkSQ&property_type_id%5B%5D=2&property_type_id%5B%5D=3&property_type_id%5B%5D=4&property_type_id%5B%5D=60&property_type_id%5B%5D=40&property_type_id%5B%5D=42&property_type_id%5B%5D=65&property_type_id%5B%5D=38&property_type_id%5B%5D=22&property_type_id%5B%5D=53&property_type_id%5B%5D=45&property_type_id%5B%5D=35&property_type_id%5B%5D=36&property_type_id%5B%5D=1&property_type_id%5B%5D=43&query=Bali%2C%20Indonesia&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&room_types%5B%5D=Entire%20home%2Fapt&s_tag=EuRdFAxG&satori_version=1.1.0&screen_size=small&search_type=UNKNOWN&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&toddlers=0&version=1.4.8'}


URL_API_shared_properties = {'type':'SharedProperties', 'url': 'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&adults=2&allow_override%5B%5D=&auto_ib=false&children=0&client_session_id=e8e9034a-38af-4cdf-9f62-1e67ded128f6&currency=USD&display_currency=USD&experiences_per_grid=20&fetch_filters=true&guests=2&guidebooks_per_grid=20&has_zero_guest_treatment=true&infants=0&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&place_id=ChIJoQ8Q6NNB0S0RkOYkS7EPkSQ&query=Bali%2C%20Indonesia&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&room_types%5B%5D=Private%20room&room_types%5B%5D=Hotel%20room&room_types%5B%5D=Shared%20room&s_tag=XZGKw-7p&satori_version=1.1.0&screen_size=small&search_type=FILTER_CHANGE&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&toddlers=0&version=1.4.8'}

### REVIEWS

URL_API_reviews = 'https://www.airbnb.ru/api/v2/homes_pdp_reviews?currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id=5749962&_format=for_p3&limit=7&offset=14&order=language_country'


URLs = [URL_API_shared_properties,URL_API_villas,URL_API_other_properties]


