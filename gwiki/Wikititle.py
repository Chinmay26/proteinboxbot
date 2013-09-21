#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:Chinmay Naik (chin.naik26@gmail.com)

This file is part of ProteinBoxBot.

ProteinBoxBot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ProteinBoxBot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ProteinBoxBot.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib2,json

def getResult():
    '''Obtain the entire set of wikidata gene articles from genewikiplus
    '''
    url = "http://api.genewikiplus.org/map/"
     
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        result  = response.read()
        result = result.decode('utf-8')
        gene_list = json.loads(result)
        
        for entry in gene_list:
            yield (entry['entrez_id'],entry['title_url'])
        
        
      
    except urllib2.HTTPError as e:
        raise e     
    except IOError as e:
        print("Network error")
        raise e
  
def getTitle(entrez):
    '''
    Get the title of wikipedia article from genewikiplus
    Arguments:
    entrez - entrez gene id
    '''
    url = "http://api.genewikiplus.org/map/"
    url = url + str(entrez)
    
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        result  = response.read()
        return result
    except urllib2.HTTPError as e:
        raise e     
    except IOError as e:
        print("Network error")
        raise e
    
