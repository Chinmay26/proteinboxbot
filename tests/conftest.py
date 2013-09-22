#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest, urllib2


def internet_on():
    try:
        urllib2.urlopen('http://74.125.224.193', timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False
 
    

def pytest_runtest_setup(item):
    if 'requires_network' in item.keywords and not internet_on():
        pytest.skip("\ntest needs active connection to run");
        
        
        