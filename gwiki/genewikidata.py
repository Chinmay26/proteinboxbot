'''
Created on Jun 21, 2013

@author: chinmay
'''
import pywikibot
#can query wikidata to get property-id's as well. Seems redundant when we have pre-defined properties
properties ={'Entrez Gene ID': 'p351' , 
             'HGNC ID' : 'p354' ,
              'OMIM ID' : 'p492' }
#TO-DO  Include other properties
#Q4115189 - sandbox
#Obtain the gene article from wikipedia

site = pywikibot.Site('en', 'wikipedia')
page = pywikibot.Page(site,'Alpha-1-B glycoprotein')
wikipedia_item = pywikibot.ItemPage.fromPage(page)
#Obtain the item from wikidata
repo = pywikibot.Site('wikidata' , 'wikidata').data_repository()
item = pywikibot.ItemPage(repo,wikipedia_item.getID())#currently can access wikidata items through ID's only



item.get()

#print item.claims
#claim = pywikibot.Claim(repo,'p352')
#claim.setTarget("5649")    
#item.addClaim(claim,bot=True)

#checks whether the item has claims
#for key in properties:
 #   property_id = properties[key]
  #  if item.claims.has_key(property_id):
   #     print property_id
#item.claims.has_key(k)
#dicts = item.claims.viewkeys() #gives property id's present in the item
#print type(dicts)

