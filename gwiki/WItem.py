'''
Created on Jul 10, 2013

@author: chinmay
'''
class Item(object):
    '''
    Serves as base class to Human/Mouse  Gene/Protein
    Contains source values for different claims
    Contains common methods needed by subclasses
    '''
    Entrez= 'Q1345229'
    Ensembl  = 'Q1344256'
    Uniprot  = 'Q905695'
    property_list_sources = {
              "HGNC ID"                 : Entrez  ,
              "Homologene ID"           : Entrez  ,
              "gene symbol"             : Entrez  ,
              "Entrez Gene ID"          : Entrez  ,
              "OMIM ID"                 : Entrez  ,
              "Ensembl Gene ID"         : Ensembl ,
              "ortholog"                : Entrez  ,
              "Ensembl Transcript ID"   : Ensembl ,
              "GenLoc_chr"              : Ensembl ,
              "GenLoc_start"            : Ensembl ,   
              "GenLoc_end"              : Ensembl ,
              "RefSeq"                  : Entrez  ,
              "AltSymbols"              : Entrez  ,
              "species"                 : Entrez  ,
              "RefSeq RNA ID"           : Entrez  ,
              "EC classification"       : Entrez  ,              
              "PDB"                     : Uniprot ,
              "Uniprot ID"              : Uniprot ,
              "molecular function"      : Entrez  ,
              "encoded by"              : Entrez  ,
              "cell component"          : Entrez  ,
              "biological process"      : Entrez  ,
              "RefSeq Protein ID"       : Entrez  ,
              "Ensembl Protein ID"      : Ensembl ,
              "Gene Ontology ID"        : Entrez  

                             
                             }
        
    def coerce_unicode(self, obj):
        if isinstance(obj, str):
            return unicode(obj, 'utf8')
        elif isinstance(obj, int):
            return unicode(str(obj), 'utf8')
        elif isinstance(obj, list):
            uni_obj = []
            for item in obj:
                item = self.coerce_unicode(item)
                uni_obj.append(item)
            return uni_obj
        else: 
            return obj
        
    def setField(self,field_name,field_value):
        '''Sets a field in the fieldsdict using the fields as a validity check.

        The field value must be a unicode object (some coercion will be tried, 
        but may fail).

        Obviously can be bypassed by changing fieldsdict directly, but this is
        not encouraged since it'll be ignored if it's incorrect.
        '''
        
        fieldsdict = self.fieldsdict
        field_value = self.coerce_unicode(field_value)
        
        if field_name in self.fields:
            if field_name in self.multivalue:
                if isinstance(field_value, list):
                    fieldsdict[field_name] = field_value
                elif field_value:
                    fieldsdict[field_name] = [field_value]
            else:
                if not isinstance(field_value, int):
                    pass
                fieldsdict[field_name] = field_value
        else:
            raise NameError("Specified field does not exist. Reference the fields list for valid names.")

        self.fieldsdict = fieldsdict
        return fieldsdict
    
    def updateWith(self, targetbox):
        '''
        Takes the fields from the target ProteinBox and this ProteinBox and selectively builds a new
        ProteinBox from the merger of the two. It decides which field to use to build the new object
        using the following rule:
        If the target's field value is missing or equal to this one's, this one's value is used. Otherwise,
        the target's value is used. (Easy enough).
        Returns the new ProteinBox with the new fields and a summary message describing the fields updated.
        Also returns a updatedFields dict, which stores data as such: {field_changed:(old, new), ...}
        '''
        
        src = self.fieldsdict
        try:
            tgt = targetbox.fieldsdict
        except AttributeError:
            raise TypeError("Cannot update")
        if isinstance(targetbox,HumanGene):
            new = HumanGene()
        elif isinstance(targetbox,HumanProtein):
            new = HumanProtein()
        elif isinstance(targetbox,MouseGene):
            new = MouseGene()
        else:
            new = MouseProtein()
        updatedFields = {}
        for field in self.fields:
            srcval = src[field]
            tgtval = tgt[field]                

            if tgtval and not(set(srcval) == set(tgtval)):
                updatedFields[field] = (srcval, tgtval)
                new.setField(field, tgtval)
            else:
                new.setField(field, srcval)


     
        summary = "The following claims were modified"
        if updatedFields:
            summary = "Updated {} claims: ".format(len(updatedFields))
            for field in updatedFields:
                summary = summary+field+", "
            summary = summary.rstrip(", ")

        return new, summary, updatedFields
    
    
#encodes, ortholog , Gene Atlas
class HumanGene(Item):
    '''
    The complete set of claims , property ids to construct a HumanGene wikidata item
    '''
        
    fields = [
              "Name",
              "description",
              "HGNC ID",
              "Homologene ID",
              "description",
              "gene symbol",
              "Entrez Gene ID",
              "OMIM ID",
	      "aliases",	
             # "GeneAtlas_image1",
             # "GeneAtlas_image2",
             # "GeneAtlas_image3",
              "Ensembl Gene ID",
              "ortholog",
              "Ensembl Transcript ID",
              "GenLoc_chr",
              "GenLoc_start",
              "GenLoc_end",
              "found in taxon",
              "subclass of",
              "encodes",
              "RefSeq",
     #         "AltSymbols",
              "species",
              "RefSeq RNA ID"
              ]
    
    multivalue = [#"AltSymbols",
		  "subclass of",
                  "RefSeq",
                  "Ensembl Transcript ID",
                  "RefSeq RNA ID"]
    
    properties = {
                         'p354' : 'HGNC ID',
                         'p593' : 'Homologene ID',
                         'p353' : 'gene symbol',
                         'p351' : 'Entrez Gene ID',
                        #'p692' : 'GeneAtlas image',  
                         'p594' : 'Ensembl Gene ID',
                         'p688' : 'encodes',
                         'p704' : 'Ensembl Transcript ID',
                         'p643' : 'GenLoc_chr',
                         'p89'  : 'species',
                         'p644' : 'GenLoc_start',
                         'p645' : 'GenLoc_end',
                         'p703' : 'found in taxon' ,
                         'p279' : 'subclass of',
                         'p639' : 'RefSeq RNA ID',
                         'p684' : 'ortholog',
                         'p656' : 'RefSeq',
                         'p492' : 'OMIM ID'
    
    
                        }
    
    def __init__(self):
        self.fieldsdict = {}
        for field in self.fields:
            if field in self.multivalue:
                self.fieldsdict[field]=u''
            else:
                self.fieldsdict[field]=u'' 
    
    
#encoded by 
class HumanProtein(Item): 
    '''
    The complete set of claims,property id's  to construct a HumanProtein Wikidata item
    '''
            
    fields = [
              "Name",
              "description",
	      "aliases",
              "EC number",
              "EC classification",              
              "PDB",
              "Uniprot ID",
              "molecular function",
              "encoded by",
              "cell component",
              "biological process",
              "RefSeq Protein ID",
              "Ensembl Protein ID",
              "found in taxon",
              "subclass of"
              
             ]
    
    multivalue = ["PDB",
		  "subclass of",
                  "molecular function",
                  "cell component",
                  "biological process",
                  "RefSeq Protein ID",
                  "Ensembl Protein ID",
                  "EC number"
                   ]
    
    properties = {
                    
                         'p660' : 'EC classification',
                         'p591' : 'EC number',
                         'p638' : 'PDB',
                         'p702' : 'encoded by',
                         'p352' : 'Uniprot ID',
                         'p637' : 'RefSeq Protein ID',
                         'p681' : 'cell component',
                         'p682' : 'biological process',
                         'p680' : 'molecular function',
                         'p703' : 'found in taxon' ,
                         'p279' : 'subclass of',
                         'p705' : 'Ensembl Protein ID'
                         
                        }
    
    def __init__(self):
        self.fieldsdict = {}
        for field in self.fields:
            if field in self.multivalue:
                self.fieldsdict[field]=u''
            else:
                self.fieldsdict[field]=u''     
                
                
class MouseProtein(Item): 
    '''
    The complete set of fields to construct a MouseProtein Wikidata item
    '''
            
    fields = [
              "Name",
              "description",
	      "aliases" ,
              "EC number",              
              "PDB",
              "Uniprot ID",
              "molecular function",
              "cell component",
              "biological process",
              "RefSeq Protein ID",
              "encoded by",
              "found in taxon",
              "Ensembl Protein ID",
              "subclass of",
              "EC classification"
              
             ]
    
    multivalue = ["PDB",
		  "subclass of",
                  "molecular function",
                  "cell component",
                  "biological process",
                  "RefSeq Protein ID",
                  "Ensembl Protein ID"
                   ]
    
    properties = {
                  
                         'p660' : 'EC classification',
                         'p638' : 'PDB',
                         'p352' : 'Uniprot ID',
                         'p637' : 'RefSeq Protein ID',
                         'p702' : 'encoded by',
                         'p681' : 'cell component',
                         'p682' : 'biological process',
                         'p680' : 'molecular function',
                         'p703'  : 'found in taxon' ,
                         'p705' : 'Ensembl Protein ID',
                         'p279' : 'subclass of'
                         
                         
                        }
    
    def __init__(self):
        self.fieldsdict = {}
        for field in self.fields:
            if field in self.multivalue:
                self.fieldsdict[field]=u''
            else:
                self.fieldsdict[field]=u''
                
                
class MouseGene(Item):
    '''
    The complete set of fields to construct a MouseGene Wikidata item
    '''    
    fields = [
              "Name",
              "MGI ID",     #mouse genome informatics ID
              "Homologene ID",
              "description",              
	      "aliases" ,	
              "gene symbol",
              "Entrez Gene ID",
              "Ensembl Gene ID",
              "Ensembl Transcript ID",
              "GenLoc_chr",
              "GenLoc_start",
              "GenLoc_end",
              "found in taxon",
              "subclass of",
              "RefSeq",
              "species",
              "ortholog",
              "encodes",
             # "AltSymbols",
              "RefSeq RNA ID"
              ]
    
    multivalue = [#"AltSymbols",
		  "subclass of",
                  "RefSeq",
                  "Ensembl Transcript ID",
                  "RefSeq RNA ID"]
    
    properties = {
                         'p671' : 'MGI ID',
                         'p593' : 'Homologene ID',
                         'p89'  : 'species',
                         'p353' : 'gene symbol',
                         'p351' : 'Entrez Gene ID',
                         'p594' : 'Ensembl Gene ID',
                         'p704' : 'Ensembl Transcript ID',
                         'p688' : 'encodes',
                         'p643' : 'GenLoc_chr',
                         'p644' : 'GenLoc_start',
                         'p684' : 'ortholog',
                         'p645' : 'GenLoc_end',
                         'p703'  : 'found in taxon' ,
                         'p279' : 'subclass of',
                         'p639' : 'RefSeq RNA ID',
                         'p656' : 'RefSeq'
                        }
    
    def __init__(self):
        self.fieldsdict = {}
        for field in self.fields:
            if field in self.multivalue:
                self.fieldsdict[field]=u''
            else:
                self.fieldsdict[field]=u'' 
                        
