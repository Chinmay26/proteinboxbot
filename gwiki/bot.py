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


import pywikibot,sys,re,ipdb
import mygeneinfo,argparse,datetime
import genewikidata
import wikidata,WItem,Wikititle

try:
    import settings
except ImportError as e:
    print("Configure settings.py")
    raise e

class bot(object):
    '''
    Bot  to handle updation/creation of wikidata items
    '''

    log=[]
   
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
        
    def logger(self,exit_status,Item,msg):
        ''' Log entries to log file with path specified below 
        Arguments:
        -exit_status : 0 -success , 1 -failure
        -Item  : Updated wikidata item
        -msg   : message contains error cause or updated claim values
        '''
        fmt='%Y-%m-%d   %H-%M-%S'
	ts=datetime.datetime.now().strftime(fmt)
        log_entry = {
                    "status"  : exit_status,
                    "Item"    : Item,
                    "message" : msg,
		    "timestamp" : ts
                    }
        self.log.append(log_entry)
        print log_entry
        with open("/var/www/wikidatabot/logs.txt","a") as logfile:
            logfile.write(str(log_entry)+'\n')
            

        
    def write(self,Item,Entity,updatedClaims):  
        '''     write to wikidata
        Arguments:
        -Item : Wikidata item to write to
        -Entity : Canbe HumanGene,HumanProtein,MouseGene,MouseProtein
        -updatedClaims : Claims to be written to this wikidata item
	Handles multivalue-claims and single value claims seperately.
	Writes source(reference) to claim after adding claim.

        '''
	#ipdb.set_trace()
	item_dict = Item.get()
        Claims = item_dict['claims']
	modifiedClaims=[]
        
        Repo = self.genewikidata.data_repo
        if 'description' in updatedClaims:
            des = updatedClaims['description'][1]
            descriptions = {"en":str(des)}
            Item.editDescriptions(descriptions)
	    modifiedClaims.append('description')
   	
	if 'aliases' in updatedClaims:
	    alval = updatedClaims['aliases'][1]
            aliases_dict=[]
 	    if 'aliases' in item_dict:
                if 'en' in item_dict['aliases']:
                    aliases_dict=item_dict['aliases']['en']
	    if alval not in aliases_dict:
		aliases_dict.append(alval)
	    	als = {"en":aliases_dict}
	    	Item.editAliases(als)
	    	modifiedClaims.append('aliases')
		
        #Specify the source using property "imported from"
        imported_from = "P143"
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
                                existing_val = existing_val.title()
                            curval.append(existing_val)
               

                        
                        
                    for val in multival:
                        #if value exists dont update
                        if val in curval:
                            pass
                        else:
                            val = unicode(val)
                            if (val.startswith('Q') or val.startswith('q')) and property != 'P352':
                                valitem = pywikibot.ItemPage(Repo,val)
                                if not valitem.exists():
                                    print 'Item not exists'
                                val = valitem
                            claim.setTarget(val)
                            
                            #set the source item
                            if pfield in WItem.Item.property_list_sources:
                                source_Item = pywikibot.ItemPage(Repo,WItem.Item.property_list_sources[pfield])
                                source_for_claim.setTarget(source_Item)
                            # claim = value + source
                            Item.addClaim(claim,bot=True)
                            if pfield in WItem.Item.property_list_sources:
                                claim.addSource(source_for_claim)
        #                    print val,pfield,Item
                            if pfield not in modifiedClaims:
				modifiedClaims.append(pfield)
                        
                    
                else:
                    val = unicode(updatedClaims[pfield][1])
                    print val
                        #Check the val type
                        #If item page  ex: val = Q20
                        
                    if (val.startswith('Q') or val.startswith('q')) and property != 'P352':
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
                            source_for_claim.setTarget(source_Item)
                        #add the claim
                        Item.addClaim(claim,bot=True)
                        if pfield in WItem.Item.property_list_sources:
                            claim.addSource(source_for_claim)
                        print pfield, property,val,Item
                        if pfield not in modifiedClaims:
			    modifiedClaims.append(pfield)
                 
        if modifiedClaims:
            message = "Successfully edited claims "
            for claim in modifiedClaims:
                message =  message + "{field} :  {oldval} ---> {newval}   ".format(field=claim,
                                                                             oldval=updatedClaims[claim][0],newval=updatedClaims[claim][1])
        else:
            message = "No modification done"
        
        #ipdb.set_trace()    
        return message
      
        
        
    def run_HumanProtein(self,HumanProtein,WID):
        ''' Run the bot for human protein items
        Arguments:
        -HumanProtein : HumanProtein object constructed from mygeneinfo.api
        -Item         : HumanProtein Wikidata Item

	The default linked Item to Wikipedia article is Human Protein Wikidata Item.
	Thus, pull this item from wikidata through the wikipedia article.
         '''

        try:
            Item=self.genewikidata.get_item(WID)		
            CurProtein = wikidata.construct_from_item(Item,WItem.HumanProtein())
            updatedProtein,summary,updatedClaims = CurProtein.updateWith(HumanProtein)
                

        except Exception as err:
            if isinstance(err,wikidata.WikidataConstructItem):
                message = 'WikidataParseFailure. ErrorCause:{e} '.format(e=err)
                raise wikidata.WikidataConstructItem(message)
            else:
                raise err
        #ipdb.set_trace()        
        message = self.write(Item,updatedProtein,updatedClaims)
        self.logger(0, Item.getID(), msg = message )
            
    def run_HumanGene(self,HumanGene):
        '''  Run the bot for the Human Gene item
        Arguments:
        HumanGene : HumanGene object constructed from mygeneinfo.api
        
	Search for already created Human Gene item by wikidata label. If fails, as backup search from "Also known as"(alias) field
	which has values as "entrez:1234".
        '''
        
        key  = HumanGene.fieldsdict['Entrez Gene ID']
        title = HumanGene.fieldsdict['Name']
        res = wikidata.search_Item(title)
	entrez='P351'
        if res:
            ID = wikidata.search_claim(res,entrez,key)
	    if not ID:
		res=wikidata.search_Item('entrez:'+str(key))
		ID=wikidata.search_claim(res,entrez,key)
            if not ID:
                message = 'Failed to retreive HumanGene item with entrez:{EZ} from search result:{RES}'.format(RES=res,EZ=key)
                raise wikidata.WikidataSearchError(message)
            Item = self.genewikidata.get_item(ID)
        else:
            message = 'Failed to search by label already created HumanGene Wikidata item with EntrezID={val}'.format(val=key)
            raise wikidata.WikidataSearchError(message)
        try:
            CurHGene = wikidata.construct_from_item(Item, WItem.HumanGene())
            updatedHGene,summary,updatedClaims = CurHGene.updateWith(HumanGene)
              #print updatedClaims
        except Exception as err:
            if isinstance(err,wikidata.WikidataConstructItem):
                message = 'WikidataParseFailure. ErrorCause:{e} '.format(e=err)
                raise wikidata.WikidataConstructItem(message)
            else:
                raise err
        #ipdb.set_trace()        
        message = self.write(Item,updatedHGene,updatedClaims)
        self.logger(0, Item.getID(), msg = message ) 
            
    def run_MouseGene(self,MouseGene):
        ''' Run the bot for Mouse Gene item
        Arguments:
        MouseGene : MouseGene item constructed from mygeneinfo.api

        Search for already created Mouse Gene item by wikidata label. If fails, as backup search from "Also known as"(alias) field
        which has values as "entrez:1234".

        ''' 
        key  = MouseGene.fieldsdict['Entrez Gene ID']
        title = MouseGene.fieldsdict['Name']
        res = wikidata.search_Item(title)
	entrez='P351'
        if res:
            ID = wikidata.search_claim(res,entrez,key)
            if not ID:
                res = wikidata.search_Item('entrez:'+str(key))
                ID = wikidata.search_claim(res,entrez,key)
            if not ID:
                message = 'Failed to retreive MouseGene item with entrez:{EZ} from search result:{RES}'.format(RES=res,EZ=key)
                raise wikidata.WikidataSearchError(message)
            Item = self.genewikidata.get_item(ID)
        else:
            message = 'Failed to search already created MouseGene Wikidata item with EntrezID={val}'.format(val=key)
            raise wikidata.WikidataSearchError(message)
        
        try:
            CurMGene = wikidata.construct_from_item(Item, WItem.MouseGene())
            updatedMGene,summary,updatedClaims = CurMGene.updateWith(MouseGene)
              #print updatedClaims
        except Exception as err:
            if isinstance(err,wikidata.WikidataConstructItem):
                message = 'WikidataParseFailure. ErrorCause:{e} '.format(e=err)
                raise wikidata.WikidataConstructItem(message)
            else:
                raise err
        #ipdb.set_trace()        
        message = self.write(Item,updatedMGene,updatedClaims)
        self.logger(0, Item.getID(), msg = message )  
            
    def run_MouseProtein(self,MouseProtein):
        ''' Run the bot for Mouse Protein item
        Arguments:
        MouseProtein : MouseProtein item constructed from mygeneinfo.api

        Search for already created Human Gene item by wikidata label. If fails, as backup search from "Also known as"(alias) field
        which has values as "uniprot:1234".
        ''' 
        
        key  = MouseProtein.fieldsdict['Uniprot ID']
        title = MouseProtein.fieldsdict['Name']
        res = wikidata.search_Item(title)
	uniprot='P352'
        if res:
            ID = wikidata.search_claim(res,uniprot,key)
            if not ID:
                res=wikidata.search_Item('uniprot:'+str(key))
                ID=wikidata.search_claim(res,uniprot,key)
            if not ID:
                message = 'Failed to retreive MouseProtein item with uniprot:{UP} from search result:{RES}'.format(RES=res,UP=key)
                raise wikidata.WikidataSearchError(message)
            Item = self.genewikidata.get_item(ID)
        else:
            message = 'Failed to search already created MouseProtein Wikidata item with UniprotID={val}'.format(val=key)
            raise wikidata.WikidataSearchError(message)
        
        
        try:
            CurMProtein = wikidata.construct_from_item(Item, WItem.MouseProtein())
            updatedMProtein,summary,updatedClaims = CurMProtein.updateWith(MouseProtein)
              #print updatedClaims
        except Exception as err:
            if isinstance(err,wikidata.WikidataConstructItem):
                message = 'WikidataParseFailure. ErrorCause:{e} '.format(e=err)
                raise wikidata.WikidataConstructItem(message)
            else:
                raise err
        #ipdb.set_trace()        
        message = self.write(Item,updatedMProtein,updatedClaims)
        self.logger(0, Item.getID(), msg = message )         
            
           
    def report(self,run,success_runs,fail_runs,elog):
	'''
	Generate report for bot run
	''' 
	log=[]
	fmt='%Y-%m-%d   %H-%M-%S'
        ts=datetime.datetime.now().strftime(fmt)
        log_entry = {
                    "Total Processed "  : run,
                    "Total Success Runs"    : success_runs,
                    "Total Failures" : fail_runs,
                    "Errors" : elog,
		    "Timestamp" : ts	
                    }
        self.log.append(log_entry)
        print log_entry
        with open("/var/www/wikidatabot/reports.txt","a") as logfile:
            logfile.write(str(log_entry)+'\n')

    
    def run(self,Entrezlist=None):
        '''launch the bot
        Arguments:
        Entrezlist : dict containing a list of entrez ids. The bot will run only these entrez gene ids 
        '''
        run=0
	success_runs=0
	fail_runs=0
	elog=[]
        if not Entrezlist:
            source = Wikititle.getResult()
        else:
            tuple_list=[]
            for eid in Entrezlist:
                tuple1=()
                title=Wikititle.getTitle(entrez=eid)
                tuple1=(eid,str(title))
                tuple_list.append(tuple1)
            source = tuple_list
        for entrez,title in source:
	    run+=1	
            if run<360:
		continue
	    if run>400:	
		break
	
            try: 
		uni_title=title
           	if not isinstance(title,unicode):
		    uni_title=unicode(title,'utf-8')
		    
            #title = HumanProtein.fieldsdict['Name']
                Wikidata_ID = self.genewikidata.get_identifier(uni_title)
            #print Wikidata_ID
                if Wikidata_ID:
                    Item = self.genewikidata.get_item(Wikidata_ID)
		#ipdb.set_trace()
	        else:
                    #create item and add link it to wikipedia article
                    Wikidata_ID=wikidata.create_Item(title)
                    wikidata.addSiteLinks(Wikidata_ID, title)
               
	        HumanGene,HumanProtein,MouseGene,MouseProtein = mygeneinfo.Parse(str(entrez),uni_title)
                #ipdb.set_trace() 
         
                self.run_HumanProtein(HumanProtein,Wikidata_ID)
         
                self.run_HumanGene(HumanGene)
            
		if MouseProtein:
	                self.run_MouseProtein(MouseProtein)
        	if MouseGene:
        	        self.run_MouseGene(MouseGene)
               
		success_runs+=1 
            except Exception as err:
		fail_runs+=1
		elog.append(err)
		#ipdb.set_trace()
                if isinstance(err,wikidata.WikidataSearchError):
                    err_msg = 'Cause:{e}'.format(e=err)
                    self.logger(1,'invalid',msg=err_msg)
                    #sys.exit(0)
                print err
                message = 'Failure. Error:{e} '.format(e=err)
                self.logger(1, Item.getID(), msg=message)
                
                continue
        
        self.report(int(run)-1,success_runs,fail_runs,elog)  
            
            

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= '''Handling Gene wikidata items''')
    
    parser.add_argument('--only', action='store', dest='update',help='A file with contents like "only = [<list of entrez ids>]"')
    
    args = parser.parse_args()
    
    _only = []
    
    if args.update:
        with open(args.update) as infile:
            exec(infile)
            try:
                _only = only
            except NameError:
                sys.stderr.write('Specified update-only file has invalid format\n')
    BOT = bot(genewikidata.GeneWikidata())
    BOT.run(Entrezlist = _only)
    
