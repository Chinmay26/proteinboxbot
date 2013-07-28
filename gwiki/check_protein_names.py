'''
Created on Jul 26, 2013

@author: chinmay
'''
import pywikibot
import mygeneinfo
import genewikidata
gw = genewikidata.GeneWikidata()

def setnames():
    source = gw.title_and_entrez()
    for title,entrez in source:
        #print title,entrez
        Wikidata_ID = gw.get_identifier(title)
        #print Wikidata_ID
        
        if Wikidata_ID:
            Item = gw.get_item(Wikidata_ID)
            #get the HGNC name
            gene_json = mygeneinfo.getJson( mygeneinfo.BASE_URL + entrez )
            
            title = mygeneinfo.get(gene_json, 'name')
            print title
            labels = {"en" : title}
            
            Item.editLabels(labels)
            
if __name__ == '__main__':
    setnames()
            
            