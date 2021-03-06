new_directories = ['PayScale Code ONET Affinities',
                    'Unclassified ONET Job Affinities',
                    'Generic PayScale Code ONET Affinities',
                    '2012 NAICS',
                    '2013 IPEDS',
                    'CIP CODE', 
                    'Employers', 
                    'Industries',
                    'Jobs Research Center', 
                    'Cities',
                    'CityStateCountries',
                    'Old ONET Files',
                    'Question Affinities',
                    'Metro Affinities', 
                    'Question Affinities',
                    'Search Survey Affinities', 
                    'Question Affinities',
                    'Question Affinities',
                    'AutoPropertyGenerated', 
                    'MSAs',
                    'Question Affinities', 
                    'Degrees No Higher',
                    'ELEARNERS', 
                    'Canadian Metros',
                    'Combined Statistical Areas', 
                    'Countries',
                    'States', 
                    'Occupational Area Affinities',
                    'Practice Area Affinities',
                    'Monster Location Affinities',
                    'Unable To Classify',
                    'OLD NAICS', 
                    'OLD IPEDS',
                    'SEARCH Affinities', 
                    'Regional Affinities',
                    'PayScale Code ONET Affinities',
                    'Breadth 10 Job Rollups',
                    'Counties',
                    'Breadth 15 Job Affinities', 
                    'Breadth 20 Old Job Affinities',
                    'Breadth 30 Old Job Affinities',
                    'Breadth 40 Old Job Affinities',
                    'Breadth 50 Old Job Affinities',
                    'Degrees No Higher',
                    'Historical Affinities',
                    'Possible Duplicates']

directory_keys = {'All Other PayScale Code': 'PayScale Code ONET Affinities',
                  'Unclassified': 'Unclassified ONET Job Affinities',
                  'Generic': 'Generic PayScale Code ONET Affinities',
                  '2012 NAICS CODE': '2012 NAICS',
                  '2013 IPEDS ID': '2013 IPEDS',
                  'Question': 'Question Affinities', 'Degrees no higher': 'Degrees No Higher',
                  'All People in': 'Unable To Classify',
                  'SURVEY People in': 'Unable to Classify', 'NAICS CODE': 'OLD NAICS', 'IPEDS ID': 'OLD IPEDS',
                  'SEARCH': 'SEARCH Affinities',
                  'PayScale Code': 'PayScale Code ONET Affinities',
                  'County': 'Counties',
                  'All': 'Historical ALL Affinities',
                  'People with': 'Question Affinities', 'SEARCH SURVEY': 'Search Survey Affinities',
                  'People Who': 'Question Affinities', 'People Asked': 'Question Affinities',
                  'Unable To Classify': 'Unable To Classify', 'Region': 'Regional Affinities',
                  'Combined Statistical Area': 'Combined Statistical Areas',
                  "historical": "Historical Affinities"}

in_line_keys = {'breadth\\10': 'Breadth 10 Job Rollups', 'breadth\\15': 'Breadth 15 Job Affinities',
                'breadth\\20': 'Breadth 20 Old Job Affinities', 'breadth\\30': 'Breadth 30 Old Job Affinities',
                'breadth\\40': 'Breadth 40 Old Job Affinities', 'breadth\\50': 'Breadth 50 Old Job Affinities',
                'field\\degree only': 'Degrees No Higher'}

easy_classify = {'CIP CODE': 'CIP CODE', 'Industry=': 'Industries', 'Valid CityStateCountry': 'CityStateCountries',
                 'Job=': 'Jobs Research Center', 'Location Country=': 'Countries',
                 'AutoPropertyGenerated': 'AutoPropertyGenerated', 'Location State=': 'States',
                 'Practice Area=': 'Practice Area Affinities', 'Metropolitan Statistical Area': 'MSAs',
                 'Combined Statistical Area': 'Combined Statistical Areas',
                 'Monster Location': 'Monster Location Affinities', 'ELEARNERS': 'ELEARNERS',
                 'Canada Metropolitan Area': 'Canadian Metros', 'Occupational Area': 'Occupational Area Affinities',
                 'ONET 7': 'Old ONET Files', "ONET BAK": "Old ONET Files",
                 'People in the ': 'Metro Affinities', 'Location City=': 'Cities',
                 'Employer Name': 'Employers'}