"""
File: DomainRequestRules.py
Author: Amit Prakash and See below for other crediting authors (via the source pages/URLs)
Purpose: See how many domain requests created/blocked from cnn.com and macys.com
"""

# Import all necessary modules/libraries
import json
from urllib.parse import urlparse
from tld import get_fld
from tabulate import tabulate
from itertools import chain, starmap

# Define global variables (to store the top level domains)
topLvlList = []

"""
Reads a har file from the filesystem, converts to CSV, then dumps to
stdout.
Credit to "https://gist.githubusercontent.com/zvodd/78d94e2211de96a4ca5d107c0709c3ec/raw/3c463f92412347012a3af2be783102e052a83663/parsehar.py"
"""
def harToDataframe(harfile_path, topLvlDomain):
    """Reads a har file from the filesystem, converts to CSV, then dumps to
    stdout.
    """
    harfile = open(harfile_path, 'rb')
    harfile_json = json.load(harfile)
    i = 0
    for entry in harfile_json['log']['entries']:
        i = i + 1
        url = entry['request']['url']
        urlparts = urlparse(entry['request']['url'])
        size_bytes = entry['response']['bodySize']
        size_kilobytes = float(entry['response']['bodySize'])/1024
        mimetype = 'unknown'
        if 'mimeType' in entry['response']['content']:
            mimetype = entry['response']['content']['mimeType']
        # Print statement with all details commented out, instead we keep track of 3rd party top level domains in topLvlList
        #print ('{},"{}",{},{},{},{}'.format(i, url, urlparts.hostname, size_bytes, 
        #                               size_kilobytes, mimetype))
        if topLvlDomain not in get_fld(url, fail_silently = True) and get_fld(url, fail_silently = True) not in topLvlList:
            topLvlList.append(get_fld(url, fail_silently = True))    

"""
Flattens a JSON into a dictionary with single level key-value pairs
Credit to: https://towardsdatascience.com/how-to-flatten-deeply-nested-json-objects-in-non-recursive-elegant-python-55f96533103d
"""
def flatten_json_iterative_solution(dictionary):
    """Flatten a nested json file"""
    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in json file"""
        # Unpack one level only!!!        
        if isinstance(parent_value, dict):
            for key, value in parent_value.items():
                temp1 = parent_key + '_' + key
                yield temp1, value
        elif isinstance(parent_value, list):
            i = 0 
            for value in parent_value:
                temp2 = parent_key + '_'+str(i) 
                i += 1
                yield temp2, value
        else:
            yield parent_key, parent_value     
    # Keep iterating until the termination condition is satisfied
    while True:
        # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        # Terminate condition: not any value in the json file is dictionary or list
        if not any(isinstance(value, dict) for value in dictionary.values()) and \
           not any(isinstance(value, list) for value in dictionary.values()):
            break
    return dictionary

if __name__ == '__main__':
    # See 3rd party top level domains for macys.com and cnn.com
    harToDataframe('www.macys.com.har', 'www.macys.com')
    macys = topLvlList
    print()
    print(macys)
    print()
    topLvlList = []
    harToDataframe('www.cnn.com.har', 'www.cnn.com')
    cnn = topLvlList
    print(cnn)
    print()
    # See common 3rd party top level domains for macys.com and cnn.com
    both = [value for value in cnn if value in macys]
    print(both)
    print()
    # See 3rd party top level domains for macys.com and cnn.com and how many requests are blocked by Disconnect
    with open('disconnect.json', 'r', encoding = 'utf-8') as json_file:
        data = json.load(json_file) 
    blockList = flatten_json_iterative_solution(data).values()
    cnnBlocks = 0          
    for value in cnn:
         if value in blockList:
            cnnBlocks += 1   
    macysBlocks = 0          
    for value in macys:
         if value in blockList:
            macysBlocks += 1            
    print(tabulate([['Cnn.com', cnnBlocks], ['Macys.com', macysBlocks]], headers=['Website', '# of requests blocked']))
    print()
