'''
Created on Jun 20, 2013

@author: chinmay
'''
import pywikibot

import mygeneinfo
import genewikidata

try:
    import settings
except ImportError as e:
    print("Configure settings.py")
    raise e

class bot(object):
    #CHECK path to log file. previous bot log file was ---> "http://api.genewikiplus.org/log/submit"
    #log_file_path = "/home/chinmay/GSOC-rough/log1.txt"
    #log=[]
    genewikidata = None
    def __init__(self,genewikidata):
        
        #TO-DO logging
        
        try:
            #TO-DO check for rewrite branch explicitly.
            assert genewikidata
            assert genewikidata.base_site
            assert genewikidata.data_repo
            self.genewikidata = genewikidata
        except AssertionError:
            raise TypeError("Setup pywikipedia-rewrite.")
        
    def logger(self):
        ''' to-do '''
            
    
    def write(self,Item,HGene):  
        ''' write to wikidata'''
        #Handle mutiple value fields like RNA ID etc
        src = HGene.fieldsdict
        for property_key in HGene.HGene_properties:
            claim = pywikibot.Claim(Item,HGene.HGene_properties[property_key])
            #print claim
            #get present value :  claim.getTarget()
             
            #value = HGene.fields[property_key]
            #print type(value),value
            
            #claim.setTarget("5649")
            #Item.addClaim(claim,bot=True) 
        
        
    def run(self):
        ''' Run the bot for human gene items '''
        source = self.genewikidata.title_and_entrez()
        for title,entrez in source:
            #print title,entrez
            Wikidata_ID = self.genewikidata.get_identifier(title)
            #print Wikidata_ID
            Item = self.genewikidata.get_item(Wikidata_ID)
            #print Item
            HGene = mygeneinfo.parse(entrez)
            print type(HGene)
            #TO-DO Get updated HGene info
            self.write(Item,HGene)
            
            
            
      

def main():
    BOT = bot(genewikidata.GeneWikidata())
    BOT.run()
    
if __name__ == '__main__':
    main()
    