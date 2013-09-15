'''
Created on Jul 3, 2013

@author: chinmay
'''
import WItem,ipdb
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
    '''Construct WItem(HumanProtein , HumanGene ,MouseProtein , MouseGene) by reading and parsing the wikidata item
    Arguments:
    -Item : wikidata ID
    -Entity : Type of Entity(can be one of HumanProtein , HumanGene ,MouseProtein , MouseGene) 
    '''
    Item_dict=Item.get()
    
    #labels definitely exist
    try :
        label = Item_dict['labels']['en']
        Entity.setField('Name',label)
    #descriptions may not exist
        if 'descriptions' in Item_dict:
            if 'en' in Item.descriptions:
                des = Item.descriptions['en']
                Entity.setField('description',des)

        if 'aliases' in Item_dict:
	    if 'en' in Item_dict['aliases']:
		alias=Item_dict['aliases']['en']       
		Entity.setField('aliases',alias)
 
        for claim in Item_dict['claims']:
            if claim in Entity.properties:
                if len(Item_dict['claims'][claim]) > 1 :
                #TO-DO  work on  qualifiers
                    multival = []
                    total = len(Item_dict['claims'][claim])
                    for k in range(0,total):
                        existing_val = Item_dict['claims'][claim][k].getTarget()
                        if isinstance(existing_val,pywikibot.page.ItemPage):
                            match = re.search(r'\[\[wikidata\:([\w]*)\]\]',str(existing_val))
                            if match:
                        #print match.group(1)
                                existing_val = str(match.group(1))
                    
                        multival.append(existing_val)
                
                    pval = multival
            
                else:
                    pval = Item_dict['claims'][claim][0].getTarget()
                #print pval , claim , type(pval)
                    if isinstance(pval,pywikibot.page.ItemPage):
                        match = re.search(r'\[\[wikidata\:([\w]*)\]\]',str(pval))
                        if match:
                        #print match.group(1)
                            pval = str(match.group(1))
                    
                field_name = Entity.properties[claim]
                Entity.setField(field_name,pval)
                
        return Entity
    
    except:
        emsg='Failed to construct Entity:{ET} from wikidata item:{ITEM}'.format(ET=Entity,ITEM=Item)
        raise WikidataConstructItem(emsg)


def search_Item(title):
    '''
    Search for wikidata item with key = wikidata item label
    Directly calls the mediawiki API
    Arguments:
    -title : Wikidata item label
    '''
    
    
    mysite = pywikibot.Site("wikidata","wikidata")
    
    params = { 'action' :'wbsearchentities' ,
                'format' : 'json' ,              
              'language' : 'en',
               'limit' : '5',      #retreive five items
                'type' : 'item',
                'search': '',
              }
    #for reelin we have four additional wikidata items for testing purposes

         
    params['search']= title
    request = api.Request(site=mysite,**params)
    data = request.submit()
    if data['success']:
        return data['search'] 


def create_Item(title):
    '''
    Create a wikidata item
    Arguments:
    -title : wikidata item label. The newly created item is initialised with this title
    '''
    #ipdb.set_trace()
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
    '''
    Search whether the item contains the claim with key=value
    Arguments:
    Items : set of items to search for
    property : property id
    value : key property value to be matched against
    '''
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
    
    
def addClaim(ID,property,value,pfield):
    ''' Add claim to the wikidata item and a label to created item
    Arguments:
    -ID : wikidata ID
    -Property : Property ID
    -value    : Property value
    -pfield   : property name
    '''
    mysite = pywikibot.Site("wikidata","wikidata")
    repo = mysite.data_repository()
    item = pywikibot.ItemPage(repo,ID)
    item.get()
    claim = pywikibot.Claim(repo,property)
    claim.setTarget(value)
    
    
    sourceField = WItem.Item.property_list_sources[pfield]
    sourceItem = pywikibot.ItemPage(repo,sourceField)
    source = pywikibot.Claim(repo,unicode('P143'))#imported from
    source.setTarget(sourceItem)
    
    item.addClaim(claim, bot = True)
    claim.addSource(source)
    
def search_HumanProtein(title):
    '''Search for Human Protein by obtaining the default linked wikidata item from wikipedia article
    
    Arguments:
    -title : Wikidata label
     '''
    
    site = pywikibot.getSite('en')
    page = pywikibot.Page(site,title)
    item = pywikibot.ItemPage.fromPage(page)
    if item.exists():
        return item.getID()
    else:
        return None
    

    
def setSource(property,pfield,pvalue):
    '''ADD source to wikidata claim
    
     Arguments:
     -Property : property id 
     -pfield   : property name
     -pvalue   : property value
    
    '''
    
    mysite = pywikibot.Site("wikidata","wikidata")
    repo = mysite.data_repository()
    
    sourceField = WItem.Item.property_list_sources[pfield]
    sourceItem = pywikibot.ItemPage(repo,sourceField)
    source = pywikibot.Claim(repo,unicode('P143'))#imported from
    source.setTarget(sourceItem)
    
    claim1 = pywikibot.Claim(repo,unicode(property))
    claim1.setTarget(pvalue)
    claim1.addSource(source)
    
    
def setHumanProtein(Name,label,uniprot):
    '''Properly setup the HumanProtein Item with appropriate label and uniprot claim
    
      Arguments:
      -Name    : HGNC Name
      -label   : Search for HP item with this existing label
      -uniprot : Add Claim==uniprotID for the item
      
      ''' 
        
    res1 = search_HumanProtein(label)
    mysite = pywikibot.Site("wikidata","wikidata")
    repo = mysite.data_repository()
    item = pywikibot.ItemPage(repo,res1)
    Item_dict = item.get()
    labels = {"en":unicode(Name)
              }
    if Item_dict['labels']['en'] != Name:
        item.editLabels(labels)

    up="uniprot:"+str(uniprot)
    setLabel(item.getID(),up)
    
    if 'P352' in item.claims:
        return
    else:
        UPclaim = pywikibot.Claim(repo,unicode('P352'))
        UPclaim.setTarget(uniprot)
        
        source = pywikibot.Claim(repo,unicode('P143'))
        sourceItem = pywikibot.ItemPage(repo,'Q905695')
        source.setTarget(sourceItem)
        
        item.addClaim(UPclaim, bot = True)
        UPclaim.addSource(source)
        
def setLabel(ItemID,value):
    mysite = pywikibot.Site("wikidata","wikidata")
    repo = mysite.data_repository()
    item = pywikibot.ItemPage(repo,ItemID)
    Item_dict = item.get()

    alias_dict=[]
    if 'aliases' in Item_dict:
        if 'en' in Item_dict['aliases']:
            alias_dict=Item_dict['aliases']['en']

    if unicode(value) not in alias_dict:
        alias_dict.append(unicode(value))
        al={"en":alias_dict}
        item.editAliases(al)

def set_GO_Terms(ItemID,GO_value):
    '''
    check if already created GO terms have GO ID claims or not. If not add GO claim
    '''
    mysite = pywikibot.Site("wikidata","wikidata")
    repo = mysite.data_repository()
    item = pywikibot.ItemPage(repo,ItemID)
    Item_dict = item.get()
    
    GO_ID='P686'
    if GO_ID not in Item_dict['claims']:
        addClaim(ItemID, GO_ID, GO_value, 'Gene Ontology ID')
    else:
        #verify the go id
        claim=Item_dict['claims'][GO_ID][0]
        if claim.getTarget() != GO_value:
            claims=[claim]
            item.removeClaims(claims)
            addClaim(ItemID, GO_ID, GO_value, 'Gene Ontology ID')
        
def addSiteLinks(ItemID,title):
    mysite = pywikibot.Site("wikidata","wikidata")
    repo = mysite.data_repository()
    item = pywikibot.ItemPage(repo,ItemID)
    Item_dict = item.get()    
    SL={"site" : "enwiki",
    "title" : title
    }
    item.setSitelink(SL) 
        
class WikidataConstructItem(Exception):
    '''Thrown when we cannot construct Proteinboxbot by reading values from wikidata item'''
        
    
class WikidataSearchError(Exception):
    '''Thrown when we cannot find the wikidata item''' 
    
    
