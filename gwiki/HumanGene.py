#Retained most of previous proteinbox
class HumanGene(object):
    
    fields = [
              "Name",
              "HGNC ID",
              "Homologene ID",
              "Symbol",
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
                  "RNA ID",
                  "RefSeq",]
    
    HGene_properties = {
                        'HGNC ID' :'p354',
                        'Homologene ID' : 'p593',
                        'gene symbol' : 'p353' ,
                        'Entrez Gene ID' : 'p351',
                      #  'GeneAtlas image' : '',  #yet to be created
                        'Ensembl ID' : 'p594',
                        'GenLoc_chr' : 'p643',
                        'Genloc start' :'p644',
                        'Genloc end' : 'p645',
                        'species' : 'p89' ,
                        'subclass of' : 'p279',
                        'RNA ID' : 'p639',
                        'RefSeq' : 'p656'
                        }
    

    def __init__(self):
        self.fieldsdict = {}
        for field in self.fields:
            if field in self.multivalue:
                self.fieldsdict[field]=u''
            else:
                self.fieldsdict[field]=u'' 
        
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
        
                        