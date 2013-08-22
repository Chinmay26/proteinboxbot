'''
Created on Aug 20, 2013

@author: chinmay
'''
import urllib2,json


def getResult():
    url = "http://api.genewikiplus.org/map/"
     
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        result  = response.read()
        result = result.decode('utf-8')
        gene_list = json.loads(result)
        
        for entry in gene_list:
            yield (entry['entrez_id'],entry['title_url'])
        
        
      
    except urllib2.HTTPError as e:
        raise e     
    except IOError as e:
        print("Network error")
        raise e
  
def getTitle(entrez):
    url = "http://api.genewikiplus.org/map/"
    url = url + str(entrez)
    
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        result  = response.read()
        return result
    except urllib2.HTTPError as e:
        raise e     
    except IOError as e:
        print("Network error")
        raise e
    
        
#if __name__=='__main__':
#    query_res = getResult()
    
#    for k,s in query_res:
#        print k,s
#   print getTitle(5649)
    