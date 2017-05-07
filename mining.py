import re, csv,string
from pymongo import MongoClient
from multiprocessing import Pool
from itertools import repeat
class geneMatrix:
	def __init__(self):
		self.matrix = [[ x for x in range(11)] for x in range(39799)]
		self.matrix[0][0] = "GeneSymbol"
    		self.matrix[0][1] = "BladderCancer"
   		self.matrix[0][2] = "LungCancer"
    		self.matrix[0][3] = "ProstateCancer"
    		self.matrix[0][4] = "ColonCancer"
    		self.matrix[0][5] = "PancreaticCancer"
    		self.matrix[0][6] = "BladderArticles"
    		self.matrix[0][7] = "LungArticles"
    		self.matrix[0][8] = "ProstateArticles"
    		self.matrix[0][9] = "ColonArticles"
    		self.matrix[0][10] = "PancArticles"
		self.counter = 0		
		self.row_find = {}

	def setMatrix(self,lib,num,article):
		self.counter = self.counter + 1
		if(self.counter == 1):
			count = 0
			for key, value in lib.iteritems():
		        	count = count + 1
		      		self.row_find[key] = count  
		      		if(value[0] >= 1): 
					self.matrix[count][0] = key
					self.matrix[count][num] = value[0]
					self.matrix[count][article] =",".join(value[1:])
		      		else:
					self.matrix[count][0] = key
					self.matrix[count][num] = 0
					self.matrix[count][article] = "NA"
		else:
			for key, value in lib.iteritems():
				count = self.row_find[key]
				if(value[0] >=1):
					self.matrix[count][num] = value[0]
					self.matrix[count][article] = ",".join(value[1:])
				else:
					self.matrix[count][num] = 0
					self.matrix[count][article] = "NA"


class geneInit:
	def __init__(self):
		self.list = self.returnGeneList()
		self.dict  = self.create_dict()
        def returnGeneList(self):
	    with open('./data/genes-new.txt','rb') as csvfile:
		genereader = csv.reader(csvfile,delimiter='\n')
		genesym = []
		for row in genereader:
		   row = row[0].split()
		   row = row[0]
		   genesym.append(row) 
		genesym.pop(0)
		return genesym
	def create_dict(self):
		gene = self.list
  		gene_dict = {}
  		for  i in range(0,len(gene)):
    			gene_dict[str(gene[i])] = [0] 
  		return gene_dict

				
 
def connectDB():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['minepm']
    return db


def extractGeneData((cancer,geneDict)):
    gene_dict = geneDict
    #gene_dict = reset_dict() 
    #open db connection,get the cancer collection
    #loop through collection
    #Do original analysis
    #client = MongoClient('mongodb://localhost:27017/')
    #db = client['minepm']
    db = connectDB()
    count = 0 
    if(cancer == "bladder"):
	collection = db.bladdercancer.find()
    elif(cancer == "lung"):
	collection = db.lungcancer.find()
    elif(cancer == "prostate"):
	collection = db.prostatecancer.find()
    elif(cancer == "colon"):
	collection = db.coloncancer.find()
    elif(cancer == "pancreatic"):
	collection = db.pancreaticcancer.find()
    for x in collection: 
	abst =  x['ab']
	abst = abst.split(" ")
	abst = map(lambda s: s.encode('ascii','ignore').upper(),abst)
	abst = map(lambda s: s.strip(string.punctuation),abst)
	abst = set(abst)
	abst = map(lambda s: s,abst)
	pmid = x["pmid"].encode('ascii','ignore')
	for i in range(0,len(abst)):
	    word = abst[i].strip()
	    #print word
	    try:
		valueMatch = gene_dict[word]
		if (valueMatch != 0):
		    valueMatch[0] = valueMatch[0] + 1
		    valueMatch.append(pmid)
		    gene_dict[word] = valueMatch
		else:
		    newlist = []
		    newlist.append(1)
		    newlist.append(pmid)
		    gene_dict[word] = newlist
	    except Exception,e:
		continue
    return gene_dict

def writecsv(data):
    csvfile = "./matrix-test.csv"
    with open(csvfile, "w") as output:
      writer = csv.writer(output, lineterminator='\n')
      writer.writerows(data)
    print "Finished Writing."
def row_find_init():
    gene = geneInit()
    gene = gene.list
    row_find = {}
    for i in range(0,len(gene)):
        row_find[str(gene[i])] = 0
    return row_find

def readcsv():
    db = connectDB()
    flag = 0
    with open("./matrix-test.csv",'r') as dat:
        reader = csv.reader(dat)
        for row in reader:
            flag = flag + 1
            if(flag != 1):
                db.genes.update({'gene':row[0]},{'$set':{'bcid':row[6],'lcid':row[7],'pcid':row[8],'ccid':row[9],'pncid':row[10]}})
            else:
                continue
					


def main():
    print "Gathering data and performing analysis...please wait"
    #For each cancer type find genes, add to the matrix

    # list bladder,lung,prostate,colon,pancreatic
    # make a thread pool
    # for cancer create a threader and call extract gene data
    # when one returns, inset into the matrix.
    miner = geneMatrix()
    geneDict = geneInit()
    geneDict = geneDict.dict
    miner.row_find = row_find_init()	#gene dictionairy for row position
    cancers = ["bladder","lung","prostate","colon","pancreatic"]
    pool = Pool(processes = len(cancers))
    result = pool.map(extractGeneData,zip(cancers,repeat(geneDict)))
    pool.close()
    print "Setting Matrix, Writing Matrix"
    miner.setMatrix(result[0],1,6)
    miner.setMatrix(result[1],2,7)
    miner.setMatrix(result[2],3,8)
    miner.setMatrix(result[3],4,9)
    miner.setMatrix(result[4],5,10) 
    writecsv(miner.matrix) # write the result of the genes vs types matrix
    #readcsv() # if updating mongodb, genes file use this
    print "Done"

if __name__ == "__main__":
	main()
