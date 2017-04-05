# https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#Navigating the Parse Tree

def getValuesfromPrint(url='http://google.com'):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import re
    from time import sleep

    url_to_scrape=url
    print "URL to Scrap:",  url_to_scrape

    try:
        r = requests.get(url_to_scrape)
    except:
        sleep(5)
        r = requests.get(url_to_scrape)

    soup = BeautifulSoup(r.text,"lxml")

    tables = soup.findChildren('table',attrs={'bordercolor': None, 'class': None}) # ignore inner tables of 'funding'
    # print url_to_scrape
    print "tabls:", len(tables)
    tables=tables[2:-2] # clean irrelevant tables
    # print "relevant tables:", len(tables)

    papers_df = pd.DataFrame([])
    count=0 # counter for papers in page

    boldsList = []  # list for collecting 'bold' items (authors)
    for bold_tag in soup.find_all('b', text=re.compile('Author')):
        boldsList.append(bold_tag.next_sibling)
    Authors=([(boldsList[i][1:]) for i in range(0,len(boldsList))])
    print Authors
    print ('No, of Authors=',len(Authors))

    AuthList=[]
    for jj in range(0,len(tables)):
        flagAuthor=0 # set to 1 if authors have been already found (solve 'group authors' conflict
        papers_attr = []
        my_table = tables[jj]
        rows = my_table.findChildren(['tr'])
        for row in rows:
            cellsV = row.findChildren('value')
            cellsB = row.findChildren('b')
            founddata = [0]
            # print cellsB
            if len(cellsB)==1:
                for cell in cellsB:
                    value=cell.string
                    print value
                    if value == 'Author(s):':
                        print 'Found author'
                        # commentSoup = BeautifulSoup(value,'lxml')
                        # comment = commentSoup.find(text=re.compile("nice"))
                        # AuthrsValue='r'
                    else:
                        if (value == 'Group Author(s)') and flagAuthor==0:
                            AuthrsValue = 's'

            if len(cellsB)>2: # build indexes list for available attributes
                founddata = []
                for cell in cellsB:
                    value = cell.string
                    if value=='Source:':
                        founddata.append(0)
                    if value=='Volume:':
                        founddata.append(1)
                    if value=='Issue:':
                        founddata.append(2)
                    if value=='Pages:':
                        founddata.append(3)
                    if value == 'DOI:':
                        founddata.append(4)
                    if 'Publi' in value:
                        founddata.append(5)

            sublist=[]
            for cell in cellsV:
                value = cell.string
                sublist.append(value) # value of attributes found for THIS paper
            # print sublist
            # print len(cellsV) # up tp 6 for journal information ; 1 for all others
            journalInfoList = sublist
            if len(cellsV)>1:
                journalInfoList=['']*6
                try:
                    map(journalInfoList.__setitem__, founddata, sublist)# map the avaliable attributes to the correct position in DB
                except:
                    print founddata
                # print journalInfoList
            [papers_attr.append(i) for i in journalInfoList]
        papers_df[count] = pd.Series(papers_attr[0:10])
        count += 1
    papers_df=papers_df.T
    papers_df.columns=['Title','Journal','Volume','Issue','Pages','DOI','Published','Cited_Web','Cited','Citing']
    print ('Len authors=',len(Authors))
    #
    print len (Authors)
    papers_df['Authors']=Authors
    print len(papers_df['Authors'])
    # print papers_df
    return papers_df


