from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.keys import Keys
from time import sleep, time
import math as m


class WebPage(object):
    """ Thie class represent WebPage objects

    Attributes:
        url: url of WebPage instance
        browser: the browser handle (if using Selenium for browsing)
        fulltext: the full text ead by BS
    Methods:
        Openurl: open the current url
        urlreadBS: read the text of the url using BS

    """
    def __init__(self, url='http://google.com', browser=''):
        self.url = url
        self.browser = browser
        self.fulltext = []

    def open_url(self):
        """
        Open a WebPage using Selenium library given and returns its webdriver handle
        return:  browser
        """
        binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
        self.browser = webdriver.Firefox(firefox_binary=binary)
        self.browser.get(self.url)
        # print 'loaded Selenium page:', self.url
        # return self.browser

    def read_url_BS4(self,url=''):
        """
        Open a WebPage using BS4 library given and returns its webdriver handle
        # return:  self.fulltext (full text from url(
        """
        fulltext=''
        try: r = requests.get(url)
        except:
            print "couldn't find URL:", url

        soup = BeautifulSoup(r.text,"lxml")
        for string in soup.stripped_strings:
            # fulltext+=repr(string)
            fulltext+=(string+'\n')
        self.fulltext=fulltext
        print 'loaded BS page:', url
        return self.fulltext


class WOSResultsPage(WebPage):
    """
    This is a WebPage class used specificly for the WOS results webpage
    The 'PrintPapers' method 'prints' (navigates to) the  papers page and return the url of te 500Papers web-page
    """
    def __init__(self, url='http://google.com', browser=''):
        self.url = url
        self.browser = browser
        self.fulltext = []
        self.url2scrape = ''
        self.df = []

    def PrintX50Papers(self, firstPaper=1, lastPaper=500):
        """
        'print' to page a batch of papers; usually 500, but can be less for last page
        returns the url of the 5000-papers print
        """
        s_time=time()
        browser=self.browser
        old_url =  self.browser.current_url
        # open print form and print to screen
        elem = browser.find_element_by_name('formatForPrint')  # Find the search box
        elem.send_keys('' + Keys.RETURN)
        elem = browser.find_element_by_name('fields_selection')  # Find the search box
        elem.send_keys('f' + Keys.RETURN)
        elem = browser.find_element_by_id('markFrom')  # Find the search box
        elem.click()
        elem.send_keys(firstPaper)
        elem = browser.find_element_by_id('markTo')  # Find the search box
        elem.click()
        elem.send_keys(lastPaper)
        elem.send_keys(Keys.ENTER)
        while self.url2scrape ==old_url:
            sleep(0.5)
            self.url2scrape = self.browser.current_url
        print 'waited for url',time()-s_time ,'sec'
        browser.switch_to.window(browser.window_handles[1]) #handle 1 is the 50 papers results
        sleep(7)
        self.url2scrape = browser.current_url
        # print 'url_to_scrape:',self.url2scrape
        return self.url2scrape

    def GoTo50Papers(self, firstPaper=1, lastPaper=500,pageNumber=1):
        """
        'naviagte' to a 50=papers web=page returns the url of the 5000-papers print
        """
        old_url=self.url2scrape
        elem = self.browser.find_element_by_link_text(str(pageNumber)) # move to next 50
        elem.click()
        # print 'switching to:', 'page', ' ' , pageNumber, 'x 50s'
        self.url2scrape = self.browser.current_url
        s_time=time()
        while self.url2scrape ==old_url:
            sleep(0.5)
            self.url2scrape = self.browser.current_url
        print 'waited for url',time()-s_time ,'sec'
        return self.url2scrape



    def parse_data(self,fileName):
        """
        This function collect the data from the 'fooltext' variable and organize it in a df array
        :return: df # dataframe with the collected data
        """
        import pandas as pd
        attributes = ['Saving records','Title:', 'Author(s):', 'Source:', 'Volume:', 'Issue:', 'Pages:', 'Published:',
                      'Times Cited in Web of Science Core Collection:', 'Cited Reference Count:', 'Accession Number:']
        df = pd.DataFrame(columns=attributes)
        counter = 0
        flag=0

        f=open(fileName,'r')
        # f=fileName
        for line in f:
            # print line
            for s in attributes:  # check if 'save flag' is 1; if 1 -> save the data at the relevant column
                if flag == s:
                    df.set_value(counter, flag, line[0:-1])
            flag = line[0:-1] if (line in s for s in attributes) else flag  # check if line is a relevant attribute.
            if flag == 'Title:':
                counter += 1  # increment paper counter
        # rename columns:
        attributes_nl = [s[0:-1] for s in attributes]
        df.columns = attributes_nl
        df = df.rename(columns={'Times Cited in Web of Science Core Collection': 'Times Cited'})
        self.df = df
        return self.df

def collect_data_from_print(WOSPage,text_file_h,firstPaper=1,lastPaper=500):
    """
    The 'collect_data_from_print function' saves the raw text of the papers
    :param firstPaper: number of first paper
    :param lastPaper: number of last paper.
    :return: ()
    """
    # print 'first paper number is: ', firstPaper
    # print 'last paper number is: ', lastPaper

    no_of_50X_pages=int(m.ceil((lastPaper-firstPaper+1)/50.)) # high range of number of pages
    print 'no_of_50X_pages=',no_of_50X_pages
    WOSPage.PrintX50Papers(firstPaper=firstPaper,lastPaper=lastPaper) # print X papers; and return the URL of the new page
    for i in range (2,no_of_50X_pages+1): #start at 2 since the first page is already loaded
        print i-1,
        WOSPage.read_url_BS4(WOSPage.url2scrape) # print the text fo the 50-papers webpage; return self.fulltext
        sleep(1)
        text_file_h.write('Saving records\n' + str(int(firstPaper + (i - 2) * 50)) + '\n')
        text_file_h.write(WOSPage.fulltext.encode('utf-8')) # extract the data and save to file
        WOSPage.GoTo50Papers(pageNumber=i) # go to page i with 50 papers in it
    WOSPage.read_url_BS4(WOSPage.url2scrape)  # print the text fo the 50-papers webpage; return self.fulltext
    sleep(1)
    try:text_file_h.write('Saving records\n' + str(int(firstPaper + (i - 1) * 50)) + '\n')
    # fails for last partial page with less than 50 entries
    # TODO: fix that
    except: pass
    text_file_h.write(WOSPage.fulltext.encode('utf-8'))  # extract the data and save to file

