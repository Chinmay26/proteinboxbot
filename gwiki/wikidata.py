'''
Created on Jul 3, 2013

@author: chinmay
'''
import HumanGene
import pywikibot
import re
try:
    import settings
except ImportError:
    print(''' Configure settings.py''')
    raise

def construct_from_item(Item, HGene):
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
        if claim in HGene.HGene_properties:
            if len(Item.claims[claim]) > 1 :
                #TO-DO  work on muitvalue claims and qualifiers
                multival = []
            
            else:
                pval = Item.claims[claim][0].getTarget()
                #print pval , claim , type(pval)
                if isinstance(pval,pywikibot.page.ItemPage):
                    match = re.search(r'\[\[wikidata\:([\w]*)\]\]',str(pval))
                    if match:
                        #print match.group(1)
                        pval = str(match.group(1))
                    
                field_name = HGene.HGene_properties[claim]
                HGene.setField(field_name,pval)
                
    return HGene
                         
            
        
    

    
  
  
#if __name__ == '__main__' :
    
#    site = pywikibot.Site('en','wikipedia')
    
#    repo = site.data_repository()
#    item = pywikibot.ItemPage(repo,'Q414043')
#    construct_from_item(item, HumanGene.HumanGene())