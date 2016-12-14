##############################
#
# minePM Analysis R script
# 
# Michael Gargano 
#################################
# get data from csv file
data = read.csv("~/develop/minePM/matrix.csv")
#remove insignificant values
data = data.frame(data[data$BladderCancer>=3 & data$LungCancer >=3 & data$ProstateCancer >=3 & data$ColonCancer >= 3 & data$PancreaticCancer >=3,])
#################################################################
# Creating dataframe of sum counts
data.sum = apply(data[,2:6],1,sum) #Sum total Amounts
o = order(data.sum)
data.match = data.frame(data[,1],data.sum) # match genename with total counts
o = order(data.match[,2],decreasing=TRUE)
View(data[o,1:6])
#data.top = subset(data.match,data.match[,1] >=3) # subset the data to greater than sum 3
colnames(data.match) <- c("GeneSymbol","TotalCount")
#################################################################
## change the column and the index
g1.articles <- c()
for(i in 1:5){
  art = as.character(data[,i+6])
  art.all = strsplit(art,",")
  u = unlist(art.all)
  u.count = unique(u)
  g1.articles[i] = length(u.count)
}
# conver this apply


################################################################
#DENDROGRAM OF TOP 10 Most Hit GENES
data.top.sorted = data.match[order(data.match[,2],data.match[,1],decreasing=TRUE),]
top.25.genes = data.top.sorted[1:10,1]
m = match(top.25.genes, data[,1])
res.new = data[m,2:6]
res.new.h = data[m,1:6]
# vector articles with at least 1 gene
res = t(t(data[m,2:6])/g1.articles)
res.h = t(t(data[m,2:6])/g1.articles)# scale the data by column
heatmap(res.h,col = colorRampPalette(c("green","red"))(100)) # heatmap
d <- dist(res, method = "euclidean") # distance matrix
fit <- hclust(d, method="ward.D2") 
plot(fit,labels = data[m,1]) # display dendogram
################################################################

################################################################
#DENDROGRAM FOR CANCER TYPES distance based
#function for clustering
plot.clust <-function(x) {
  d = dist(t(x))
  print(d)
  h = hclust(d)
  plot(h)
}
res.c <- t(t(data[,2:6])/g1.articles) #Scale the data by columns
res.c = res.c / rowSums(res.c) # Scale by row
#CLuster shows which cancer types are most similar
plot.clust(res.c)
################################################################

################################################################
# percent of articles with genes found
total.art <- c(20991,21793,21417,22440,21590)
prct.art <- g1.articles/total.art
barplot(prct.art,xlab = "Tumor Type", ylab="Frequency (%)",
        col =c("red","green","blue","orange","yellow"),legend=colnames(data[,2:6]),args.legend= c(x=1.5,y=-4.1),main ="Proportion of 1 Gene Found Across Tumor Types")
# percent of average amount of genes per tumor type
sums.col = colSums(data[,2:6])
prct.genes = sums.col / g1.articles
barplot(prct.genes,xlab = "Tumor Type", ylab="Frequency (Integer)",
        col =c("red","green","blue","orange","yellow"),main ="Frequency of Genes Per Abstracts Across Tumor Types")
legend("topright",legend=colnames(data[,2:6]),fill = c("red","green","blue","orange","yellow"),lty)
############################################3

#CHI SQUARE TEST

chi <- function(i,d,t){
  mt = rbind(d[i,2:6],t - d[i,2:6])
  f = chisq.test(mt)
 
   return(f$p.value)
}



res.chi <- sapply(1:nrow(data),chi,d=data,t=g1.articles)




