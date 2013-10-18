#this is what parses the HTML code and does some awesome stuff with it.
from BeautifulSoup import BeautifulSoup
#We want this to time our requests irregularly, so that we don't overwhelm a server or get kicked.
import time, random

#The url-getting library used in this example. 
import requests

#Another python lib for getting urls, but not very persistent. Will likely fail if server/connection finnicky.
import urllib

#re for regular expressions, not used in this scraper.
#htmlentitydefs used with urllib, but not neccessary with requests. I think.
import re, htmlentitydefs

#read/write our csvs
import csv, codecs, cStringIO


#initialize the csv we'll be writing to. Careful, will rewrite file in your current directory.
outfile = open('purchases2.csv', 'w')

#writer writes to the csv!
writer = csv.writer(outfile)

#write our header row
writer.writerow(['fundingyear',
'rowkey',
'rowname',
'four71',
'FRN',
'SPIN',
'service_provider',
'service',
'orig_requested_amt',
'funded',
'disbursed',
'util_percent',
'discount'])

#get the table with all the keys
reftable = open('azschool-billingentity.csv')
#handle reads the csv sequentially, line by line
handle = csv.reader(reftable)
#skip the header row in the reference
handle.next()

#We're fortunate that we only need to pass one parameter (key)
#this is the urlroot of each of the pages that we want, without the key parameter.
urlroot = 'http://www.e-ratecentral.com/us/reports/fundingHistoryDetail_ben.asp?v=&typ=entNum&ste=AZ&fy=all&desc=1&ky='

#for each row in our reference csv....
for h in handle:
    #key is in the first column ([0])
    key = h[0]
    #Name of the school. There's a leading space in the csv, so .strip() gets rid of that.
    name = h[1].strip()
    #So I can see how far in terminal we are.
    print name

    #get our url. "+" concatenates the pair of these. 
    url = urlroot + key
    # requests gets the page...
    r = requests.get(url)
    #... rendered as raw HTML text ...
    response = r.text
    #... which BeautifulSoup digests.
    soup = BeautifulSoup(response)  

    #for each item on the page with the tag 'tr'...
    for row in soup('tr'):
        #this runs sequentially down the page. Since year is declared above each table, we need to set some variable to the current year.
        #here's the exact tag for all of those. Fortunately it's unique. Pull it, see if the row only has one of those tags. If that's the case, there's your year! 
        if len(row('td', attrs= {"class":"rptData", "colspan":"12", "bgcolor":"#eeeeee"})) == 1:
            #returns a list. contents[0] returns the first item in that list.
            yearlist = row.find('td', attrs= {"class":"rptData", "colspan":"12", "bgcolor":"#eeeeee"}).contents[0]
            #This is messy html with tags, so .renderContents() returns the contents of the tag.
            year = yearlist.renderContents()
        #so if it's not a year row, we want the table data.
        else:
            #each data row has 12 'td' items
            if len(row('td')) == 12:
                #create a list of those items.
                cells = row('td')

                #get our School and year rows.
                fundingyear = year
                rowkey = key
                rowname = name

                #get row data. Easy peasy.
                four71 = cells[1].string
                #except for this. It's a hyperlinked item so womp womp. Not the cleanest method.
                FRN = cells[2].contents[0].renderContents()
                SPIN = cells[3].string
                service_provider = cells[4].string
                service = cells[5].string
                orig_requested_amt = cells[6].string
                funded = cells[7].string
                disbursed = cells[9].string
                util_percent = cells[10].string
                discount = cells[11].string

                #now write a row to our csv with all those variables.
                writer.writerow([ fundingyear,
                                rowkey,
                                rowname,
                                four71,
                                FRN,
                                SPIN,
                                service_provider,
                                service,
                                orig_requested_amt,
                                funded,
                                disbursed,
                                util_percent,
                                discount ])

    #before you go back to the beginning of the loop, wait a sec. Or a few.
    #random.random() returns a random-ish value between 0 and 1
    #time.sleep waits for the # of seconds inside. Adjust the "[value] *" to wait for more/less time.
    #reminder: at [value=4] this will wait for an average of 2 seconds. 3500 urls to get. 7000 seconds, nearly two hours of waiting alone. Vast majority of the scrape time.

    time.sleep(4 * random.random())