#CS513 Final Project
#Shelter Animal Outcome
#Team Member:
#Vijay Sarathy, Hanzhuo Li, Haotian Huang, Wenyi Chen

library(class)
library(MLmetrics)
library(dprep)
library(rpart)
library(plyr)
library(lubridate)
library(gbm)
library(ipred)
library(Matrix)
library(e1071)

#cleaning workspace
rm(list=ls()) 

#inputting training file
file<-read.csv("train.csv",header=TRUE, stringsAsFactors=FALSE)

#inputting test set
test_set<-read.csv("test.csv",header=TRUE, stringsAsFactors=FALSE)

#filling na
file[file==""]<-0

test_set[test_set==""]<-0

#creating dummy variable for name
file$HasName[file$Name!=0]<-1
file$HasName[file$Name==0]<-0

test_set$HasName[test_set$Name!=0]<-1
test_set$HasName[test_set$Name==0]<-0

#convert categorical to numbers
file$OutcomeType<-as.numeric(factor(file$OutcomeType))
file$AnimalType<-as.numeric(factor(file$AnimalType))
file$Breed<-as.numeric(factor(file$Breed))
file$Color<-as.numeric(factor(file$Color))

test_set$AnimalType<-as.numeric(factor(test_set$AnimalType))
test_set$Breed<-as.numeric(factor(test_set$Breed))
test_set$Color<-as.numeric(factor(test_set$Color))

#Time variables
as.POSIXct(file$DateTime)

as.POSIXct(test_set$DateTime)

#decompose time variable
file$month<-month(file$DateTime)
file$year<-year(file$DateTime)
file$week<-week(file$DateTime)
file$minute<-minute(file$DateTime)
file$hour<-hour(file$DateTime)
file$day<-day(file$DateTime)

test_set$month<-month(test_set$DateTime)
test_set$year<-year(test_set$DateTime)
test_set$week<-week(test_set$DateTime)
test_set$minute<-minute(test_set$DateTime)
test_set$hour<-hour(test_set$DateTime)
test_set$day<-day(test_set$DateTime)

#handling AgeUponOutcome
file$AgeuponOutcome[file$AgeuponOutcome %in% c("0","0 years","1 day","1 month", "1 week", "1 weeks", "10 months", "11 months", "2 days", "2 months", "2 weeks", "3 days", "3 months", "3 weeks", "4 days", "4 months", "4 weeks", "5 days", "5 months", "5 weeks", "6 days", "6 months", "7 months", "8 months", "9 months")]<-"Less Than a Year"
file$AgeuponOutcome<-as.numeric(factor(file$AgeuponOutcome))

test_set$AgeuponOutcome[test_set$AgeuponOutcome %in% c("0","0 years","1 day","1 month", "1 week", "1 weeks", "10 months", "11 months", "2 days", "2 months", "2 weeks", "3 days", "3 months", "3 weeks", "4 days", "4 months", "4 weeks", "5 days", "5 months", "5 weeks", "6 days", "6 months", "7 months", "8 months", "9 months")]<-"Less Than a Year"
test_set$AgeuponOutcome<-as.numeric(factor(test_set$AgeuponOutcome))

#creating gender and intactness variables
sexuponoutcome <- as.data.frame(table(file$SexuponOutcome))
colnames(sexuponoutcome) <- c('SexuponOutcome','Freq')

file$Gender[file$SexuponOutcome %in% c("Intact Male","Neutered Male")]<-1
file$Gender[file$SexuponOutcome %in% c("Intact Female", "Spayed Female")]<-2
file$Gender[file$SexuponOutcome %in% c("Unknown",0)]<-0

gender <- as.data.frame(table(file$Gender))
colnames(gender) <- c('Gender','Freq')

file$Intact[file$SexuponOutcome %in% c("Unknown","",0)]<-0
file$Intact[file$SexuponOutcome %in% c("Intact Male","Intact Female")]<-1
file$Intact[file$SexuponOutcome %in% c("Neutered Male", "Spayed Female")]<-2

intact <- as.data.frame(table(file$Intact))
colnames(intact) <- c('Intact','Freq')

test_set$Gender[test_set$SexuponOutcome %in% c("Intact Male","Neutered Male")]<-1
test_set$Gender[test_set$SexuponOutcome %in% c("Intact Female", "Spayed Female")]<-2
test_set$Gender[test_set$SexuponOutcome %in% c("Unknown",0)]<-0

test_set$Intact[test_set$SexuponOutcome %in% c("Unknown","",0)]<-0
test_set$Intact[test_set$SexuponOutcome %in% c("Intact Male","Intact Female")]<-1
test_set$Intact[test_set$SexuponOutcome %in% c("Neutered Male", "Spayed Female")]<-2

#explorebreed <- as.data.frame(table(file$Breed))
#colnames(explorebreed) <- c('Breed', 'Frequency')
#explorecolor <- as.data.frame(table(file$Color))
#colnames(explorecolor) <- c('Color', 'Frequency')
#missingnames <- sum(file$Name =="")

#frequencies
hist(file$Breed,col = blues9,main = "Frequency of Breed",xlab = "Breed")
hist(file$Color,col = blues9,main = "Frequency of Color",xlab = "Color")

hist(test_set$Breed,col = blues9,main = "Frequency of Breed",xlab = "Breed")
hist(test_set$Color,col = blues9,main = "Frequency of Color",xlab = "Color")

#Something wrong with the code here ----  Haotian Huang
#categorizing breed, color
file$BreedCat<-0
file$BreedCat<-file$Breed[file$Breed %in% seq(600,650,1)]<-1

test_set$BreedCat<-0
test_set$BreedCat<-test_set$Breed[test_set$Breed %in% seq(400,450,1)]<-1

file$ColorCat<-0
file$ColorCat<-file$Color[file$Color %in% seq(20,40,1)]<-1
file$ColorCat<-file$Color[file$Color %in% seq(100,120,1)]<-2
file$ColorCat<-file$Color[file$Color %in% seq(0,20,1)]<-3
file$ColorCat<-file$Color[file$Color %in% seq(60,80,1)]<-4
file$ColorCat<-file$Color[file$Color %in% seq(120,140,1)]<-5
file$ColorCat<-file$Color[file$Color %in% seq(80,100,1)]<-6
file$ColorCat<-file$Color[file$Color %in% seq(280,300,1)]<-7
file$ColorCat<-file$Color[file$Color %in% seq(300,320,1)]<-8
file$ColorCat<-file$Color[file$Color %in% seq(320,340,1)]<-9

test_set$ColorCat<-0
test_set$ColorCat<-test_set$Color[test_set$Color %in% seq(20,40,1)]<-1
test_set$ColorCat<-test_set$Color[test_set$Color %in% seq(60,80,1)]<-2
test_set$ColorCat<-test_set$Color[test_set$Color %in% seq(0,20,1)]<-3
test_set$ColorCat<-test_set$Color[test_set$Color %in% seq(80,100,1)]<-4
test_set$ColorCat<-test_set$Color[test_set$Color %in% seq(120,140,1)]<-5
test_set$ColorCat<-test_set$Color[test_set$Color %in% seq(240,260,1)]<-6
test_set$ColorCat<-test_set$Color[test_set$Color %in% seq(160,180,1)]<-7
test_set$ColorCat<-test_set$Color[test_set$Color %in% seq(200,220,1)]<-8
test_set$ColorCat<-test_set$Color[test_set$Color %in% seq(220,240,1)]<-9

hist(file$day)

#selecting OutcomeSubType,AnimalType,SexuponOutcome,AgeuponOutcome
#6: AnimalType, 8: Age, 11:HasName, 16:hour, 18:Gender, 19:Intact
sub<-file[,c(6,8,11,16,18:19)]

#4: AnimalType, 6: Age, 9:HasName, 14:hour, 16:Gender, 17:Intact
sub1<-test_set[,c(4,6,9,14,16:17)]
#normalize subset
sub<-mmnorm(sub)

sub1<-mmnorm(sub1)

#splitting into training and test sets
idx<-sample(nrow(sub),as.integer(.70*nrow(sub))) 
training<-file[idx,] 
test<-file[-idx,] 

#selecting AnimalType,SexuponOutcome,AgeuponOutcome,HasName, hour, BreedCat, ColorCat
features<-c(6,8,11,16,18:19)
features1<-c(4,6,9,14,16:17)

#Naive Bayes
attach(training)
nb<-naiveBayes(OutcomeType ~ AnimalType + AgeuponOutcome + HasName + hour + Gender + Intact,data=training[,c(4,features)])
#Return to Owner: 4; Euthanasia: 3; Adoption: 1; Transfer: 5; Died: 2.
detach(training)

#KNN
pred<-knn(training[,features],test[,features],training[,4],k=1)

pred1<-knn(file[,features],test_set[,features1],file[,4],k=1)

#accuracy score
Accuracy(test[,4],pred)
ConfusionMatrix(test[,4],pred)

write.csv(cbind(test_set,pred1),"solution.csv")