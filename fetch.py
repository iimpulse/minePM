import urllib2  # to read file from url
from Bio import Entrez
import logging
import time,subprocess,os
from urllib2 import HTTPError
from datetime import date

Entrez.email = "gargano.mi@husky.neu.edu"     # Always tell NCBI who you are
cancers = ["lung","bladder","pancreatic","prostate","colon"]
handle = open("data/log.txt",'r')
dateFrom = handle.read()
handle.close()
for cancer in cancers:
	# compile esearch function for To FROM date
	#handle = Entrez.esearch(db="pubmeD",term="(\"" + cancer + "\"[Title/Abstract]) AND (\"" + dateFrom + "\"[Date - Publication] : \"3000\"[Date - Publication])",retmax=25000) 
	print "Entrez search for " + cancer 
	handle = Entrez.esearch(db="pubmed", term="(\"" + cancer + " cancer\"[Title/Abstract])", retmax=25000)
	record = Entrez.read(handle)
	idlist = record["IdList"]
	print "Fetching and Parsing " + str(len(idlist)) + " " + cancer + " records" 
	fileNum = 1
	end = len(idlist) + 200
	for i in range(0,end,200):
		slice = idlist[i:i+200]
		for attempt in range(10):
			try:
				handle = Entrez.efetch(db="pubmed", retmode="XML",rettype = "", id=",".join(slice),retstart=1,retmax=200)
				xml = urllib2.urlopen(handle.url)
				text = xml.read() # convert contents to string
			  
				# save to file BC_#.xml
				fileName = "./data/" + cancer + "/file_"+str(fileNum)+".xml"
				f = open(fileName, "w")
				f.write(text)
				f.close()
				line = subprocess.check_output(['tail', '-1', fileName])[0:-1]
				if(line == "</html>"):
					os.remove(fileName)
					raise NameError('Error 500 during write')	
				fileNum = fileNum + 1
				handle.close()
				break
				
			except (HTTPError,NameError),e:
				logging.warning(e)
				handle.close()
				time.sleep(5)
				continue
		
