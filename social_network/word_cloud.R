word_cloud <- function(name){
	library(twitteR)
	library(ROAuth)
	library(RCurl)
	library(tm)
 	#authentication
	download.file(url="http://curl.haxx.se/ca/cacert.pem",destfile="cacert.pem")
	consumerKey <-'JhbIkTRGSPc2RQ3AbxQuV9KOq'
	consumerSecret <-'iMskFIQt13IssJJhfF2VOUiZn2ZtRc6Ex7URYr6Z2ssRqBaTtQ'
	accessToken <-'3338047535-X1RKOdmaPSrLFnVHsHOI4ijlnQ37U2IP0ujkVzK'
	accessTokenSecret <-'aHJTt5Hu83jpBa6MLftVzb671ThNfOKpEsC6jsnUm17VS'
	v <- setup_twitter_oauth(consumerKey, consumerSecret, accessToken, accessTokenSecret)
	save(v, file="my_oauth")
	#search
	ted2_tweets= searchTwitter('name',n=500,lang="en")
	ted2_text = sapply(ted2_tweets, function(x) x$getText())
	#data cleaning
	ted2_text <- gsub("rt", "", ted2_text)
	ted2_text <- gsub("@\\w+", "", ted2_text)
	ted2_text <- gsub("[[:punct:]]", "", ted2_text)
	ted2_text <- gsub("http\\w+", "", ted2_text)
	ted2_text <- gsub("[ |\t]{2,}", "", ted2_text)
	ted2_text <- gsub("^ ", "", ted2_text)
	ted2_text <- gsub(" $", "", ted2_text)
	ted2_corpus = Corpus(VectorSource(ted2_text))
	tdm = TermDocumentMatrix(ted2_corpus, control = list(removePunctuation=TRUE,stopwords=c("#ted2", stopwords("english")),removeNumbers= TRUE))
	#formatting
	m = as.matrix(tdm)
	word_freqs = sort(rowSums(m), decreasing=TRUE)
	dm = data.frame(word=names(word_freqs), freq=word_freqs)
	wordcloud(dm$word, dm$freq, ,max.words=100, random.order=FALSE, colors=brewer.pal(8, "Dark2"))
}