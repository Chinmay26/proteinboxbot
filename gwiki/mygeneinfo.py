
 
import json,urllib2,re,urllib
import wikidata
import time
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

MOUSE_TAXON_ID = 10090

refseq_valid_accession_prefixes = ["NG_", "NT_", "NC_", "AW_", "NW_", "NS_", "NZ_"]

refseq_RNA_ID_valid_accession_prefixes = ["NM_", "NR_", "XM_", "XR_"]

refseq_Protein_ID_valid_accession_prefixes = ["NP_", "AP_", "YP_", "XP_", "ZP_"]



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
    
    

def parse_accession(initial_list, type):
    final_rectified = []
    if type == "RefSeq Protein ID":
        for id in initial_list:
            if unicode(id[0:3]) in refseq_Protein_ID_valid_accession_prefixes:
                final_rectified.append(id)
            
    elif type == "RefSeq":
        for id in initial_list:
            if unicode(id[0:3]) in refseq_valid_accession_prefixes:
                final_rectified.append(id)
                
    elif type == "RefSeq RNA ID":
        for id in initial_list:
            if unicode(id[0:3]) in refseq_RNA_ID_valid_accession_prefixes:
                final_rectified.append(id)
                
    return final_rectified


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

#To-do Gene Atlas image
#Construct for human gene 
def parse_HumanGene_json(gene_json,homolog_json):
#edit: Refseq is a multivalue field
    HGItem = HumanGene()
    root = gene_json
    
    HGItem.setField("found in taxon", "Q5")
    HGItem.setField("description","human Gene")
    HGItem.setField("subclass of","Q7187")

    #for genes label = HGNC symbol
    HGItem.setField("Name", get(root, 'symbol'))
    entrez = get(root, 'entrezgene')
    HGItem.setField("Entrez Gene ID", entrez)
    HGItem.setField("Homologene ID", get(get(root, 'homologene'), 'id'))
    HGItem.setField("gene symbol", get(root, 'symbol'))
    HGItem.setField("Ensembl Gene ID", get(get(root, 'ensembl'), 'gene'))
    
    HGItem.setField("Ensembl Transcript ID", get(get(root, 'ensembl'), 'transcript'))
    HGItem.setField("GenLoc_chr", get(get(root, 'genomic_pos'), 'chr'))
    HGItem.setField("GenLoc_start", get(get(root, 'genomic_pos'), 'start'))
    HGItem.setField("GenLoc_end", get(get(root, 'genomic_pos'), 'end'))
    HGItem.setField("AltSymbols", get(root, 'alias'))
    
    #adding id's based on valid refseq prefixes
    initial = get(get(root, 'refseq'), 'rna')
    HGItem.setField("RefSeq",parse_accession(initial, "RefSeq"))
    initial = get(get(root, 'accession'), 'rna')
    HGItem.setField("RefSeq RNA ID",parse_accession(initial, "RefSeq RNA ID"))
    
    HGItem.setField("HGNC ID", get(root, 'HGNC'))
    HGItem.setField("OMIM ID",get(root,'MIM'))
    
    #encodes  -- search for human protein
    key = get(root,'name') 
    ID = []
    res = wikidata.search_Item(key)
    #search for human protein, property = uniprot ID 
    #most surely human protein is present, but still....
    uniprot = findReviewedUniprotEntry(get(root, 'uniprot'), entrez)
    if res:
        uniprotID = 'p352'
        ID = wikidata.search_claim(res,uniprotID ,uniprot)
    #search result is null or corresponding human protein doesnot exist
    if not ID:
        #create human protein item
        #ID = wikidata.create_Item(key)
        #add uniprot claim to human protein item
        #wikidata.addClaim(ID, 'p352',uniprot)
        #TO-DO
        print "ERROR IN RETREIVING Human protein item"   
    #following convention of having capitalised wikidata identifiers 
    HGItem.setField("encodes", ID.title())
    
    #ortholog
    key = get(homolog_json,'symbol')
    ID = []
    res = wikidata.search_Item(key)
    #search for mouse gene, property = entrez ID 
    if res:
        entrezID = 'p351'
        mouse_entrez = get(homolog_json,'entrezgene')
        ID = wikidata.search_claim(res,entrezID ,mouse_entrez)
    #search result is null or corresponding mouse gene doesnot exist
    if not ID:
        #create mouse gene item
        
        ID = wikidata.create_Item(key)
        #add entrez claim to mouse gene item
        mouse_entrez = get(homolog_json,'entrezgene')
        wikidata.addClaim(ID, 'p351',str(mouse_entrez))
        print "created mouse gene item -- with entrez", mouse_entrez
        #following convention of having capitalised wikidata identifiers    
    HGItem.setField("ortholog", ID.title())
    
    
    
    
    return HGItem



#Construct for mouse gene 
def parse_MouseGene_json(homolog_json,gene_json):
#edit: Refseq is a multivalue field
    MGItem = MouseGene()
    root = homolog_json
    
    MGItem.setField("found in taxon", "Q83310")
    MGItem.setField("subclass of","Q7187")
    MGItem.setField("description","mouse Gene")
    
    #for mouse gene label = MGI symbol
    MGItem.setField("Name",  get(root, 'symbol'))
    entrez = get(root, 'entrezgene')
    MGItem.setField("Entrez Gene ID", entrez)
    MGItem.setField("Homologene ID", get(get(root, 'homologene'), 'id'))
    MGItem.setField("gene symbol", get(root, 'symbol'))
    MGItem.setField("Ensembl Gene ID", get(get(root, 'ensembl'), 'gene'))
    MGItem.setField("Ensembl Transcript ID", get(get(root, 'ensembl'), 'transcript'))
    MGItem.setField("GenLoc_chr", get(get(root, 'genomic_pos'), 'chr'))
    MGItem.setField("GenLoc_start", get(get(root, 'genomic_pos'), 'start'))
    MGItem.setField("GenLoc_end", get(get(root, 'genomic_pos'), 'end'))
    MGItem.setField("AltSymbols", get(root, 'alias'))
   
    
    
    #adding id's based on valid refseq prefixes
    initial = get(get(root, 'refseq'), 'rna')
    MGItem.setField("RefSeq",parse_accession(initial, "RefSeq"))
    initial = get(get(root, 'accession'), 'rna')
    MGItem.setField("RefSeq RNA ID",parse_accession(initial, "RefSeq RNA ID"))
    
    #encodes  -- search for mouse protein
    key = get(root,'name') 
    ID = []
    res = wikidata.search_Item(key)
    #search for mouse protein, property = uniprot ID 
    #most surely mouse protein is present, but still....
    uniprot = findReviewedUniprotEntry(get(root, 'uniprot'), entrez)
    if res:
        uniprotID = 'p352'
        ID = wikidata.search_claim(res,uniprotID ,uniprot)
    #search result is null or corresponding human gene doesnot exist
    if not ID:
        #create mouse protein item
        print "creating mouse protein with uniprot ID",uniprot
        ID = wikidata.create_Item(key)
        #add uniprot claim to mouse protein item
        wikidata.addClaim(ID, 'p352',uniprot)    
    MGItem.setField("encodes", ID.title())
    
    #ortholog
    key = get(gene_json,'symbol')
    ID = []
    res = wikidata.search_Item(key)
    #search for human gene, property = entrez ID 
    if res:
        entrezID = 'p351'
        ID = wikidata.search_claim(res,entrezID ,get(gene_json,'entrezgene'))
    #search result is null or corresponding human gene doesnot exist
    if not ID:
        #create human gene item
        #ID = wikidata.create_Item(key)
        #add entrez claim to human gene item
        #human_entrez = get(gene_json,'entrezgene')
        #wikidata.addClaim(ID, 'p3521',human_entrez)
        #TO-DO
        print "ERROR"    
    MGItem.setField("ortholog", ID.title())
    
    return MGItem

#TO-do ec classification
def parse_MouseProtein_json(Homolog_json):
    root = Homolog_json
    MPItem = MouseProtein()
    
    #found in taxon wikidata item mouse=Q83310 , protein=Q8054
    MPItem.setField("Name", get(root,'name'))
    MPItem.setField("description", "mouse Protein")
    MPItem.setField("found in taxon", "Q83310")
    MPItem.setField("subclass of","Q8054")
    name = get(root, 'name')
    MPItem.setField("Name", name)
    
    entrez = get(root, 'entrezgene')
    uniprot = findReviewedUniprotEntry(get(root, 'uniprot'), entrez)
    MPItem.setField("Uniprot ID", uniprot)
    
    #MPItem.setField("EC number", get(root, 'ec'))
    initial = get(get(root, 'refseq'), 'protein')
    MPItem.setField("RefSeq Protein ID",parse_accession(initial,"RefSeq Protein ID"))
    MPItem.setField("Ensembl Protein ID", get(get(root, 'ensembl'), 'protein'))
    
    #GO TERMS
    #Wikidata items for GO terms
    GO_ID = 'p686'
    if get(root, 'go'):
        GO_DICT = get(root,'go')
        for key in GO_DICT:
            res_list = GO_DICT[key]
            ID = []
            #single term
            if 'term' in res_list:
                title = res_list['term']
                res = wikidata.search_Item(title)
                if res:
                    #fix val['id']='GO:223'  remove the first three elements 
                    GID = wikidata.search_claim(res, GO_ID, res_list['id'][3:])
                    
                #Create GO Item if it does not exist
                if not GID:
                    GID = wikidata.create_Item(title)
                    print "created GO item ",GO_ID,GID
                    #add created id's for the go terms
                    
                    wikidata.addClaim(GID, GO_ID, res_list['id'][3:])
                ID.append(GID.title())
                
            else:
                #mutiple terms in go field              
                for val in res_list:
                #search for the item
                
                    title = val['term']
                # title has multiple words seperated by /   
                # found
                    if title.find('/') != -1:
                        match = re.search(r'([\w ]*)\/.*',title)
                        title = match.group(1)
                    res = wikidata.search_Item(title)
                    GID = []
                #search for the corresponding go term
                    if res:
                    #fix val['id']='GO:223'  remove the first three elements 
                        GID = wikidata.search_claim(res, GO_ID, val['id'][3:])
                    
                #Create GO Item if it does not exist
                    if not GID:
                        GID = wikidata.create_Item(title)
                        print "created GO item ",GO_ID,GID
                    #add created id's for the go terms
                    
                        wikidata.addClaim(GID, GO_ID, val['id'][3:])
                    ID.append(GID.title())
            if key == 'CC':
                MPItem.setField("cell component",ID)
            if key == 'MF':
                MPItem.setField("molecular function",ID)
            if key == 'BP':
                MPItem.setField("biological process",ID)
    
    #if get(root, 'go'):
    #    MPItem.setField("cell component", parse_go_category(get(root['go'], 'CC')))
    #    MPItem.setField("molecular function", parse_go_category(get(root['go'], 'MF')))
    #    MPItem.setField("biological process", parse_go_category(get(root['go'], 'BP')))
    
    #PDB  - CHECK what if Human proteins donot have pdb Id?
    pdbs = rcsb.pdbs_for_uniprot(uniprot)
    if not pdbs:
        pdbs = get(root, 'pdb')
    MPItem.setField("PDB", pdbs)
    
    #For "encoded by" property search for corresponding gene item. If not present ,create it and obtain wikidata identifier
    #search_title = HGNC symbol
    key = get(root,'symbol') 
    ID = []
    res = wikidata.search_Item(key)
    #search for mouse gene, property = entrez 
    if res:
        entrezID = 'p351'
        ID = wikidata.search_claim(res,entrezID ,entrez)
    #search result is null or corresponding mouse gene doesnot exist
    if not ID:
        #create mouse gene item
        ID = wikidata.create_Item(key)
        print "creating mouse gene", entrez
        #add entrez claim to mouse gene item
        wikidata.addClaim(ID, 'p351',entrez)    
    MPItem.setField("encoded by", ID.title())
    
    return MPItem

#TO-DO EC classification
def parse_HumanProtein_json(gene_json):
    root = gene_json
    HPItem = HumanProtein()
    
    #found in taxon wikidata item human=Q5 , protein=Q8054
    #for proteins label= HGNC fullname
    HPItem.setField("Name", get(root,'name'))
    HPItem.setField("description", "human Protein")
    HPItem.setField("found in taxon", "Q5")
    HPItem.setField("subclass of","Q8054")
    name = get(root, 'name')
    HPItem.setField("Name", name)
    
    entrez = get(root, 'entrezgene')
    uniprot = findReviewedUniprotEntry(get(root, 'uniprot'), entrez)
    HPItem.setField("Uniprot ID", uniprot)
    
    # HPItem.setField("EC number", get(root, 'ec'))
    #adding refseq id's based on valid accession prefixes 
    initial = get(get(root, 'refseq'), 'protein')
    HPItem.setField("RefSeq Protein ID",parse_accession(initial,"RefSeq Protein ID"))
    HPItem.setField("Ensembl Protein ID", get(get(root, 'ensembl'), 'protein'))
    
    #Wikidata items for GO terms
    GO_ID = 'p686'
    if get(root, 'go'):
        GO_DICT = get(root,'go')
        for key in GO_DICT:
            res_list = GO_DICT[key]
            ID = []
            #single term
            if 'term' in res_list:
                title = res_list['term']
                res = wikidata.search_Item(title)
                if res:
                    #fix val['id']='GO:223'  remove the first three elements 
                    GID = wikidata.search_claim(res, GO_ID, res_list['id'][3:])
                    
                #Create GO Item if it does not exist
                if not GID:
                    GID = wikidata.create_Item(title)
                    print "created GO item ",GO_ID,GID
                    #add created id's for the go terms
                    
                    wikidata.addClaim(GID, GO_ID, res_list['id'][3:])
                ID.append(GID.title())
                
            else:
                #mutiple terms in go field              
                for val in res_list:
                #search for the item
                
                    title = val['term']
                # title has multiple words seperated by /   
                # found
                    if title.find('/') != -1:
                        match = re.search(r'([\w ]*)\/.*',title)
                        title = match.group(1)
                    res = wikidata.search_Item(title)
                    GID = []
                #search for the corresponding go term
                    if res:
                    #fix val['id']='GO:223'  remove the first three elements 
                        GID = wikidata.search_claim(res, GO_ID, val['id'][3:])
                    
                #Create GO Item if it does not exist
                    if not GID:
                        GID = wikidata.create_Item(title)
                        print "created GO item ",GO_ID,GID
                    #add created id's for the go terms
                    
                        wikidata.addClaim(GID, GO_ID, val['id'][3:])
                    ID.append(GID.title())
                
                

            if key == 'CC':
                HPItem.setField("cell component",ID)
            if key == 'MF':
                HPItem.setField("molecular function",ID)
            if key == 'BP':
                HPItem.setField("biological process",ID)
    
    #PDB
    pdbs = rcsb.pdbs_for_uniprot(uniprot)
    if not pdbs:
        pdbs = get(root, 'pdb')   
    HPItem.setField("PDB", pdbs)
    
    #For "encoded by" property search for corresponding gene item. If not present ,create it and obtain wikidata identifier
    #search_title = HGNC symbol
    key = get(root,'symbol') 
    ID = []
    res = wikidata.search_Item(key)
    #search for human gene, property = entrez 
    if res:
        entrezID = 'p351'
        ID = wikidata.search_claim(res,entrezID ,entrez)
    #search result is null or corresponding human gene doesnot exist
    if not ID:
        #create human gene item
        ID = wikidata.create_Item(key)
        print "created human gene", entrez
        #add entrez claim to human gene item
        wikidata.addClaim(ID, 'p351',str(entrez))    
    HPItem.setField("encoded by", ID.title())

    
    return HPItem
   


def get_homolog(gene, taxon, json):
    """Returns the homologous gene for a given gene in a given taxon.

    Arguments:
    - `gene`:  the original gene
    - `taxon`: the taxon of the species in which to find a homolog
    - `json`:  the mygene.info json document for original gene
    """
    homologs = get(get(json, 'homologene'), 'genes')
    # isolate our particular taxon (returns [[taxon, gene]])
    if homologs:
        pair  = filter(lambda x: x[0]==taxon, homologs)
        if pair:
            return pair[0][1]
        else: return None
    else: return None

def get_json_documents(entrez):
    """Returns the three JSON documents needed to construct a ProteinBox.
    Dict structure: {gene:json, meta:json, homolog:json}
    For use as a helper method for the parse_json() method.

    Arguments:
    - `entrez`: human gene entrez id
    """
    gene_json = getJson( BASE_URL + entrez )
    meta_json = getJson( META_URL )

    homolog = get_homolog(entrez, MOUSE_TAXON_ID, gene_json)
    homolog_json = getJson(BASE_URL+str(homolog)) if homolog else None

    return {'gene_json':gene_json, 'meta_json':meta_json, 'homolog_json':homolog_json}


def parse_json(gene_json, meta_json, homolog_json):
    '''construct human/mouse gene/protein'''
    HP = parse_HumanProtein_json(gene_json)
    
    HG = parse_HumanGene_json(gene_json,homolog_json)
    
    MP = parse_MouseProtein_json(homolog_json)   
    
    MG = parse_MouseGene_json(homolog_json,gene_json)
    
    return HG,HP,MG,MP
    
    
    
    
def Parse(entrez):
    
    return parse_json(**get_json_documents(entrez))

    
    
  
if __name__ == '__main__':
   Parse('1589')

 
  