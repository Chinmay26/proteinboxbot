'''
Created on Jun 21, 2013

@author: chinmay
'''
import pywikibot
import re
from pywikibot.data import api

#repo = pywikibot.Site('wikidata' , 'wikidata').data_repository()


try:
    import settings
except ImportError as e:
    print("Could not import settings")
    raise e
    

#Q4115189 - sandbox
#Obtain the gene article from wikipedia
class GeneWikidata(object):
    code_site = settings.Code_site
    family = settings.Code_site
    base_site = None
    data_repo = None
    category = None
    def __init__(self):
        self.base_site = pywikibot.Site(code = self.code_site, fam = self.family, user = None, sysop = None, interface =None)
        #fam = family
        #sysop = system operator 
        #TO-DO  After getting bot flag, update login here by using sysop
        api.LoginManager(site = self.base_site , user = settings.wikidata_user , password = settings.wikidata_password ).login()
        #self.base_site.login()
        self.data_repo = self.base_site.data_repository()
        
    def get_item(self,Wikidata_ID):
        item = pywikibot.ItemPage(self.data_repo , Wikidata_ID)
        item.get()
        return item
    
    def articles(self):
        self.category = pywikibot.Category(pywikibot.Link(settings.CATEGORY_NAME,defaultNamespace=14)) 
        #NOTICE  total = None  when running for the entire set of PBB templates
        articles = self.category.articles(recurse = False, step = None, total = 1, content = True, namespaces = None)
        #content = True retreive the contents of gene wikiarticles
        #recurse = False Dont go into subcategories
        #total  retreive the many number of pages 
        for article in articles:
            yield article
            
    def title_and_entrez(self):
        for article in self.articles():
            match = re.search(r'\{\{\s?PBB\s?\|\s?geneid=\s?([\d]*)\s?\}\}', article.text)
            if match :
                yield (article.title(),match.group(1)) 
                
    #def infoboxes(self):
        
     #   self.category = pywikibot.Category(pywikibot.Link("Template:GNF_Protein_box",defaultNamespace=14))
        
    def get_identifier(self,title):
        #create temporary wikipedia site object to get WIKIDATA ITEM identifier from linked wikipedia page
        site = pywikibot.Site('en', 'wikipedia')
        page = pywikibot.Page(site,title)
        item = pywikibot.ItemPage.fromPage(page)
        if item.exists():
            return item.getID()
        
                
    #TO-DO Create a wikidata item
            
    
    
        
   # def write(self,name,symbol):
    #    page = pywikibot.Page(site,'name')
     #   if not page.exists():
      #      page = pywikibot.Page(site,'symbol')
       #     wikipedia_item = pywikibot.ItemPage.fromPage(page)
#Obtain the item from wikidata
        #    item = pywikibot.ItemPage(repo,wikipedia_item.getID())#currently can access wikidata items through ID's only
         #   item.get()

#print item.claims
#claim = pywikibot.Claim(repo,'p352')
#claim.setTarget("5649")    
#item.addClaim(claim,bot=True)

#checks whether the item has claims
#for key in properties:
 #   property_id = properties[key]
  #  if item.claims.has_key(property_id):
   #     print property_id
#item.claims.has_key(k)
#dicts = item.claims.viewkeys() #gives property id's present in the item
#print type(dicts)

