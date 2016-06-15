count_of_tweets <- function(name){
	library(twitteR)
	library(ROAuth)
	library(RCurl)
 	download.file(url="http://curl.haxx.se/ca/cacert.pem",destfile="cacert.pem")
	consumerKey <-'JhbIkTRGSPc2RQ3AbxQuV9KOq'
	consumerSecret <-'iMskFIQt13IssJJhfF2VOUiZn2ZtRc6Ex7URYr6Z2ssRqBaTtQ'
	accessToken <-'3338047535-X1RKOdmaPSrLFnVHsHOI4ijlnQ37U2IP0ujkVzK'
	accessTokenSecret <-'aHJTt5Hu83jpBa6MLftVzb671ThNfOKpEsC6jsnUm17VS'
	v <- setup_twitter_oauth(consumerKey, consumerSecret, accessToken, accessTokenSecret)
	save(v, file="my_oauth")
	movie <- searchTwitter(name, since='2015-06-27',until='2015-06-28', n=10000, lang='en')
	length(movie)
}