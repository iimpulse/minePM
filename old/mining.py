import re, csv,string
from pymongo import MongoClient
def connectDB():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['minepm']
    return db


def extractGeneData(cancer,gene_dict):
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
    
def returnGeneList():
    with open('./data/genes-new.txt','rb') as csvfile:
        genereader = csv.reader(csvfile,delimiter='\n')
        genesym = []
        for row in genereader:
           row = row[0].split()
           row = row[0]
           genesym.append(row) 
        genesym.pop(0)
        return genesym

def writecsv(data):
    csvfile = "./matrix.csv"
    with open(csvfile, "w") as output:
      writer = csv.writer(output, lineterminator='\n')
      writer.writerows(data)
def reset_dict():
  gene = returnGeneList()
  gene_dict = {}
  for  i in range(0,len(gene)):
    gene_dict[str(gene[i])] = [0] 
  return gene_dict

def row_find_init():
    gene = returnGeneList();
    row_find = {}
    for i in range(0,len(gene)):
        row_find[str(gene[i])] = 0
    return row_find

def readcsv():
    db = connectDB()
    flag = 0
    with open("./matrix.csv",'r') as dat:
        reader = csv.reader(dat)
        for row in reader:
            flag = flag + 1
            if(flag != 1):
                db.genes.update({'gene':row[0]},{'$set':{'bcid':row[6],'lcid':row[7],'pcid':row[8],'ccid':row[9],'pncid':row[10]}})
            else:
                continue
			#row[0] is gene symbol
			#row[6] is bladder cancer
			#row[7] is lung cancer
			#row[8] is prostate cancer
			#row[9] is colon
			#row[10] is pancreatic cancer
			# Get the connection and 		


def main():
    # Define Matrix (col)(row)
    #39825
    Matrix = [[ x for x in range(11)] for x in range(39799)]
    Matrix[0][0] = "GeneSymbol"
    Matrix[0][1] = "BladderCancer"
    Matrix[0][2] = "LungCancer"
    Matrix[0][3] = "ProstateCancer"
    Matrix[0][4] = "ColonCancer"
    Matrix[0][5] = "PancreaticCancer"
    Matrix[0][6] = "BladderArticles"
    Matrix[0][7] = "LungArticles"
    Matrix[0][8] = "ProstateArticles"
    Matrix[0][9] = "ColonArticles"
    Matrix[0][10] = "PancArticles"
    print "Gather data and performing analysis...please wait"
    #For each cancer type find genes, add to the matrix
    gene_dict = reset_dict() # gene dictionary for ids
    row_find = row_find_init()	#gene dictionary for row positioni	
    bladder = extractGeneData("bladder",gene_dict)  
    count = 0
    for key, value in bladder.iteritems():
      count = count + 1
      row_find[key] = count  
      if(value[0] >= 1): 
        Matrix[count][0] = key
        Matrix[count][1] = value[0]
        Matrix[count][6] =",".join(value[1:])
      else:
        Matrix[count][0] = key
        Matrix[count][1] = 0
        Matrix[count][6] = "NA"
    
    gene_dict = reset_dict()
    lung =  extractGeneData("lung",gene_dict)
    for key,value in lung.iteritems():
        count = row_find[key]
        if(value[0] >=1):
            Matrix[count][2] = value[0]
            Matrix[count][7] = ",".join(value[1:])
        else:
            Matrix[count][2] = 0
            Matrix[count][7] = "NA"
    gene_dict = reset_dict()
    prostate = extractGeneData("prostate",gene_dict)
    for key,value in prostate.iteritems():   
        count = row_find[key]
        if(value[0] >= 1):
            Matrix[count][3] = value[0]
            Matrix[count][8] = ",".join(value[1:])
        else:
            Matrix[count][3] = 0
            Matrix[count][8] = "NA"    
    gene_dict = reset_dict()
    colon  = extractGeneData("colon",gene_dict)
    for key,value in colon.iteritems():   
        count = row_find[key]
        if(value[0] >= 1):
            Matrix[count][4] = value[0]
            Matrix[count][9] = ",".join(value[1:])
        else:
            Matrix[count][4] = 0
            Matrix[count][9] = "NA"
    gene_dict = reset_dict()
    panc  = extractGeneData("pancreatic",gene_dict)
    for key,value in panc.iteritems():   
        count = row_find[key]
        if(value[0] >= 1):
            Matrix[count][5] = value[0]
            Matrix[count][10] = ",".join(value[1:])
        else:
            Matrix[count][5] = 0
            Matrix[count][10] = "NA"
    writecsv(Matrix) # write the result of the genes vs types matrix
    #readcsv() # if updating mongodb, genes file use this
    print "Data analyzed and written to matrix.csv"


if __name__ == "__main__":
	main()
