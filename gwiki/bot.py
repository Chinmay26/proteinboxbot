'''
Created on Jun 20, 2013

@author: chinmay
'''
import pywikibot
import genewiki,mygeneinfo,genewikidata

class bot(object):
    #CHECK path to log file. previous bot log file was ---> "http://api.genewikiplus.org/log/submit"
    #log_file_path = "/home/chinmay/GSOC-rough/log1.txt"
    #log=[]
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

def main():
    BOT = bot(genewiki.Genewiki())
    BOT.run()
    
if __name__ == '__main__':
    main()
    