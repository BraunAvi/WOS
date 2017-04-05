# Search parameters:
#   (WC=physics) AND LANGUAGE: (English) AND DOCUMENT TYPES: (Article) Indexes=SCI-EXPANDED Timespan=1970
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from time import sleep

# resource: https://automatetheboringstuff.com/chapter11/


def openpageQuery(url='http://google.com', page=1,browser=webdriver.Firefox(firefox_binary=FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'))):
    """
    Open a  given and returns its webdriver handle
    :param url:
    :param page:
    :param browser:
    :return:  browser
    """

    # pageN=page
    url_org=url
    #  a new url url  has to be acquire  for new search
    # url_org=url_org.replace("page=1", "page="+str(pageN),1)
    #open Web of knowledge
    binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    browser = webdriver.Firefox(firefox_binary=binary)
    browser.get(url_org)
    sleep(2)
    print 'loaded Query '
    return browser


def openpagePapers(firstPaper=1,lastPaper=10,browser=webdriver.Firefox(firefox_binary=FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'))):
    """
    'print' to page a batch of papers; usually 500, but can be less for last page
    returns the url of the 5000-papers print
    """
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
    sleep(0.5)
    browser.switch_to.window(browser.window_handles[1])
    sleep(7)
    url_to_scrape = browser.current_url
    # print url_to_scrape
    return url_to_scrape

