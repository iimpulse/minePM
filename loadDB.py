#!/bin/python
from Bio import Entrez
from pymongo import MongoClient
from Bio import Medline
import logging
import os,sys
from datetime import date

######################################
# Updates August 13,2016 LOADING
# 
# After loading the files from old script
# 	-> Modify to check each folder for new data
#	-> If folders are empty move on, else load the new data
#	
#
#


def updateDBdata(cancer):
	client = MongoClient('mongodb://localhost:27017/')
	db = client['minepm']
	Entrez.email = "gargano.mi@husky.neu.edu"    # Always tell NCBI who you are
	if(cancer == "bladder"):
		collection = db.bladdercancer
		dir = './data/bladder/'
	elif(cancer == "lung"):
		collection = db.lungcancer
		dir = "./data/lung/"
	elif(cancer == "prostate"):
		collection = db.prostatecancer	
		dir = "./data/prostate/"
	elif(cancer == "colon"):
		collection = db.coloncancer
		dir = "./data/colon/"
	elif(cancer == "pancreatic"):
		collection = db.pancreaticcancer
		dir = "./data/pancreatic/"
	for f in os.listdir(dir):
		handle = open(dir + f,'r')
		records = Entrez.read(handle)
		for x in records['PubmedArticle']:
			try:
				abstract = x['MedlineCitation']['Article']['Abstract']['AbstractText']
				abstract = "".join(abstract)
				pmid = x['MedlineCitation']['PMID']
				title = x['MedlineCitation']['Article']['ArticleTitle']
				author = []
				for z in x['MedlineCitation']['Article']['AuthorList']:
					try:
						auth = z['LastName'] + " " + z['Initials']
						author.append(auth)
					except Exception,e:
						continue
				author.sort()
				authors = " , ".join(author)	
				item  = {"pmid": pmid,"title":title,"ab": abstract,"authors":authors}
				collection.insert(item)
			except Exception,e:
				continue
	        handle.close()
		os.remove(dir + f)
	client.close()

def main():
	updateDBdata("pancreatic")
	updateDBdata("bladder")
	updateDBdata("colon")
	updateDBdata("lung")
	updateDBdata("prostate")
	stamp = date.today().isoformat()
	handle = open('data/log.txt','w')
	handle.write(stamp)

	

if __name__ == "__main__":
	main()
	
