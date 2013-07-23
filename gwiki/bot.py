'''
Created on Jun 20, 2013

@author: chinmay
'''
import pywikibot
import mygeneinfo,argparse
import genewikidata
import wikidata,WItem

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
            
    def updateProtein(self,Item,entrez):

        HProtein = mygeneinfo.parse_HumanProtein(entrez)
        #print type(HGene)
        CurProtein = wikidata.construct_from_item(Item,WItem.HumanProtein())
        #print CurGene
        return CurProtein.updateWith(HProtein)
        #self.write(Item,HGene)
        
    def write(self,Item,HProtein,updatedClaims):  
        ''' write to wikidata'''
        Claims = Item.get().get('claims')
        Repo = self.genewikidata.data_repo
        #CHECK item.editEntity()
        #print Claims,type(Claims)
        for property in HProtein.properties:
            #only if the property is to be updated
            pfield = HProtein.properties[property]
            if  pfield in updatedClaims:
                if pfield in HProtein.multivalue:
                    claim = pywikibot.Claim(Repo,unicode(property))
                    multival = updatedClaims[pfield][1]
                    #get the existing values from wikidata
                    curval = []
                    if property in Claims:
                        #total existing values
                        total = len(Item.claims[unicode(property)])
                        for k in range(0,total):
                            existing_val = Item.claims[unicode(property)][k].getTarget()
                            curval.append(existing_val)
               

                        
                        
                    for val in multival:
                        #to-do handle wikidata items as values
                        if val in curval:
                            pass
                        else:
                            claim.setTarget(val)
                            Item.addClaim(claim,bot=True)
                            print val,pfield,Item
                        
                        
                    
                else:
                    val = updatedClaims[pfield][1]
                    print val
                        #Check the val type
                        #If item page  ex: val = Q20
                        
                    if val.startswith('Q') and property != 'p352':
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
                    print pfield, property,val,Item
                    
                
                
                
            
        
        
        #src = HGene.fieldsdict
        #for property_key in HGene.HGene_properties:
            #claim = pywikibot.Claim(Item,HGene.HGene_properties[property_key])
            #print claim
            #get present value :  claim.getTarget()
             
            #value = HGene.fields[property_key]
            #print type(value),value
            
            #claim.setTarget("5649")
            #Item.addClaim(claim,bot=True) 
        
        
    def run_HumanProtein(self):
        ''' Run the bot for human protein items '''
        source = self.genewikidata.title_and_entrez()
        for title,entrez in source:
            #print title,entrez
            Wikidata_ID = self.genewikidata.get_identifier(title)
            #print Wikidata_ID
            Item = self.genewikidata.get_item(Wikidata_ID)
            #print Item
            try:
               updatedProtein,summary,updatedClaims = self.updateProtein(Item,entrez)
               #print updatedClaims
            except Exception as err:
                print 'handle exceptions like -- Item not exists, property invalidtype '
                
            self.write(Item,updatedProtein,updatedClaims)
            
            
            
            
      

def main():
    
    BOT.run_HumanProtein()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= '''Handling Gene wikidata items''')
    
    #parser.add_argument('--HumanGene', action = 'HGENE', help = 'update HUMAN GENE wikidata items' )
    
    #parser.add_argument('--HumanProtein', action = 'HGENE', help = 'update Human Protein wikidata items')
    
    BOT = bot(genewikidata.GeneWikidata())
    main()
    