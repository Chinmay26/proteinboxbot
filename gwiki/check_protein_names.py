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
import mygeneinfo
import genewikidata
gw = genewikidata.GeneWikidata()

def setnames():
    source = gw.title_and_entrez()
    for title,entrez in source:
        #print title,entrez
        Wikidata_ID = gw.get_identifier(title)
        #print Wikidata_ID
        
        if Wikidata_ID:
            Item = gw.get_item(Wikidata_ID)
            #get the HGNC name
            gene_json = mygeneinfo.getJson( mygeneinfo.BASE_URL + entrez )
            
            title = mygeneinfo.get(gene_json, 'name')
            print title
            labels = {"en" : title}
            
            Item.editLabels(labels)
            
if __name__ == '__main__':
    setnames()
            
            
