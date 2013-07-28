'''
Created on Jul 10, 2013

@author: chinmay
'''
class Item(object):
        
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
        
        src = self.fieldsdict
        try:
            tgt = targetbox.fieldsdict
        except AttributeError:
            raise TypeError("Cannot update")
        if isinstance(targetbox,HumanGene):
            new = HumanGene()
        if isinstance(targetbox,HumanProtein):
            new = HumanProtein()
        if isinstance(targetbox,MouseGene):
            new = MouseGene()
        if isinstance(targetbox,MouseProtein):
            new = MouseProtein()
        updatedFields = {}
        for field in self.fields:
            srcval = src[field]
            tgtval = tgt[field]                

            if tgtval and srcval != tgtval:
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
        
    fields = [
              "Name",
              "description",
              "HGNC ID",
              "Homologene ID",
              "description",
              "gene symbol",
              "Entrez Gene ID",
              "OMIM ID",
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
              "AltSymbols",
              "species",
              "RefSeq RNA ID"
              ]
    
    multivalue = ["AltSymbols",
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
                         'p492' : 'OMIM'
    
    
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
            
    fields = [
              "Name",
              "description",
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
                         'p680' : 'molecular function ',
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
            
    fields = [
              "Name",
              "description",
              "EC number",              
              "PDB",
              "Uniprot ID",
              "molecular function",
              "cell component",
              "biological process",
              "RefSeq Protein ID",
              "found in taxon",
              "subclass of"
              
             ]
    
    multivalue = ["PDB",
                  "molecular function",
                  "cell component",
                  "biological process",
                  "RefSeq Protein ID",
                  "EC classification"
                   ]
    
    properties = {
                  
                         'p660' : 'EC classification',
                         'p638' : 'PDB',
                         'p352' : 'Uniprot ID',
                         'p637' : 'RefSeq Protein ID',
                         'p681' : 'cell component',
                         'p682' : 'biological process',
                         'p680' : 'molecular function ',
                         'p703'  : 'found in taxon' ,
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
        
    fields = [
              "Name",
              "MGI ID",     #mouse genome informatics ID
              "Homologene ID",
              "description",              
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
              "AltSymbols",
              "RNA ID"
              ]
    
    multivalue = ["AltSymbols",
                  "RefSeq",
                  "RNA ID"]
    
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
                        