The Gene Wiki Project
======================================================================

Background
----------------------------------------------------------------------
The [Gene Wiki](http://en.wikipedia.org/wiki/Portal:Gene_Wiki) project
on [Wikipedia](http://en.wikipedia.org) is an initiative to create a
comprehensive review article for every notable human gene. There are
currently over 10,400 human genes in the Gene Wiki, and more are added
at a steady rate.

We have developed a number of tools to analyze, expand and maintain
the Gene Wiki project. While initial development was largely in Java,
much of the core code is actively being ported to Python to facilitate
use in scripting and ease-of-use.

Projects
----------------------------------------------------------------------
The following projects all fall under the Gene Wiki umbrella:

- [__pygenewiki__](https://bitbucket.org/sulab/pygenewiki) : code to 
  update and expand Gene Wiki pages and resources. Includes ProteinBoxBot,
  the GeneWiki API, and GeneWiki Generator (a BioGPS plugin).
  
  
- __ProteinBoxBot__(this project): Wikidata bot to upload gene data
  onto Wikidata.


- [__mediawiki-sync__](https://bitbucket.org/sulab/mediawiki-sync): a 
  Java daemon that copies changes from one MediaWiki installation to 
  another, created to support the Gene Wiki mirror at
  [GeneWiki+](http://genewikiplus.org).

- [__genewiki-miner__](https://bitbucket.org/sulab/genewiki-miner):
  code related to information extraction and parsing for many of the
  papers and analyses we've done on the Gene Wiki.

- [__genewiki-commons__](https://bitbucket.org/sulab/genewiki-commons):
  Common code used across Java projects (required as a Maven
  dependency)

- [__genewiki-generator__](https://bitbucket.org/sulab/genewiki-generator):
  Previous version of this project, written in Java. Provides the
  ProteinBoxBot and GeneWiki Generator (bioGPS plugin).
  
  __ProteinBoxBot__
======================================================================
ProteinBoxBot is a wikidata bot for maintaing Human(&Mouse) Gene(&Protein) items on [Wikidata](http://www.wikidata.org/wiki/Wikidata:Main_Page). 
PBB retreives information about genes through [MyGene,info](http://mygene.info/) and creates/updates/maintains Gene items on Wikidata
eg Reelin [wikidata_item](https://www.wikidata.org/wiki/Q414043).
In due course, the Protein Box templates of Gene Wikipedia articles (eg [Reelin]()) will source their information from these Gene Wikidata items.

Installation
----------------------------------------------------------------------
The bot only requires [Pywikibot framework](https://www.mediawiki.org/wiki/Manual:Pywikipediabot). The detailed installation steps for the 
framework are [here](https://www.mediawiki.org/wiki/Manual:Pywikipediabot/Installation).

Quick Start Guide
----------------------------------------------------------------------
The bot runs in two modes:

 - Normal sequential mode-- It retreives the set of entrez id's from [genewikiplus](http://api.genewikiplus.org/map/). The id's returned from GW+ is the order in which the bot runs.

  Command  -- sudo python bot.py

 - Specified mode --- Specify a text file with list of entrez id's. The bot will run for these entrez id's only.
  
  Command  -- sudo python bot.py --only /path/to/file

The file contents should be of the folowing format.

only=[<list of entrez id's>]  Ex: only=[5649,362]



