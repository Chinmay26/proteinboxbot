#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
#from gwiki import bot
from gwiki import settings
requires_network=pytest.mark.require_network

class TestBotSetup:
    '''
        Check pywikipedia framework setup
        Check login onto wikidata, wikipedia
        Requires valid net connection
    '''
    def test_FrameworkSetup(self):
        ''' 
        throws import error if pywikipedia framework not setup
        '''
        import pywikibot
       
    @requires_network
    def test_Login(self):
        '''
        Check login to wikidata
        '''
        import pywikibot
        from pywikibot.data import api
        assert len(settings.wikidata_user)!=0
        assert len(settings.wikidata_password)!=0
        base_site=pywikibot.Site(code=settings.Code_site, fam=settings.Code_site)
        assert api.LoginManager(site=base_site,user=settings.wikidata_user,password=settings.wikidata_password).login() == True
        
