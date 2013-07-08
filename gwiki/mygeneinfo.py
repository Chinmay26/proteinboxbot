
#MODIFIED mygeneinfo of previous bot. Retained most part of previous mygeneinfo 
import json,urllib2,re
try:
    import settings
except ImportError as e:
    print "Configure settings appropriately"
    raise e
    
from HumanGene import *
BASE_URL =  settings.mygene_base

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
    
def get(json,key):
    result = u''
    if isinstance(json, dict):
        result = json[key] if key in json else u''
    elif isinstance(json, list):
        result = get(json[0], key) if (len(json)>0) else u''
    elif isinstance(json, unicode):
        result = json
    elif isinstance(json, str):
        result = json.decode('utf8')
    return result
    
    
def parse_json(gene_json):
#edit: Refseq is a multivalue field
    box = HumanGene()
    root = gene_json
    
    box.setField("species", "Q5")
    box.setField("subclass of","Q7187")
    name = get(root, 'name')
    if re.match(r'\w', name):
        name = name[0].capitalize()+name[1:]
    box.setField("Name", name)
    entrez = get(root, 'entrezgene')
    box.setField("Entrez Gene ID", entrez)
    box.setField("Homologene ID", get(get(root, 'homologene'), 'id'))
    box.setField("gene symbol", get(root, 'symbol'))
    box.setField("Ensembl ID", get(get(root, 'ensembl'), 'gene'))
    box.setField("GenLoc_chr", get(get(root, 'genomic_pos'), 'chr'))
    box.setField("GenLoc_start", get(get(root, 'genomic_pos'), 'start'))
    box.setField("GenLoc_end", get(get(root, 'genomic_pos'), 'end'))
    box.setField("RefSeq",get(get(root, 'refseq'), 'rna'))
    box.setField("AltSymbols", get(root, 'alias'))
    box.setField("RNA ID",get(get(root, 'accession'), 'rna'))
    
    return box
    
    

def parse(entrez):
    gene_json = getJson( BASE_URL + entrez )
    return parse_json(gene_json)
    
    
    
  
#if __name__ == '__main__':
#   parse('5649')

 
  