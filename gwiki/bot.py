'''
Created on Jun 20, 2013

@author: chinmay
'''
import pywikibot
import mygeneinfo
import genewikidata
import wikidata,HumanGene

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
            
    def update(self,Item,entrez):

        HGene = mygeneinfo.parse(entrez)
        #print type(HGene)
        CurGene = wikidata.construct_from_item(Item,HumanGene.HumanGene())
        #print CurGene
        return CurGene.updateWith(HGene)
        #self.write(Item,HGene)
        
    def write(self,Item,HGene,updatedClaims):  
        ''' write to wikidata'''
        Claims = Item.get().get('claims')
        Repo = self.genewikidata.data_repo
        #CHECK item.editEntity()
        #print Claims,type(Claims)
        for property in HGene.HGene_properties:
            #only if the property is to be updated
            pfield = HGene.HGene_properties[property]
            if  pfield in updatedClaims:
                if pfield in HGene.multivalue:
                    pass
                #TO-DO mulitvalue claims
                else:
                    val = updatedClaims[pfield][1]
                        #Check the item type
                        #If item page  ex: val = Q20
                        
                    if val.startswith('Q'):
                        valitem = pywikibot.ItemPage(Repo,val)
                        if not valitem.exists():
                            print 'Item not exists'
                        val = valitem
                        
                    #If claim exists and is to be updated
                    if property in Claims:
                        claim =Item.claims[unicode(property)][0]
                        
                    else:#create a claim
                        claim = pywikibot.Claim(Repo,unicode(property))
                    #add the created/updated claim to the wikidata item
                    claim.setTarget(val)
                    Item.addClaim(claim,bot=True)
                    #print pfield, property,val
                    
                
                
                
            
        
        
        #src = HGene.fieldsdict
        #for property_key in HGene.HGene_properties:
            #claim = pywikibot.Claim(Item,HGene.HGene_properties[property_key])
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
            try:
               updatedHGene,summary,updatedClaims = self.update(Item,entrez)
               #print updatedClaims
            except Exception as err:
                print 'handle exceptions like -- Item not exists, property invalidtype '
                
            self.write(Item,updatedHGene,updatedClaims)
            
            
            
            
      

def main():
    BOT = bot(genewikidata.GeneWikidata())
    BOT.run()
    
if __name__ == '__main__':
    main()
    