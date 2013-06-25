'''
Created on Jun 20, 2013

@author: chinmay
'''
import pywikibot

CATEGORY_NAME = u"Human protein templates"
site = pywikibot.Site('en', 'wikipedia')

a = pywikibot.Category(pywikibot.Link(CATEGORY_NAME,defaultNamespace=14))

#DO NOT Query Mygene.info for entrez-ID. Not all genes have PBB templates. Obtain entrez id from wikipedia category "Human protein Templates"
def infoboxes_entrez():
    for page in a.members(recurse = False, namespaces = None, step =None, total=10, content=None):
        # recurse = True gives subcategories also 
        # total gives number of pages to query
        # content = True retreives page content as well
        if "Template:PBB/" in page.name:
            yield page