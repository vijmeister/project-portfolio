"""
The script scrapes data from https://www.yahoo.com/news/politics
"""

import sys, bs4, urlparse, re, os, time,json
from selenium import webdriver
from openpyxl import Workbook
from openpyxl.compat import range

 #extract the link article title and comment number in a given html page
def parsePage(html,page,url):
 #write the results
     if i==0: #first 
         ws.title = "articles"
         ws.append(["Title","Number of Comments","Shares","Articles"])
     subTree = bs4.BeautifulSoup(html)
     topicChunk = subTree.find('h1',{'class':'headline__title'})
     topic=""
     driver = webdriver.Chrome('./chromedriver')
     url1 = 'http://graph.facebook.com/'
     url1 = ''.join([url1,url])
     driver.get(url1)
     #print driver.page_source
     commentTree = bs4.BeautifulSoup(driver.page_source,"lxml")
     driver.close()
     commentPart = commentTree.find('pre')
     comment = ""
     share=""
     if commentPart!= None:
         commentJsonStr = ''.join(commentPart.text)
         print commentJsonStr
         commentJson = json.loads(commentJsonStr)
         if 'comments' in commentJson:
             comment= commentJson['comments']
         if 'shares' in commentJsonStr:
             share = commentJson['shares']
     
     contentChunk = subTree.findAll('p')
     contentQuoteChunk = subTree.findAll('span',{'class':'quote'})
     content=""
     if contentChunk == None:
         print "no content"
     else:
         for a_content in contentChunk:
             content += a_content.text
         for a_content in contentQuoteChunk:
             content += a_content.text
         content = content.encode('utf-8').strip()
     if topicChunk == None:
         print "no topic"
     else:
         topic = topicChunk.text
         topic = topic.encode('utf-8').strip()
     ws.append([topic,comment,share,content])

 
     #wait for 2 seconds
     time.sleep(2)

numberOfPages = 10
if not os.path.exists('data'):
         os.makedirs('data')
    #workbook for excel 
wb = Workbook()
ws = wb.active
       
for num in range(1,11):        
    driver = webdriver.Chrome('./chromedriver')
    driver.get('http://www.huffingtonpost.com/news/elections-2016/'+str(num)+'/')
    tree = bs4.BeautifulSoup(driver.page_source,"lxml")
    driver.quit()
    #select class with link from tree
    articleSectiontree = tree.find('div', {'id':'center_entries'}) #find all articles in the center
    articles = articleSectiontree.findAll('h3',{'class':'seo_bnp'})
    numberOfLinks = len(articles)
    
    for i in range(numberOfLinks):
         #main url of the article
         url = articles[i].find('a').get('href')
    #     print url
         #open the browser and visit the url
         driver = webdriver.Chrome('./chromedriver')
         try:
             driver.get(url)
         except:
             error_type, error_obj, error_info = sys.exc_info()
             print 'STOPPING - COULD NOT FIND THE LINK ', url
             print error_type, 'Line:', error_info.tb_lineno
             continue
     
         #sleep for 5 seconds
         time.sleep(5)
          
         parsePage(driver.page_source,i,url)
         print 'article-link ',i,' done'
         time.sleep(10)
         driver.quit();
wb.save('data/politics.xlsx')



    


    


    