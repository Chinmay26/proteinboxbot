from gwiki import wikidata,Wikititle
import pywikibot

def query():
    '''
    Get Wikidata item ID's for gene wikidata items. Retreive the set of entrez id's from genewikiplus. 
    Query wikidata for these entrez id's. Parse the items to get human/mouse gene/protein ID's
    '''
    mysite = pywikibot.Site('wikidata','wikidata')
    repo = mysite.data_repository()
    
    source=Wikititle.getResult()
    encodes = 'P688'
    encoded_by = 'P702'
    ortholog = 'P684'
    EntrezID = 'P351'
    counter = 1
    f = open("/home/ubuntu/IdList","a")
    
    for entrez,title in source:
        ID_dict=[]
        HPID=None
        HGID=None
        MGID=None
        MPID=None 

        key = "entrez:" + str(entrez)
        search_res = wikidata.search_Item(key)
        if search_res:
            # get the human gene wikidata item
            HGID = wikidata.search_claim(search_res, EntrezID, str(entrez))
        if HGID:
   
            HGItem = pywikibot.ItemPage(repo,HGID)
            Item_dict = HGItem.get()
            if encodes in Item_dict['claims']:
                HP = Item_dict['claims'][encodes][0].getTarget()
                HPID = HP.getID()

            if ortholog in Item_dict['claims']:
                MG = Item_dict['claims'][ortholog][0].getTarget()
                MGID = MG.getID()
                MGItem = pywikibot.ItemPage(repo,MGID)
                dicts = MGItem.get().get('claims')
                if encodes in dicts:
                    MP = dicts[encodes][0].getTarget()
                    MPID = MP.getID()
            
            ID_dict.append(entrez)    
            ID_dict.append(HPID)
            ID_dict.append(HGID)
            ID_dict.append(MPID)
            ID_dict.append(MGID)
            
            f.write(str(counter)+'\t')
            for id in ID_dict:
                f.write(str(id) + '\t\t')
            f.write('\n')

            
        counter = counter + 1
        if counter > 1000:
            break
            
            
    f.close()    
            
            
if __name__=='__main__':
    query()
