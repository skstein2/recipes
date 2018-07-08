library(ggplot2)
library(tm)
library(SnowballC)
library(NLP)
library(qlcMatrix)
library(proxy)
library(dplyr)
library(tidytext)
library(tidyr)
library(stringr)
library(wordcloud)
library(RColorBrewer)
setwd("~/Desktop/allrecipes")

# Load data from allrecipes.com
data1 <- read.table("indian10.txt", header=FALSE, quote="", sep="|")
data2 <- read.table("indian20.txt", header=FALSE, quote="", sep="|")
data3 <- read.table("indian30.txt", header=FALSE, quote="", sep="|")
data2$V2 <- as.factor(data2$V2)
data3$V2 <- as.factor(data3$V2)
data <- rbind(data1, data2, data3)

# Clean data
names(data) <- c("recipetitle", "madeitcount", "reviewcount", "starrating", "readyintime", "ingredients", "steps", "categories")
data <- data[!duplicated(data$recipetitle),]

# What ingredients do I need to cook Indian food?
ingredients <- VCorpus(VectorSource(data$ingredients))
ingredients <- tm_map(ingredients, removeNumbers)
ingredients <- tm_map(ingredients, removePunctuation)
ingredients <- tm_map(ingredients, content_transformer(tolower))
ingredients <- tm_map(ingredients, removeWords, stopwords("english"))
ingredients <- tm_map(ingredients, stripWhitespace)
writeLines(as.character(ingredients[[1]]))

BigramTokenizer <- function(x) unlist(lapply(ngrams(words(x), 2), paste, collapse=" "), use.names=FALSE)
ingredients_dtm <- as.matrix(DocumentTermMatrix(ingredients, control=list(tokenize=BigramTokenizer)))
ingredients_dtm_binary <- ifelse(ingredients_dtm>=1, 1, 0)
ingredients_tf <- ingredients_dtm
ingredients_idf <- log(nrow(ingredients_dtm)/colSums(ingredients_dtm_binary))
ingredients_tfidf <- ingredients_dtm
for (word in names(ingredients_idf)){
  ingredients_tfidf[,word] <- ingredients_tf[,word] * ingredients_idf[word]
}

ingredients_tfidf_means <- colMeans(ingredients_tfidf)
ingredients_tfidf_means <- rev(ingredients_tfidf_means[order(ingredients_tfidf_means)])
ingredients_tfidf_means[1:25]



