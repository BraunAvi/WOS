from openWebPage_i import openpageQuery, openpagePapers
from BS_Quesry_V2 import getValuesfromPrint
from time import sleep
import pandas as pd
import time
import math


#######  Initialize data scraping:    ##########
url='https://apps.webofknowledge.com/summary.do?product=WOS&doc=1&qid=1&SID=Q2O3LWWGZpqKLmLqHEw&search_mode=AdvancedSearch&update_back2search_link_param=yes'

total_N_Papers=30799 # manually taken from query
first500page=1

print 'total_N_Papers is', total_N_Papers
total_N_Pages=total_N_Papers/500 # maximum 500 papers can be printed in one go
print 'total_Number of Pages WITH 500 papers is',total_N_Pages
PapersInLastPage=total_N_Papers-total_N_Pages*500
print 'number of papers in last page is:', PapersInLastPage
start = time.time()

browser=openpageQuery(url=url) # open the WOS search URL; return the 'webdriver' handle
print(time.time() - start)

db=pd.DataFrame([])
# We can 'print' the results in batched of 500, and view them in pages of 50 resutls.
#
for p in range(first500page,total_N_Pages+2): # collecting data from all pages500 , but not from the last one
    print p, 'x 500'
    firstPaper=(1+(p-1)*500)
    print 'first paper number is: ', firstPaper
    lastPaper=(500+(p-1)*500)
    if p == total_N_Pages + 1:
        lastPaper = PapersInLastPage + (p - 1) * 500
    print 'last paper number is: ', lastPaper
    browser.switch_to.window(browser.window_handles[0])  # move to next 50

    url_to_scrape = openpagePapers(browser=browser, firstPaper=firstPaper, lastPaper=lastPaper) # \
    #  'prints' a summary of 500 papers; returns the url of the print page

    if len(url_to_scrape[:])<20: # unsuccessful reading of url
        print 'collecting url again'
        sleep(5)
        url_to_scrape = openpagePapers(browser=browser, firstPaper=firstPaper, lastPaper=lastPaper) # open 500 papers

    total_N50_Pages=int(math.ceil((lastPaper-firstPaper)/50)+1)# number of 50papers pages in the 500papers page
    for i in range(2,total_N50_Pages+1):
        papers_df=getValuesfromPrint(url_to_scrape) # get data from 50 papers
        db = db.append(papers_df)
        elem = browser.find_element_by_link_text(str(i)) # move to next 50
        elem.click()
        print 'switching to:', p, ' ' , i, 'x 50s'
        sleep(5)
        browser.switch_to.window(browser.window_handles[1]) # move to next 50
        url_to_scrape = browser.current_url
    papers_df=getValuesfromPrint(url_to_scrape) # save to DB the last 5- papers
    db = db.append(papers_df)
    # print 'db:', db
    db.to_csv('db.csv')
    browser.close()
    # print papers_df
print 'loaded all', str(total_N_Papers)
print(time.time() - start)


