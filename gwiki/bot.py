'''
Created on Jun 20, 2013

@author: chinmay
'''
import pywikibot


class bot:
    #CHECK path to log file. previous bot log fie was ---> "http://api.genewikiplus.org/log/submit"
    log_file_path = "/home/chinmay/GSOC-rough/log1.txt"
    log=[]
    def __init__(self,genewiki):
        try:
            #TO-DO check for rewrite branch explicitly. Check valid loginID
            assert pywikibot
            assert genewiki
        except AssertionError:
            raise TypeError("Setup pywikipedia-rewrite.")
        
    
    def run():
        entrez = infoboxes_entrez()
        getinfo(entrez)
    