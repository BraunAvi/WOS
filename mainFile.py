from WebPage import *
import math as m
import time
import os


txtfileName = "fullText1977.txt"  # utility text file; saving raw data
text_file_h = open(txtfileName, "w+")
N = 500 # number of papers in batch (500 for run; 50, or ,ore for testting )

urlWOS = 'https://apps.webofknowledge.com/summary.do?product=WOS&doc=1&qid=2&SID=S2WJUa48YiBqAW1tipW&search_mode=AdvancedSearch&update_back2search_link_param=yes'

total_N_Papers = 30043
# manually taken from query
print 'total_N_Papers is', total_N_Papers
total_N_Pages = int(m.ceil(total_N_Papers / (N)))  # maximum 500 papers can be printed in one go
print 'total_Number of Pages WITH' , N, 'papers is', total_N_Pages
PapersInLastPage = total_N_Papers - total_N_Pages * N
print 'number of papers in last page is:', PapersInLastPage
start = time.time()

WOSPage = WOSResultsPage(urlWOS)  # initiate WOS page class on the search url
WOSPage.open_url()  # open the url of the main-results file

for p in range(1, total_N_Pages + 1):  # collecting data from all pages500 , but not from the last one
    print p, 'x ', N
    firstPaper = (1 + (p - 1) * N)
    print 'first paper number is: ', firstPaper
    lastPaper = (N + (p - 1) * N)
    if p == total_N_Pages + 1:
        lastPaper = PapersInLastPage + (p - 1) * N
    print 'last paper number is: ', lastPaper
    collect_data_from_print(WOSPage, text_file_h, firstPaper,
                            lastPaper=firstPaper + N - 1)  # collect 500 papers to txt file
    WOSPage.browser.switch_to.window(WOSPage.browser.window_handles[0])  # move back to main search window
    if p==(total_N_Pages) and  PapersInLastPage>0:
        print 'another', PapersInLastPage, "and we're done..."
        collect_data_from_print(WOSPage, text_file_h, firstPaper=firstPaper+N,
                                lastPaper=firstPaper + N + PapersInLastPage - 1)  # collect 500 papers to txt file
os.chdir('C:\\Users\\abraun\\Box Sync\\Projects\\SciPapers\\WOS_Scraping')
time.sleep(20)
# time.sleep(4) # allowing time for writing
WOSPage.parse_data(fileName=txtfileName)  # collect data into data frame
time.sleep(10)
WOSPage.df.to_csv('parsed1977.txt')
time.sleep(10)
text_file_h.close()

print (time.time() - start)

# --------------------- 1978 ---------------------------*
txtfileName = "fullText1978.txt"  # utility text file; saving raw data
text_file_h = open(txtfileName, "w+")
N = 500 # number of papers in batch (500 for run; 50, or ,ore for testting )

urlWOS ='https://apps.webofknowledge.com/summary.do?product=WOS&doc=1&qid=125&SID=S2WJUa48YiBqAW1tipW&search_mode=AdvancedSearch&update_back2search_link_param=yes'
total_N_Papers = 30798
# manually taken from query
print 'total_N_Papers is', total_N_Papers
total_N_Pages = int(m.ceil(total_N_Papers / (N)))  # maximum 500 papers can be printed in one go
print 'total_Number of Pages WITH' , N, 'papers is', total_N_Pages
PapersInLastPage = total_N_Papers - total_N_Pages * N
print 'number of papers in last page is:', PapersInLastPage
start = time.time()

WOSPage = WOSResultsPage(urlWOS)  # initiate WOS page class on the search url
WOSPage.open_url()  # open the url of the main-results file

for p in range(1, total_N_Pages + 1):  # collecting data from all pages500 , but not from the last one
    print p, 'x ', N
    firstPaper = (1 + (p - 1) * N)
    print 'first paper number is: ', firstPaper
    lastPaper = (N + (p - 1) * N)
    if p == total_N_Pages + 1:
        lastPaper = PapersInLastPage + (p - 1) * N
    print 'last paper number is: ', lastPaper
    collect_data_from_print(WOSPage, text_file_h, firstPaper,
                            lastPaper=firstPaper + N - 1)  # collect 500 papers to txt file
    WOSPage.browser.switch_to.window(WOSPage.browser.window_handles[0])  # move back to main search window
    if p==(total_N_Pages) and  PapersInLastPage>0:
        print 'another', PapersInLastPage, "and we're done..."
        collect_data_from_print(WOSPage, text_file_h, firstPaper=firstPaper+N,
                                lastPaper=firstPaper +N+ PapersInLastPage - 1)  # collect 500 papers to txt file
os.chdir('C:\\Users\\abraun\\Box Sync\\Projects\\SciPapers\\WOS_Scraping')
time.sleep(20)
# time.sleep(4) # allowing time for writing
WOSPage.parse_data(fileName=txtfileName)  # collect data into data frame
time.sleep(10)
WOSPage.df.to_csv('parsed1978.txt')
time.sleep(10)
text_file_h.close()

