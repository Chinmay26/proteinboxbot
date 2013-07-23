'''
Created on Jul 3, 2013

@author: chinmay
'''
import WItem
import pywikibot
from pywikibot.data import api
import re,urllib2
try:
    import settings
except ImportError:
    print(''' Configure settings.py''')
    raise

def construct_from_item(Item,Entity ):
    Item.get()
    
   # for property in HGene.HGene_properties:
        #print HGene.HGene_properties[property]
   #     if Item.claims[HGene.HGene_properties[property]].exists():
   #         if property in HGene.multivalue:
   #             print property
   #         else:
   #             pvalue = Item.claims[HGene.HGene_properties[property]]
   #             print pvalue
                
                
    for claim in Item.claims:
        if claim in Entity.properties:
            if len(Item.claims[claim]) > 1 :
                #TO-DO  work on  qualifiers
                multival = []
                total = len(Item.claims[claim])
                for k in range(0,total):
                    existing_val = Item.claims[claim][k].getTarget()
                    multival.append(existing_val)
                
                pval = multival
            
            else:
                pval = Item.claims[claim][0].getTarget()
                #print pval , claim , type(pval)
                if isinstance(pval,pywikibot.page.ItemPage):
                    match = re.search(r'\[\[wikidata\:([\w]*)\]\]',str(pval))
                    if match:
                        #print match.group(1)
                        pval = str(match.group(1))
                    
            field_name = Entity.properties[claim]
            Entity.setField(field_name,pval)
                
    return Entity


def search_Item(title):
    
    mysite = pywikibot.Site("wikidata","wikidata")
    
    params = { 'action' :'wbsearchentities' ,
                'format' : 'json' ,              
              'language' : 'en',
               'limit' : '4',
                'type' : 'item',
                'search': '',
              }
    params['search']= title
    request = api.Request(site=mysite,**params)
    data = request.submit()
    
    return data 

#def search_Item(title):

#    mysite = pywikibot.Site("wikidata","wikidata")
#    url = "http://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search=%s&language=en&type=item&limit=4",%(title)
#    req = urllib2.Request(url)
#    u = urllib2.urlopen(req)

            
        
if __name__ == '__main__':
    ID = search_Item('jhfuf6fuwqw')
    print ID

    
  
  
#if __name__ == '__main__' :
    
#    site = pywikibot.Site('en','wikipedia')
    
#    repo = site.data_repository()
#    item = pywikibot.ItemPage(repo,'Q414043')
#    construct_from_item(item, HumanGene.HumanGene())