#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gwiki import mygeneinfo
import pytest
requires_network = pytest.mark.requires_network

class TestMyGeneInfoParser:
    '''Tests for parsing valid/invalid JSON returned by mygene.info. Also, ensure correct Human/Mouse Protein/Gene objects constructed 
       by parsing JSON and qurying wikidata'''

    @requires_network
    def test_getJson(self):
        '''Checks that we can retrieve and parse a JSON document successfully.
        Also does a sanity check on mygene.info's available fields.
        '''

        metadata =  mygeneinfo.getJson("http://mygene.info/v2/metadata")
        assert 'entrezgene' in metadata['available_fields']
        assert 'uniprot' in metadata['available_fields']
        
    @requires_network   
    def test_parse_fail(self):
        '''
        Check parse with wrong wikipedia page label.
        First argument: entrez ID
        Second argument : wikipedia page label
        The correct wikipedia page label is "Reelin"    
        '''
        with pytest.raises(TypeError):
            mygeneinfo.Parse('5649','RELN')
    
    @requires_network
    def test_parse_Human_Gene(self):
        '''
        Checks parsing of Reelin Human Gene
        entrez gene =5649
        Check whether Reelin Human protein wikidata  item(Q13569356) and Mouse Gene wikidata item (Q14331135) is setup correctly 
        '''
        geneJson = mygeneinfo.getJson("http://mygene.info/v2/gene/5649")
        homologJson = mygeneinfo.getJson("http://mygene.info/v2/gene/19699")
        HumanGene = mygeneinfo.parse_HumanGene_json(geneJson,homologJson)
        
        assert HumanGene.fieldsdict['gene symbol'] == "RELN"
        assert HumanGene.fieldsdict['ortholog'] == "Q14331135"
        assert HumanGene.fieldsdict['encodes'] == "Q13569356"
        assert HumanGene.fieldsdict['Entrez Gene ID'] == "5649"
        
    @requires_network
    def test_parse_No_Homolog(self):
        '''
        Cholesterylester transfer protein(Entrez Gene ID-1071) has no mouse homolog. Check if such cases are handled 
        '''
        HG,HP,MG,MP=mygeneinfo.Parse('1071','Cholesterylester transfer protein')
        assert MG== None
        assert MP== None
        assert HG.fieldsdict['ortholog']== ''
        
    
    @requires_network
    def test_search_by_alias(self):
        '''
        Check whether items are retreived correctly or not
        '''
        assert mygeneinfo.searchAlias('entrez:5649','P351','5649') == 'Q414043'
        assert mygeneinfo.searchAlias('go:0046872','P686','0046872') == 'Q13667380'
    
    @requires_network
    def test_find_uniprot_basic(self):
        '''Make sure we find the reviewed entry of the group.'''
        entries = {'Swiss-Prot':'P24941', 'TrEMBL':'E7ESI2'}
        selected = mygeneinfo.findReviewedUniprotEntry(entries, None)
        assert selected == 'P24941'

    @requires_network
    def test_find_uniprot_reviewed(self):
        '''Checks that we're actually finding the reviewed entry (Swiss-Prot)
        and not just returning one at random.'''
        entriesMixed = {'TrEMBL':['fake-acc1', 'fake-acc2', 'fake-acc3'],
                        'Swiss-Prot':'P24941'}
        selected2 = mygeneinfo.findReviewedUniprotEntry(entriesMixed, None)
        assert selected2 == 'P24941'

    @requires_network
    def test_find_uniprot_noreviewed(self):
        '''Check that we can return something even if nothing is reviewed'''
        entriesUnreviewed = {'TrEMBL':'E7ESI2'}
        selected3 = mygeneinfo.findReviewedUniprotEntry(entriesUnreviewed, None)
        assert selected3 == 'E7ESI2'

    def test_find_uniprot_missing(self):
        '''Check that we return an empty unicode string if we are passed 
        an empty string'''
        entries = ''
        assert u'' == mygeneinfo.findReviewedUniprotEntry(entries, None)
    
    def test_find_uniprot_unexpected(self):
        '''Check that we return an empty unicode string if we're passed 
        an unexpected input'''
        entries = ['foo','bar']
        assert u'' == mygeneinfo.findReviewedUniprotEntry(entries, None)

    def test_find_uniprot_without_mygeneinfo(self):
        '''Check that we can pull a reviewed uniprot entry from uniprot
        even if mygene.info doesn't record any. (Note: this test may fail 
        if entrez id 28 returns a different uniprot acc in the future.)'''
        assert u'P16442' == mygeneinfo.findReviewedUniprotEntry('', '28')

    
        
        
        

                             
        
        