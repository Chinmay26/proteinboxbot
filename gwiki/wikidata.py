'''
Created on Jul 3, 2013

@author: chinmay
'''
import WItem
import pywikibot
import genewikidata
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
    
    #labels definitely exist
    label = Item.labels['en']
    Entity.setField('Name',label)
    #descriptions may not exist
    if 'descriptions' in Item.get():
        if 'en' in Item.descriptions:
            des = Item.descriptions['en']
            Entity.setField('description',des)
                
    for claim in Item.claims:
        if claim in Entity.properties:
            if len(Item.claims[claim]) > 1 :
                #TO-DO  work on  qualifiers
                multival = []
                total = len(Item.claims[claim])
                for k in range(0,total):
                    existing_val = Item.claims[claim][k].getTarget()
                    if isinstance(existing_val,pywikibot.page.ItemPage):
                        match = re.search(r'\[\[wikidata\:([\w]*)\]\]',str(existing_val))
                        if match:
                        #print match.group(1)
                            existing_val = str(match.group(1))
                    
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

#search for the item with given title
def search_Item(title):
    
    
    mysite = pywikibot.Site("wikidata","wikidata")
    
    params = { 'action' :'wbsearchentities' ,
                'format' : 'json' ,              
              'language' : 'en',
               'limit' : '4',      #retreive four items
                'type' : 'item',
                'search': '',
              }
    
    params['search']= title
    request = api.Request(site=mysite,**params)
    data = request.submit()
    if data['success']:
        return data['search'] 

#create an item with an label
def create_Item(title):
    
    mysite = pywikibot.Site("wikidata","wikidata")
    repo = mysite.data_repository()
    labels = []
    labels.append({"language":"en","value" : title})
    data = {
        "labels" : labels 
        }
    New = repo.editEntity({},data,bot=False)
    ID = New['entity']['id']
    return ID

def search_claim(Items,property,value):
    mysite = pywikibot.Site("wikidata","wikidata")
    repo = mysite.data_repository()
    Identifier = []
    for val in Items:
        ID = val['id']
        item = pywikibot.ItemPage(repo,ID)
        item.get()
        #check if the claim exists in item
        if property in item.claims:
            #check for correct value of claim
            if unicode(value) == item.claims[property][0].getTarget():
                Identifier = item.getID()
                break
            
    return Identifier
    
    
def addClaim(ID,property,value):
    mysite = pywikibot.Site("wikidata","wikidata")
    repo = mysite.data_repository()
    item = pywikibot.ItemPage(repo,ID)
    item.get()
    claim = pywikibot.Claim(repo,property)
    claim.setTarget(value)
    item.addClaim(claim, bot = True)
    

#def search_Item(title):

#    mysite = pywikibot.Site("wikidata","wikidata")
#    url = "http://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search=%s&language=en&type=item&limit=4",%(title)
#    req = urllib2.Request(url)
#    u = urllib2.urlopen(req)

            
        
#if __name__ == '__main__':
#    ID = search_Item('jhfuf6fuwqw')
#    print ID

    
  
  
#if __name__ == '__main__' :
    
#    site = pywikibot.Site('en','wikipedia')
    
#    repo = site.data_repository()
#    item = pywikibot.ItemPage(repo,'Q414043')
#    construct_from_item(item, HumanGene.HumanGene())