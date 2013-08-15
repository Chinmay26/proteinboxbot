'''
Created on Jun 20, 2013

@author: chinmay
'''
import pywikibot,sys,re
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
            

        
    def write(self,Item,Entity,updatedClaims):  
        ''' write to wikidata'''
        Claims = Item.get().get('claims')
        
        Repo = self.genewikidata.data_repo
        if 'description' in updatedClaims:
            des = updatedClaims['description'][1]
            descriptions = {"en":str(des)}
            Item.editDescriptions(descriptions)
        #CHECK item.editEntity()
        #Specify the source using property "imported from"
        imported_from = "p143"
        source_for_claim = pywikibot.Claim(Repo,unicode(imported_from))
        
        
        for property in Entity.properties:
            #only if the property is to be updated
            pfield = Entity.properties[property]
            if  pfield in updatedClaims:
                if pfield in Entity.multivalue:
                    claim = pywikibot.Claim(Repo,unicode(property))
                    multival = updatedClaims[pfield][1]
                    #get the existing values from wikidata
                    curval = []
                    if property in Claims:
                        #total existing values
                        total = len(Item.claims[unicode(property)])
                        for k in range(0,total):
                            existing_val = Item.claims[unicode(property)][k].getTarget()
                            if isinstance(existing_val,pywikibot.ItemPage):
                                existing_val = existing_val.getID()
                            curval.append(existing_val.title())
               

                        
                        
                    for val in multival:
                        #if value exists dont update
                        if val in curval:
                            pass
                        else:
                            val = unicode(val)
                            if (val.startswith('Q') or val.startswith('q')) and property != 'p352':
                                valitem = pywikibot.ItemPage(Repo,val)
                                if not valitem.exists():
                                    print 'Item not exists'
                                val = valitem
                            claim.setTarget(val)
                            
                            #set the source item
                            if pfield in WItem.Item.property_list_sources:
                                source_Item = pywikibot.ItemPage(Repo,WItem.Item.property_list_sources[pfield])
                                source_for_claim.setTarget(unicode(source_Item))
                            # claim = value + source
                            Item.addClaim(claim,bot=True)
                            print val,pfield,Item
                        
                        
                    
                else:
                    val = unicode(updatedClaims[pfield][1])
                    print val
                        #Check the val type
                        #If item page  ex: val = Q20
                        
                    if (val.startswith('Q') or val.startswith('q')) and property != 'p352':
                        valitem = pywikibot.ItemPage(Repo,val)
                        if not valitem.exists():
                            print 'Item not exists'
                        val = valitem
                    existing_val = None
                    #If claim exists and is to be updated
                    if property in Claims:
                        claim =Item.claims[unicode(property)][0]
                        existing_val = Item.claims[unicode(property)][0].getTarget()

                    else:#create a claim
                        claim = pywikibot.Claim(Repo,unicode(property))
                    #add the created/updated claim to the wikidata item
                 
                    claim.setTarget(val)
                    if val != existing_val:
                        #add source for claim
                        if pfield in WItem.Item.property_list_sources:
                            source_Item = pywikibot.ItemPage(Repo,WItem.Item.property_list_sources[pfield])
                            source_for_claim.setTarget(unicode(source_Item))
                        #add the claim
                        Item.addClaim(claim,bot=True)
                        print pfield, property,val,Item
                        
                        
        #adding sources
        
        
        #genloc start,end,chr  ---> genloc assembly
        # ortholog --> species
                    
                
                
                
            
        
        
        #src = HGene.fieldsdict
        #for property_key in HGene.HGene_properties:
            #claim = pywikibot.Claim(Item,HGene.HGene_properties[property_key])
            #print claim
            #get present value :  claim.getTarget()
             
            #value = HGene.fields[property_key]
            #print type(value),value
            
            #claim.setTarget("5649")
            #Item.addClaim(claim,bot=True) 
            

        
        
    def run_HumanProtein(self,HumanProtein,Item):
        ''' Run the bot for human protein items '''

        try:
            CurProtein = wikidata.construct_from_item(Item,WItem.HumanProtein())
            updatedProtein,summary,updatedClaims = CurProtein.updateWith(HumanProtein)
                
               #print updatedClaims
        except Exception as err:
            print 'handle exceptions like -- Item not exists, property invalidtype '
                
        self.write(Item,updatedProtein,updatedClaims)
            
    def run_HumanGene(self,HumanGene):
        
        key  = HumanGene.fieldsdict['Entrez Gene ID']
        title = HumanGene.fieldsdict['Name']
        res = wikidata.search_Item(title)
        if res:
            entrez = 'p351'
            ID = wikidata.search_claim(res,entrez,key)
            Item = self.genewikidata.get_item(ID)
        else:
            print "ERROR! CHECK TITLE SEARCH"
            sys.exit(1)
        try:
            CurHGene = wikidata.construct_from_item(Item, WItem.HumanGene())
            updatedHGene,summary,updatedClaims = CurHGene.updateWith(HumanGene)
              #print updatedClaims
        except Exception as err:
            print 'handle exceptions like -- Item not exists, property invalidtype '
                
        self.write(Item,updatedHGene,updatedClaims) 
            
    def run_MouseGene(self,MouseGene):
        
        key  = MouseGene.fieldsdict['Entrez Gene ID']
        title = MouseGene.fieldsdict['Name']
        res = wikidata.search_Item(title)
        if res:
            entrez = 'p351'
            ID = wikidata.search_claim(res,entrez,key)
            Item = self.genewikidata.get_item(ID)
        else:
            print "ERROR! CHECK TITLE SEARCH"
            sys.exit(1)
        
        try:
            CurMGene = wikidata.construct_from_item(Item, WItem.MouseGene())
            updatedMGene,summary,updatedClaims = CurMGene.updateWith(MouseGene)
              #print updatedClaims
        except Exception as err:
            print 'handle exceptions like -- Item not exists, property invalidtype '
                
        self.write(Item,updatedMGene,updatedClaims)  
            
    def run_MouseProtein(self,MouseProtein):
        
        key  = MouseProtein.fieldsdict['Uniprot ID']
        title = MouseProtein.fieldsdict['Name']
        res = wikidata.search_Item(title)
        if res:
            uniprot = 'p352'
            ID = wikidata.search_claim(res,uniprot,key)
            Item = self.genewikidata.get_item(ID)
        else:
            print "ERROR! CHECK TITLE SEARCH"
            sys.exit(1)
        
        
        try:
            CurMProtein = wikidata.construct_from_item(Item, WItem.MouseProtein())
            updatedMProtein,summary,updatedClaims = CurMProtein.updateWith(MouseProtein)
              #print updatedClaims
        except Exception as err:
            print 'handle exceptions like -- Item not exists, property invalidtype '
                
        self.write(Item,updatedMProtein,updatedClaims)         
            
            
            
    def run(self):
         
        source = self.genewikidata.title_and_entrez()
      
        for title,entrez in source:
            #construct items from mygeneinfo
            HumanGene,HumanProtein,MouseGene,MouseProtein = mygeneinfo.Parse(entrez)
            
            #print title,entrez
            Wikidata_ID = self.genewikidata.get_identifier(title)
            #print Wikidata_ID
            if Wikidata_ID:
                Item = self.genewikidata.get_item(Wikidata_ID)
         
         
            self.run_HumanProtein(HumanProtein,Item)
         
            self.run_HumanGene(HumanGene)
                
            self.run_MouseProtein(MouseProtein)
                
            self.run_MouseGene(MouseGene)
        
            
            
            
            
      

def main():
    
    BOT.run()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= '''Handling Gene wikidata items''')
    
    #parser.add_argument('--HumanGene', action = 'HGENE', help = 'update HUMAN GENE wikidata items' )
    
    #parser.add_argument('--HumanProtein', action = 'HGENE', help = 'update Human Protein wikidata items')
    
    BOT = bot(genewikidata.GeneWikidata())
    main()
    