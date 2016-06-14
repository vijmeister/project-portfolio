"""
The script scrapes data from https://www.yahoo.com/news/politics
"""

import sys, bs4, urlparse, re, os, time, json
from selenium import webdriver
from openpyxl import Workbook
from openpyxl.compat import range

driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.yahoo.com/news/politics')
#range 50 to fetch upto 200 articles
for i in range(50):
    driver.execute_script("window.scrollTo(0, 100000)") #scroll to end of page
    time.sleep(4)
#page with approx 200 article links to tree using beautiful soup
tree = bs4.BeautifulSoup(driver.page_source,"lxml")
driver.quit()


mainLink = 'https://www.yahoo.com/news/politics'
#select class with link from tree
articleChunks = tree.select('.js-stream-content.Bdc($c-divider-strong)!:h.js-stream-content:h+Bdc($c-divider-strong)!.Pos(r)')
numberOfLinks = len(articleChunks) #total number of links
print numberOfLinks
if not os.path.exists('data'):
     os.makedirs('data')
#workbook for excel 
wb = Workbook()
ws = wb.active
    
for i in range(numberOfLinks):
     #main url of the article
     subLink = articleChunks[i].find('a').get('href')
     url = urlparse.urljoin(mainLink, subLink)
     print url
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
     
     #extract the link article title and comment number in a given html page
     def parsePage(html,page,url):
     #write the results
         if i==0: #first 
             ws.title = "articles"
             ws.append(["Title","Number of Comments","Shares","Articles"])
         subTree = bs4.BeautifulSoup(html,"lxml")
         topicChunk = subTree.find('header',{'class':'canvas-header'})
         topic=""
         contentChunk = subTree.findAll('p',attrs={'class' : 'canvas-text'})
         content=""
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

         if contentChunk == None:
             print "no content"
         else:
             for a_content in contentChunk:
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
 
     parsePage(driver.page_source,i,url)
     print 'article-link ',i,' done'
     time.sleep(10)
     driver.quit();
wb.save('data/politics.xlsx')



    


    


    