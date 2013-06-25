'''
Created on Jun 20, 2013

@author: chinmay
'''

import pywikibot #pywikipedia-rewrite branch
# Populating gene items with the following 6 properties. currently properties can only be accessed through property-id only.
properties ={'Entrez Gene ID': 'p351' , 'Uniprot ID' : 'p352' , 'HGNC ID' : 'p354' , 'Ensembl ID' : 'p594' , 'OMIM ID' : 'p492' , 'EC Number' : 'p591' }
site = pywikibot.Site('en','wikipedia') 

page = pywikibot.Page(site, 'reelin')
item = pywikibot.ItemPage.fromPage(page)
print item.getID()
#sitelinks = []
#labels = []
#d1 = []
#d1.append("Indian Cricket Captain")
#sitelinks.append({"site" : "enwiki" , "title" : u"Uchiha Itachi"})
#labels.append({"language" : "en" , "value" : u"Itachi"})
#data = {'sitelinks' : sitelinks}
if item.exists():
    item.get()
    print "Item exists"
    print item.claims
    
    #claim = pywikibot.Claim(item,'p351')
    #claim.setTarget("5649")
    
    #item.addClaim(claim,bot=True)
    
    #print item.claims[properties['Entrez Gene ID']][0].getTarget()


#print item.claims
#print type(properties['HGNC ID'])
#print item.claims['p352'][1].getTarget()
print 'hello'
