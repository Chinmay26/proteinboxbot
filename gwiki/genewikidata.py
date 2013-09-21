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

import pywikibot
import re
from pywikibot.data import api

try:
    import settings
except ImportError as e:
    print("Could not import settings")
    raise e
    

#Obtain the gene article from wikipedia
class GeneWikidata(object):
    code_site = settings.Code_site
    family = settings.Code_site
    base_site = None
    data_repo = None
    category = None
    def __init__(self):
        '''login to wikidata '''
        self.base_site = pywikibot.Site(code = self.code_site, fam = self.family, user = None, sysop = None, interface =None)
        #fam = family
        #sysop = system operator 
        #TO-DO  After getting bot flag, update login here by using sysop
        api.LoginManager(site = self.base_site , user = settings.wikidata_user , password = settings.wikidata_password ).login()
        #self.base_site.login()
        self.data_repo = self.base_site.data_repository()
        
    def get_item(self,Wikidata_ID):
        '''
        Get the item(claims,description,aliases,sitelinks) from wikidata identifier
        '''
        item = pywikibot.ItemPage(self.data_repo , Wikidata_ID)
        item.get()
        return item
    
    def articles(self):
        self.category = pywikibot.Category(pywikibot.Link(settings.CATEGORY_NAME,defaultNamespace=14)) 
        #NOTICE  total = None  when running for the entire set of PBB templates
        articles = self.category.articles(recurse = False, step = None, total = 20, content = True, namespaces = None)
        #content = True retreive the contents of gene wikiarticles
        #recurse = False Dont go into subcategories
        #total  retreive the many number of pages 
        for article in articles:
            yield article
   
    def entrez(self):    
        for article in self.articles():
            match = re.search(r'\{\{\s?PBB\s?\|\s?geneid=\s?([\d]*)\s?\}\}', article.text)
            if match :
                yield (match.group(1)) 
            
    def title_and_entrez(self):
        for article in self.articles():
            match = re.search(r'\{\{\s?PBB\s?\|\s?geneid=\s?([\d]*)\s?\}\}', article.text)
            if match :
                yield (article.title(),match.group(1)) 

        
    def get_identifier(self,title):
        ''' temporary wikipedia site object to get WIKIDATA ITEM identifier from linked wikipedia page '''
        site = pywikibot.Site('en', 'wikipedia')
        page = pywikibot.Page(site,title)
        item = pywikibot.ItemPage.fromPage(page)
        if item.exists():
            return item.getID()
        
