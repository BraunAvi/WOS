from WebPage import WOSResultsPage, WebPage
WOSPage=WOSResultsPage('')
fileName="fullText.txt" # utility text file; saving raw data
WOSPage.collectdata(fileName=fileName) # collect data into data frame
print WOSPage.df.__sizeof__()
print WOSPage.df.head()
print WOSPage.df.tail()
fileNameW='DF.txt'
WOSPage.df.to_csv(fileNameW, sep='\t')
# dffile=open('DF.txt','w')
# dffile.write(WOSPage.df)
# dffile.close()