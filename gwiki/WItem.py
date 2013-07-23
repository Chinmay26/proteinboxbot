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
    
class HumanGene(Item):
        
    fields = [
              "Name",
              "HGNC ID",
              "Homologene ID",
              
              "gene symbol",
              "Entrez Gene ID",
             # "GeneAtlas_image1",
             # "GeneAtlas_image2",
             # "GeneAtlas_image3",
              "Ensembl ID",
              "GenLoc_chr",
              "GenLoc_start",
              "GenLoc_end",
              "species",
              "subclass of",
              "RefSeq",
              "AltSymbols",
              "RNA ID"
              ]
    
    multivalue = ["AltSymbols",
                  "RefSeq",
                  "RNA ID"]
    
    properties = {
                         'p354' : 'HGNC ID',
                         'p593' : 'Homologene ID',
                         'p353' : 'gene symbol',
                         'p351' : 'Entrez Gene ID',
                        #'GeneAtlas image' : '',  #yet to be created
                         'p594' : 'Ensembl ID',
                         'p643' : 'GenLoc_chr',
                         'p644' : 'GenLoc_start',
                         'p645' : 'GenLoc_end',
                         'p89'  : 'species' ,
                         'p279' : 'subclass of',
                         'p639' : 'RNA ID',
                         'p656' : 'RefSeq'
                        }
    
    def __init__(self):
        self.fieldsdict = {}
        for field in self.fields:
            if field in self.multivalue:
                self.fieldsdict[field]=u''
            else:
                self.fieldsdict[field]=u'' 
    
    
    
class HumanProtein(Item): 
            
    fields = [
              "Name",
              "description",
              "chemical structure",
              "EC number",              
              "PDB",
              "Uniprot ID",
              "molecular function",
              "cell component",
              "biological process",
              #"RefSeq Protein ID"
              "species",
              "subclass of"
              
             ]
    
    multivalue = ["PDB",
                  "molecular function",
                  "cell component",
                  "biological process",
                  #"RefSeq Protein ID",
                  "EC classification"
                   ]
    
    properties = {
                         'p117' : 'chemical structure',
                         'p660' : 'EC classification',
                         'p638' : 'PDB',
                         'p352' : 'Uniprot ID',
                         'p637' : 'RefSeq Protein ID',
                         'p681' : 'cell component',
                         'p682' : 'biological process',
                         'p680' : 'molecular function ',
                         'p89'  : 'species' ,
                         'p279' : 'subclass of'
                         
                         
                        }
    
    def __init__(self):
        self.fieldsdict = {}
        for field in self.fields:
            if field in self.multivalue:
                self.fieldsdict[field]=u''
            else:
                self.fieldsdict[field]=u''     
                        