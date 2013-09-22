#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from gwiki import wikidata,settings
requires_network=pytest.mark.require_network
import pywikibot
site = pywikibot.Site('wikidata','wikidata')
repo = site.data_repository()



class TestWikidataFunctions:
    '''
    Check querying of wikidata
    '''
    
    @requires_network
    def test_WikidataSuccessSearchItem(self):
        '''
        Search for Reelin Gene item with label=Reln(Q414043) having claim entrez id(p351) = 5649 
        Search for Reelin Protein item with label=reelin(Q13569356) having claim uniprot id(p352) = P78509
        '''

        result=wikidata.search_Item(title='entrez:5649')
        assert wikidata.search_claim(Items=result, property='P351', value='5649') == 'Q414043'
        
        result=wikidata.search_Item(title='uniprot:p78509')
        assert wikidata.search_claim(Items=result, property='P352', value='P78509') == 'Q13569356'
        
    @requires_network
    def test_WikidataFailSearchItem(self):
        '''
        Search for Reelin Gene item with key=entrez:5649(label is Reln -- Q414043) having claim entrez id(p351) = 1050  (correct value = 5649) 
        Search for Reelin Protein item with label=reelin(Q13569356) having claim uniprot id(p352) = P987 (correct value = P78509 )
        '''
        result=wikidata.search_Item(title='entrez:5649')
        assert wikidata.search_claim(Items=result, property='p351', value='1050') == []
        
        result=wikidata.search_Item(title='uniprot:p78509')
        assert wikidata.search_claim(Items=result, property='p352', value='P987') == []
        
    @requires_network    
    def test_Constructfrom_WikidataItem_Success(self):
        '''
        Check whether the wikidata oject claims are being parsed correctly 
        Construct object from Reelin Human Gene item - Q414043
        Construct object from Reelin Human Protein item - Q13569356
        Construct object from Reelin Mouse Protein item - Q14331165
        Construct object from Reelin Mouse Gene item - Q14331135
        '''
        from gwiki import WItem
        item=pywikibot.ItemPage(repo,'Q414043')
        HGene=wikidata.construct_from_item(Item=item, Entity=WItem.HumanGene())
        assert HGene.fieldsdict['HGNC ID'] == '9957'
        assert HGene.fieldsdict['Homologene ID'] == '3699'
        assert HGene.fieldsdict['OMIM ID'] == '600514'
        assert HGene.fieldsdict['encodes'] == 'Q13569356'
        assert HGene.fieldsdict['Entrez Gene ID'] == '5649'
        
        item=pywikibot.ItemPage(repo,'Q13569356')
        HProtein=wikidata.construct_from_item(Item=item, Entity=WItem.HumanProtein())
        assert HProtein.fieldsdict['Uniprot ID'] == 'P78509'
        assert HProtein.fieldsdict['found in taxon'] == 'Q5'
        assert HProtein.fieldsdict['encoded by'] == 'Q414043'
        
        item=pywikibot.ItemPage(repo,'Q14331165')
        MProtein=wikidata.construct_from_item(Item=item, Entity=WItem.MouseProtein())
        assert MProtein.fieldsdict['Uniprot ID'] == 'Q60841'
        assert MProtein.fieldsdict['found in taxon'] == 'Q83310'
        assert MProtein.fieldsdict['encoded by'] == 'Q14331135'
        
        item=pywikibot.ItemPage(repo,'Q14331135')
        MGene=wikidata.construct_from_item(Item=item, Entity=WItem.MouseGene())
        assert MGene.fieldsdict['Entrez Gene ID'] == '19699'
        assert MGene.fieldsdict['found in taxon'] == 'Q83310'
        assert MGene.fieldsdict['encodes'] == 'Q14331165'
        
        
    @requires_network    
    def test_Constructfrom_WikidataItem_Fail(self):
        '''
         Check failure to parse wikidata items
        '''
        from gwiki import WItem
        item=pywikibot.ItemPage(repo,'Q414043')#human gene reelin item
        HGene=wikidata.construct_from_item(Item=item, Entity=WItem.HumanProtein()) #human protein object
        with pytest.raises(KeyError):
            HGene.fieldsdict['Entrez Gene ID']
    
    
        
    def test_addSingleClaim(self):
        '''
        Check adding claims + sources to wikidata sandbox item = Q4115189
        claim property id='p351' value=5649
        First login to wikidata,add claim,check claim added or not
        '''
        import pywikibot
        from pywikibot.data import api
        assert len(settings.wikidata_user)!=0
        assert len(settings.wikidata_password)!=0
        base_site=pywikibot.Site(code=settings.Code_site, fam=settings.Code_site,user=settings.wikidata_user)
        Wrepo=base_site.data_repository()
        assert api.LoginManager(site=base_site,user=settings.wikidata_user,password=settings.wikidata_password).login() == True
        

        item = pywikibot.ItemPage(Wrepo,'Q4115189')
        item.get()
        claim = pywikibot.Claim(Wrepo,'P351')
        claim.setTarget('5649')
   
        sourceItem = pywikibot.ItemPage(Wrepo,'Q1345229')
        source = pywikibot.Claim(Wrepo,unicode('P143'))#imported from
        source.setTarget(sourceItem)
        assert api.LoginManager(site=base_site,user=settings.wikidata_user,password=settings.wikidata_password).login() == True
        item.addClaim(claim, bot=True)
        claim.addSource(source)
#check claim has been added or not       
        item=pywikibot.ItemPage(Wrepo,'Q4115189')
        claims=item.get().get('claims')
        total = len(claims['P351'])
        
        assert claims['P351'][int(total)-1].getTarget() == '5649'   