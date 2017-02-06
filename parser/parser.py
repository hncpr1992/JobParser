from bs4 import BeautifulSoup # For HTML parsing
import urllib.request as ub
import re # Regular expressions
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
import time 
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

# website parsing functiion
def text_extractor(website):
    '''
    extract words from html file
    ''' 
    # try contacting the website
    try:
        site = ub.urlopen(website).read() 
    except: 
        return "Fail to link"
    
    # build beatifulsoup object
    soupObj = BeautifulSoup(site,"lxml") 
    
    # Remove script and style. We only need body
    for script in soupObj(["script", "style"]):
        script.extract() 
    
    # Extract text
    text = soupObj.get_text() 
    
    # break into lines
    lines = (line.strip() for line in text.splitlines()) 
    
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) 

    # Now get rid of any terms that aren't words (include 3 for d3.js)
    text = re.sub("[^a-zA-Z.+3]"," ", text)  
    
    # Go to lower case and split them apart
    text = text.lower().split()  
    
    # get distinct word counts
    text = list(set(text)) 

    return text

def pageGenerator(n):

"""
return the link of pages that will be connected concerning the search of data science job
"""
links = []
for i in range(n):
    front = "http://www.indeed.com/jobs?q=data+science&jt=fulltime&fromage=1&start="
    end = "&pp="
    links.append("".join([front,str(i*10),end]))
return links

def completeLink(link):
	"""
	create complete link of websites
	"""
    return "http://www.indeed.com" + link

def jobLinkCollector(pageAddr):
	"""
	extract links to the job pages from the html file
	"""
    # load page
    site = ub.urlopen(pageAddr).read()
    soupObj = BeautifulSoup(site,"lxml")
    
    # find the division for the fixed 10 jobs on one page
    jobs = soupObj.find_all("div",attrs = {"data-tn-component":"organicJob"})
    jobLink = []
    
    # iteration for get the link of each job site
    for i in range(len(jobs)):
        link = jobs[i].find("a",attrs={"data-tn-element":"jobTitle"}).get("href")
        jobLink.append(completeLink(link))
    
    return jobLink

def allJobLinks(n):
    """
	# generate the pages for indeed jobs
    """
    jobPages = pageGenerator(n)
    jobLinks = []
    
    for page in range(len(jobPages)):
        jobLinks.extend(jobLinkCollector(jobPages[page]))
    
    return jobLinks    


def skillWordCount(textList,skillList):
    """
    This function is used to count the skills on each webpage
    """
    skillDict = dict((el,0) for el in skillList)
    
    for text in textList:
        for i in skillList:
            skillDict[i] += int((np.array(text)==i).sum())
    
    return skillDict

def jobLocCollector(pageAddr):
    
    """
	Collect job locations from the html
    """
    # load page
    site = ub.urlopen(pageAddr).read()
    soupObj = BeautifulSoup(site,"lxml")
    
    # find the division for the fixed 10 jobs on one page
    jobs = soupObj.find_all("div",attrs = {"data-tn-component":"organicJob"})
    jobLoc = []
    
    # iteration for get the link of each job site
    for i in range(len(jobs)):
        loc = jobs[i].find("span",attrs={"itemprop":"addressLocality"}).contents[0]
        loc = ''.join(i for i in loc if not i.isdigit()).strip()
        jobLoc.append(loc)
    
    return jobLoc

def allJobInfo(n):
    """
	
    """
    # generate the pages for indeed jobs
    jobPages = pageGenerator(n)
    
    jobInfo= []
    
    for page in range(len(jobPages)):
        links = jobLinkCollector(jobPages[page])
        locs = jobLocCollector(jobPages[page])
        info = [(x,y) for x,y in zip(links,locs)]
        jobInfo.extend(info)
    
    return jobInfo

def locSkill(textList,skillList):
    """
    This function is used to get skill and loc info
    """ 
    
    res = []
    for i in range(len(textList)):
        skillDict = dict((el,0) for el in skillList)
        for j in skillList:
            skillDict[j] += int((np.array(textList[i])==j).sum())
        res.append([skillDict,allInfo[i][1]])
        
    
    return res


# skill set
skillList = ['r','python','java','c++','ruby','perl','matlab','javascript','scala','excel','tableau',
                'd3.js','sas','d3','spss','hadoop','mapreduce','spark','pig','hive','zookeeper',
                'oozie','mahout','flume','sql','nosql','hbase','cassandra','mongodb']


# Test
allInfo = allJobInfo(2)
infoList = []

for item in tqdm(allInfo):
    infoList.append(text_extractor(item[0]))
    time.sleep(0.5)

finalInfo = locSkill(infoList,skillList)

# The finalInfo contains the location and skill requirements of each job








