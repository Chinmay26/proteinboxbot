'''
Created on Jun 20, 2013

@author: chinmay
'''
import json,urllib2

BASE_URL =  "http://mygene.info/gene/"
#TO-DO Currently we obtain only first JSON document-basic gene info. Extend to include homologs, meta-json etc
def getJson(url):
    ufile = None
    try:
        ufile = urllib2.urlopen(url)
        contents = ufile.read()          
        if not isinstance(contents, unicode):
            contents = contents.decode('utf-8')
            return json.loads(contents)
    except urllib2.HTTPError as e:
        if e.code == 404:  
            raise e     
    except IOError as e:
        print("Network error: are you connected to the internet?")
        raise e
    
def getinfo(entrez):
    gene_json = getJson(BASE_URL + entrez) 
    #print gene_json
    if gene_json is None:
        return
    HGNC = ''
    OMIM =''
    name =''
    if "HGNC" in gene_json:
        HGNC = gene_json["HGNC"]
    if "MIM" in gene_json:
        OMIM = gene_json["MIM"]
    if "name" in gene_json:
        Gene_name = gene_json["name"]
    if "symbol" in gene_json:
        Symbol = gene_json["symbol"]
    #print entrez,HGNC , OMIM , Gene_name,Symbol
    
    
    
  
if __name__ == '__main__':
   getinfo(str(10008))
 #   for i in range(1,50):
  #      getinfo(str(i))  
  