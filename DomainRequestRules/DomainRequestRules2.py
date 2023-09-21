"""
File: DomainRequestRules2.py
Author: Amit Prakash and See below for other crediting authors (via the source pages/URLs)
Purpose: See how many domain requests created/blocked from cnn.com using specified AdBlockRules
"""

# Import all necessary modules/libraries
import json
from adblockparser import AdblockRules
from urllib.parse import urlparse
from tld import get_fld
from tabulate import tabulate

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
        # print ('{},"{}",{},{},{},{}'.format(i, url, urlparts.hostname, size_bytes, 
        #                               size_kilobytes, mimetype))
        if topLvlDomain not in get_fld(url, fail_silently = True) and get_fld(url, fail_silently = True) not in topLvlList:
            topLvlList.append([mimetype, get_fld(url, fail_silently = True)])    

if __name__ == '__main__':
    # See 3rd party top level domains for cnn.com
    harToDataframe('www.cnn.com.har', 'www.cnn.com')
    cnn = topLvlList
    rule1Blocks = 0
    rule2Blocks = 0
    rule3Blocks = 0
    rules = AdblockRules(['||*cookiesync?*'])
    for k, v in topLvlList:
        if(rules.should_block(v)):
            rule1Blocks += 1
    rules = AdblockRules(['||scorecardresearch.com$image'])
    for k, v in topLvlList:
        if("image" in k and rules.should_block(v, {'image': True})):
            rule2Blocks += 1
    rules = AdblockRules(['||doubleclick.net$script'])
    for k, v in topLvlList:
        if("script" in k and rules.should_block(v, {'script': True})):
            rule3Blocks += 1
    print(tabulate([['||*cookiesync?*', rule1Blocks], ['||scorecardresearch.com$image', rule2Blocks], ['||doubleclick.net$script', rule3Blocks]], headers=['Rule', '# of requests blocked']))
    print()