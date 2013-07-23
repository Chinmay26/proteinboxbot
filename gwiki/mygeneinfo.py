
 
import json,urllib2,re,urllib
try:
    import settings
except ImportError as e:
    print "Configure settings appropriately"
    raise e
    
from WItem import *
import rcsb
BASE_URL =  settings.mygene_base
META_URL = settings.mygene_meta
UNIP_URL = settings.uniprot_url

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
    
    
#Construct for human gene 
def parse_HumanGene_json(gene_json):
#edit: Refseq is a multivalue field
    HGItem = HumanGene()
    root = gene_json
    
    HGItem.setField("species", "Q5")
    HGItem.setField("subclass of","Q7187")
    name = get(root, 'name')
    if re.match(r'\w', name):
        name = name[0].capitalize()+name[1:]
    HGItem.setField("Name", name)
    entrez = get(root, 'entrezgene')
    HGItem.setField("Entrez Gene ID", entrez)
    HGItem.setField("Homologene ID", get(get(root, 'homologene'), 'id'))
    HGItem.setField("gene symbol", get(root, 'symbol'))
    HGItem.setField("Ensembl ID", get(get(root, 'ensembl'), 'gene'))
    HGItem.setField("GenLoc_chr", get(get(root, 'genomic_pos'), 'chr'))
    HGItem.setField("GenLoc_start", get(get(root, 'genomic_pos'), 'start'))
    HGItem.setField("GenLoc_end", get(get(root, 'genomic_pos'), 'end'))
    HGItem.setField("RefSeq",get(get(root, 'refseq'), 'rna'))
    HGItem.setField("AltSymbols", get(root, 'alias'))
    HGItem.setField("RNA ID",get(get(root, 'accession'), 'rna'))
    
    return HGItem

def _queryUniprot(entrez):
    return uniprotAccForEntrezId(entrez)

def parse_go_category(entry):

    # single term:
    if 'term' in entry:
        return {entry['id']:entry['term']}
    # multiple terms
    else:
        terms = []
        results = []
        for x in entry:
            if x['term'] not in terms:
                results.append( {x['id']:x['term']} )
            terms.append(x['term'])
        return results

def uniprotAccForEntrezId(entrez):
    '''Returns either one reviewed uniprot id or None.'''
    url = 'http://www.uniprot.org/mapping/'
    params = {
        'from':'P_ENTREZGENEID',
        'to':'ACC',
        'format':'list',
        'reviewed':'',
        'query':entrez
    }

    data = urllib.urlencode(params)
    response = urllib2.urlopen(urllib2.Request(url, data))
    accns = response.read().split('\n')
    for acc in accns:
        if isReviewed(acc): return acc
    return None

def isReviewed(uniprot):
    url = 'http://www.uniprot.org/uniprot/?query=reviewed:yes+AND+accession:{}&format=list'.format(uniprot)
    return bool(urllib.urlopen(url).read().strip('\n'))

def findReviewedUniprotEntry(entries, entrez):
    """Attempts to return the first reviewed entry in a given dict of dbname:id
    pairs for a gene's UniProt entries.
    If a reviewed entry is not found, it attempts to query Uniprot directly for one.
    If this still is unsuccessful, it returns one from TrEMBL at random.

    Arguments:
    - `entries`: a dict of entries, e.g {'Swiss-Prot':'12345', 'TrEMBL':'67890'}
    """
    if not isinstance(entries, dict) and not entrez:
        return u''
    elif entrez:
        return _queryUniprot(entrez)

    if 'Swiss-Prot' in entries:
        entry = entries['Swiss-Prot']
    else:
        entry = entries['TrEMBL']

    if isinstance(entry, list):
        for acc in entry: 
            if isReviewed(acc): return acc
        # if no reviewed entries, check Uniprot directly
        canonical = _queryUniprot(entrez)
        if canonical: return canonical
        else: return entry[0] 
    else: 
        canonical = _queryUniprot(entrez)
        if canonical: return canonical
        else: return entry
    
def findReviewedUniprotEntry2(entries, entrez):
    """Attempts to return the first reviewed entry in a given dict of dbname:id
    pairs for a gene's UniProt entries.
    If a reviewed entry is not found, it attempts to query Uniprot directly for one.
    If this still is unsuccessful, it returns one from TrEMBL at random.

    Arguments:
    - `entries`: a dict of entries, e.g {'Swiss-Prot':'12345', 'TrEMBL':'67890'}
    """
    if not isinstance(entries, dict) and not entrez:
        return u''
    elif entrez:
        return uniprotAccForEntrezId(entrez)

    def isreviewed(uniprot_id):
        try:
            uniprot = urllib.urlopen(UNIP_URL+uniprot_id+".txt")
        except IOError:
            print ("Could not connect to UniProt- check network?")
        text = uniprot.read()
        return ('Reviewed;' in text and not 'Unreviewed;' in text)

    def queryUniprot(entrez):
        return uniprotAccForEntrezId(entrez)

    if 'Swiss-Prot' in entries:
        entry = entries['Swiss-Prot']
    else:
        entry = entries['TrEMBL']

    if isinstance(entry, list):
        for acc in entry:
            if isreviewed(acc): return acc
        # if no reviewed entries, check Uniprot directly
        canonical = queryUniprot(entrez)
        if canonical: return canonical
        else: return entry[0]
    else:
        canonical = queryUniprot(entrez)
        if canonical: return canonical
        else: return entry

def parse_HumanGene(entrez):
    gene_json = getJson( BASE_URL + entrez )
    return parse_HumanGene_json(gene_json)

def parse_HumanProtein_json(gene_json):
    root = gene_json
    HPItem = HumanProtein()
    
    #species wikidata item human=Q5 , protein=Q8054
    HPItem.setField("Name", get(root,'name'))
    HPItem.setField("description", "Human Protein")
    HPItem.setField("species", "Q5")
    HPItem.setField("subclass of","Q8054")
    name = get(root, 'name')
    HPItem.setField("Name", name)
    
    entrez = get(root, 'entrezgene')
    uniprot = findReviewedUniprotEntry(get(root, 'uniprot'), entrez)
    HPItem.setField("Uniprot ID", uniprot)
    
    HPItem.setField("EC number", get(root, 'ec'))
    
    #GO TERMS
    
    if get(root, 'go'):
        HPItem.setField("cell component", parse_go_category(get(root['go'], 'CC')))
        HPItem.setField("molecular function", parse_go_category(get(root['go'], 'MF')))
        HPItem.setField("biological process", parse_go_category(get(root['go'], 'BP')))
    
    #PDB  - CHECK what if Human proteins donot have pdb Id?
    pdbs = rcsb.pdbs_for_uniprot(uniprot)
    if not pdbs:
        pdbs = get(root, 'pdb')
    #checmical_structure
    
        
        
    HPItem.setField("PDB", pdbs)
    
    return HPItem
   
    
    
    
def parse_HumanProtein(entrez):
    gene_json = getJson( BASE_URL + entrez )
    return parse_HumanProtein_json(gene_json)
    
    
    
    
  
if __name__ == '__main__':
   parse_HumanProtein('5649')

 
  