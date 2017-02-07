class indeedDSParser():
    
    """
    This class is used to collect the location and skills requirement information of Data Science job on indeed
    """
    def __init__(self,n):
        self.info = []
        self.webStart = "http://www.indeed.com/jobs?q=data+science&jt=fulltime&fromage=1&start=0&pp="
        self.skillList = ['r','python','java','c++','ruby','perl','matlab','javascript','scala','excel','tableau',
                'd3.js','sas','d3','spss','hadoop','mapreduce','spark','pig','hive','zookeeper',
                'oozie','mahout','flume','sql','nosql','hbase','cassandra','mongodb']
        self.pageAmount = n
        self.linkSkill = []
    
    
    def text_extractor(self,website):
        '''
        extract words from on job page (html file)
        '''
        try:
            site = ub.urlopen(website).read() 
        except: 
            return  
        
        # Get the html from the site
        soupObj = BeautifulSoup(site,"lxml") 

        for script in soupObj(["script", "style"]):
            script.extract() # Remove these two elements from the BS4 object

        text = soupObj.get_text() # Get the text from this
        
        # break into lines
        lines = (line.strip() for line in text.splitlines()) 
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) 
        text = re.sub("[^a-zA-Z.+3]"," ", text)  
        # Go to lower case and split them apart
        text = text.lower().split()  
        # get distinct word counts
        text = list(set(text)) 
        return text
    
    
    def pageGenerator(self,n):
        """
        return the link of pages that will be used
        """
        links = []
        for i in range(n):
            front = "http://www.indeed.com/jobs?q=data+science&jt=fulltime&fromage=1&start="
            end = "&pp="
            links.append("".join([front,str(i*10),end]))
        return links


    def completeLink(self,link):
        return "http://www.indeed.com" + link

    
    def jobLinkCollector(self,pageAddr):
    
        # load page
        site = ub.urlopen(pageAddr).read()
        soupObj = BeautifulSoup(site,"lxml")

        # find the division for the fixed 10 jobs on one page
        jobs = soupObj.find_all("div",attrs = {"data-tn-component":"organicJob"})
        jobLink = []

        # iteration for get the link of each job site
        for i in range(len(jobs)):
            link = jobs[i].find("a",attrs={"data-tn-element":"jobTitle"}).get("href")
            jobLink.append(self.completeLink(link))

        return jobLink
    
    
    def jobLocCollector(self,pageAddr):
    
        # load page
        site = ub.urlopen(pageAddr).read()
        soupObj = BeautifulSoup(site,"lxml")

        # find the division for the fixed 10 jobs on one page
        jobs = soupObj.find_all("div",attrs = {"data-tn-component":"organicJob"})
        jobLoc = []

        # iteration for get the loc of each job site
        for i in range(len(jobs)):
            loc = jobs[i].find("span",attrs={"itemprop":"addressLocality"}).contents[0]
            loc = ''.join(i for i in loc if not i.isdigit()).strip()
            jobLoc.append(loc)

        return jobLoc
    
    
    def linkSkillInfo(self,n):
        """
        jobInfo contains the links of jobs and their locations. 
        It will be processed further in locSkill
        """
        
        # generate the pages for indeed jobs
        jobPages = self.pageGenerator(n)
        linkSkill= []

        for page in range(len(jobPages)):
            links = self.jobLinkCollector(jobPages[page])
            locs = self.jobLocCollector(jobPages[page])
            info = [(x,y) for x,y in zip(links,locs)]
            self.linkSkill.extend(info)
    
    
    def locSkill(self,textList,skillList):
        """
        This function is used to get skill and loc info
        """ 
        for i in range(len(textList)):
            skillDict = dict((el,0) for el in skillList)
            for j in skillList:
                skillDict[j] += int((np.array(textList[i])==j).sum())
            self.info.append([skillDict,self.linkSkill[i][1]])

    
    def run(self):
        self.linkSkillInfo(self.pageAmount)
        infoList = []

        for item in tqdm(self.linkSkill):
            infoList.append(self.text_extractor(item[0]))
            time.sleep(0.1)
        
        self.locSkill(infoList,self.skillList)
    
    
    def get(self):
        return self.info