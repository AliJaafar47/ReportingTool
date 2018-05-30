from elasticsearch import Elasticsearch
import time
from datetime import datetime


# version format

def format_version(version):
    try : 
        if (version[0]== 'v' or version[0]== 'V'):
            version = version[1:]
        
        ch = version.split("#")

        if len(ch) == 1 or len(ch) > 2 :
            return version
    
        line1 = ch[0].replace(',', '.')
        line2 = line1.replace(':', '.')
        line3 = line2.replace(';', '.')
        result = ""
        j=0
        for i in line3.split("."):
            if j+1 == len(line3.split(".")):
                result = result+str(i).zfill(2)  
            else :
                result = result+str(i).zfill(2)+"."
            j=j+1
        result=result+"#"+ str(ch[1]).zfill(2)
        return result
    except : 
        return version 



def getProjectNameFromId(id):
    es = Elasticsearch()
    res = es.search(index="nodes_hierarchy", doc_type="nodes_hierarchy",size=1, from_=0, body={"query": {"bool": {"must":[{ "match": { "id": id}}]}}})
    for doc in res['hits']['hits']:
        return(doc['_source']['name'])
def getIDNameFromProjectName(name):
    es = Elasticsearch()
    res = es.search(index="nodes_hierarchy", doc_type="nodes_hierarchy",size=1, from_=0, body={"query": {"bool": {"must":[{ "match": { "name": name}}]}}})
    for doc in res['hits']['hits']:
        return(doc['_source']['id'])


def getprojectsHGW():
    es = Elasticsearch()
    project_list = []
    res = es.search(index="nodes_hierarchy", doc_type="nodes_hierarchy",size=100, from_=0, body={"query": {"bool": {"must":[{ "match": { "node_type_id": "1"}}]}}})
    for doc in res['hits']['hits']:
        #print(doc['_source']['id'])
        if "HGW" in doc['_source']['name']:
            res1 = es.search(index="testprojects", doc_type="testprojects",size=100, from_=0, body={"query": {"bool": {"must":[{ "match": { "id": doc['_source']['id']}}]}}})
            for doc1 in res1['hits']['hits']:
            #print(doc1['_source']['active'])
                if doc1['_source']['active'] == 1 and doc1['_source']['is_public'] == 1:
                    oneProject=Project_Names(doc['_source']['name'],doc['_source']['id'])
                    project_list.append(oneProject)
    project_list.sort(key=lambda Project_Names: Project_Names.name)
    return project_list

def getprojectsSTB():
    es = Elasticsearch()
    project_list = []
    res = es.search(index="nodes_hierarchy", doc_type="nodes_hierarchy",size=100, from_=0, body={"query": {"bool": {"must":[{ "match": { "node_type_id": "1"}}]}}})
    for doc in res['hits']['hits']:
        #print(doc['_source']['id'])
        if "STB" in doc['_source']['name']:
            res1 = es.search(index="testprojects", doc_type="testprojects",size=100, from_=0, body={"query": {"bool": {"must":[{ "match": { "id": doc['_source']['id']}}]}}})
            for doc1 in res1['hits']['hits']:
            #print(doc1['_source']['active'])
                if doc1['_source']['active'] == 1 and doc1['_source']['is_public'] == 1:
                    oneProject=Project_Names(doc['_source']['name'],doc['_source']['id'])
                    project_list.append(oneProject)
    project_list.sort(key=lambda Project_Names: Project_Names.name)
    return project_list
                
class Project_Names():
    def __init__(self,name,id):
        self.name=name
        self.id=id
    
class TestPlan ():
    def __init__(self,testPlanName,testPlanId):
        self.es = Elasticsearch()
        if "SAH - " in testPlanName : 
            self.testPlanName = testPlanName
        else : 
            self.testPlanName ="SAH - " + testPlanName
        self.testPlanID = testPlanId
        self.setPlatforms()
        self.setBuilds()
        self.setTestCases()
        
        
    def setPlatforms(self):
        platformsList=[]
        res = self.es.search(index="testplan_platforms", doc_type="testplan_platforms",size=20, from_=0, body={"query": {"bool": {"must":[{"match": { "testplan_id": self.testPlanID }}]}}})
        for doc in res['hits']['hits']:
            id = doc['_source']['platform_id']
            res = self.es.search(index="platforms", doc_type="platforms",size=20, from_=0, body={"query": {"bool": {"must":[{ "match": { "id": id }}]}}})
            for doc in res['hits']['hits']:
                name = doc['_source']['name']
            onePlateforme = Platform (name,id,self.testPlanID)
            platformsList.append(onePlateforme)
        self.platforms = platformsList
        
    def setBuilds(self):
        buildsList = []
        res = self.es.search(index="builds", doc_type="builds",size=100, from_=0, body={"query": {"bool": {"must":[{"match": { "testplan_id": self.testPlanID }}]}}})
        for doc in res['hits']['hits']:
            oneBuild = Build(doc['_source']['name'],doc['_source']['id'])
            buildsList.append(oneBuild)
        self.builds = buildsList
        
    def setTestCases (self):
        testcasesList=[]
        for i in self.builds :
            for j in self.platforms :
                globalSearch = self.es.search(index="executions", doc_type="executions",size=10000, from_=0, body={"query": {"bool": {"must":[{ "match": { "testplan_id": self.testPlanID }} ,{ "match": { "platform_id": j.platformId }},{ "match": { "build_id": i.buildId }}]}},"filter": {"range" : { "execution_ts" : {"from": start_day,"to": end_day,"time_zone": "+01:00"}}}})
                ### continue if number of execution 0 
                #print(globalSearch)
                if(len(globalSearch['hits']['hits'])==0):
                    continue

                
                    
                oneTest = TestcasesStatus(globalSearch,j.platformId,self.testPlanID,i.buildId,self.testPlanName,j.platformName,i.buildName)
                testcasesList.append(oneTest)   
        self.testCases=testcasesList
        
    
class Platform():
    def __init__(self,platformName,platformId,testPlanId):   
        self.platformName=platformName
        self.platformId = platformId
        self.testPlanId=testPlanId
        
class TestcasesStatus ():
    def __init__(self,globalSearch ,platformID,testPlanId,buildID,testPlanName,plateformName,buildName):
        self.testPlanName = testPlanName
        self.plateformName =plateformName
        self.buildName = buildName
        self.version_used=[]
        self.date=""
        
        self.platformID=platformID
        self.testPlanId=testPlanId
        self.buildID=buildID
        self.globalSearch=globalSearch
        self.es = Elasticsearch()
        
        
        self.numberOfTotalAssigned=0
        self.numberOfTotalFailed=0
        self.numberOfTotalPassed=0
        self.numberOfTotalNotExecuted=0
        self.numberOfTotalBlocked=0
        
        self.state=""
        self.previewState=""
        
        self.numberOfAssignedAutomatedTests=0
        self.numberOfFailedAutomatedTests=0
        self.numberOfBlockedAutomatedTests=0
        self.numberOfPassedAutomatedTests=0
        self.numberOfAutomatedNotExecuted=0
        
        self.numberOfAssignedManualTests=0
        self.numberOfFailedManualTests=0
        self.numberOfPassedManualTests=0
        self.numberOfManualNotExecuted=0
        self.numberOfBlockedManualTests=0
        
        self.numberofbugsUpToDate=0
        self.numberofbugs=0
        
        self.numberOfCriticalBugs=0
        self.numberOfMajorBugs=0
        self.numberOfMediumBugs=0
        self.numberOfMinorBugs=0
        
        self.numberOfCriticalBugsUpToDate=0
        self.numberOfMajorBugsUpToDate=0
        self.numberOfMediumBugsUpToDate=0
        self.numberOfMinorBugsUpToDate=0
        
        self.numberOfTotalFailed_pr=""
        self.numberOfTotalPassed_pr=""
        self.numberOfTotalNotExecuted_pr=""
        self.numberOfTotalBlocked_pr=""
        
        self.numberOfFailedAutomatedTests_pr=""
        self.numberOfBlockedAutomatedTests_pr=""
        self.numberOfPassedAutomatedTests_pr=""
        self.numberOfAutomatedNotExecuted_pr=""
        
        self.numberOfFailedManualTests_pr=""
        self.numberOfPassedManualTests_pr=""
        self.numberOfManualNotExecuted_pr=""
        self.numberOfBlockedManualTests_pr=""
        
        self.bugs = []
        ## setting Assigned tests (automated and manual)
        self.setAssignedTests()
        ## setting of passed not executed and failed tests (automated and manual)
        self.setOtherStatus()
        self.setbugsSettings()
        self.setPreviewState()
        self.setState()
        
        if self.numberOfTotalAssigned == 0 :
            self.numberOfTotalFailed_pr=str(0)+"%"
            self.numberOfTotalPassed_pr=str(0)+"%"
            self.numberOfTotalNotExecuted_pr=str(0)+"%"
            self.numberOfTotalBlocked_pr=str(0)+"%"
        else : 
            self.numberOfTotalFailed_pr=str(round((self.numberOfTotalFailed/self.numberOfTotalAssigned)*100))+"%"
            self.numberOfTotalPassed_pr=str(round((self.numberOfTotalPassed/self.numberOfTotalAssigned)*100))+"%"
            self.numberOfTotalNotExecuted_pr=str(round((self.numberOfTotalNotExecuted/self.numberOfTotalAssigned)*100))+"%"
            self.numberOfTotalBlocked_pr=str(round((self.numberOfTotalBlocked/self.numberOfTotalAssigned)*100))+"%"
        if self.numberOfAssignedAutomatedTests == 0 :
            self.numberOfFailedAutomatedTests_pr=str(0)+"%"
            self.numberOfBlockedAutomatedTests_pr=str(0)+"%"
            self.numberOfPassedAutomatedTests_pr=str(0)+"%"
            self.numberOfAutomatedNotExecuted_pr=str(0)+"%"
        else :  
            self.numberOfFailedAutomatedTests_pr=str(round((self.numberOfFailedAutomatedTests/self.numberOfAssignedAutomatedTests)*100))+"%"
            self.numberOfBlockedAutomatedTests_pr=str(round((self.numberOfBlockedAutomatedTests/self.numberOfAssignedAutomatedTests)*100))+"%"
            self.numberOfPassedAutomatedTests_pr=str(round((self.numberOfPassedAutomatedTests/self.numberOfAssignedAutomatedTests)*100))+"%"
            self.numberOfAutomatedNotExecuted_pr=str(round((self.numberOfAutomatedNotExecuted/self.numberOfAssignedAutomatedTests)*100))+"%"
        if self.numberOfAssignedManualTests == 0 :
            self.numberOfFailedManualTests_pr=str(0)+"%"
            self.numberOfPassedManualTests_pr=str(0)+"%"
            self.numberOfManualNotExecuted_pr=str(0)+"%"
            self.numberOfBlockedManualTests_pr=str(0)+"%"
        else :
            self.numberOfFailedManualTests_pr=str(round((self.numberOfFailedManualTests/self.numberOfAssignedManualTests)*100))+"%"
            self.numberOfPassedManualTests_pr=str(round((self.numberOfPassedManualTests/self.numberOfAssignedManualTests)*100))+"%"
            self.numberOfManualNotExecuted_pr=str(round((self.numberOfManualNotExecuted/self.numberOfAssignedManualTests)*100))+"%"
            self.numberOfBlockedManualTests_pr=str(round((self.numberOfBlockedManualTests/self.numberOfAssignedManualTests)*100))+"%"
        
    def setPreviewState(self):
        
        bb=(self.numberOfTotalPassed+self.numberOfTotalFailed-self.numberOfTotalBlocked)*0.01
        bx = round(self.numberOfTotalPassed + self.numberOfTotalFailed-self.numberOfTotalBlocked)*0.05
        
        
        bc = 2 if (bx<=2) else bx
        
        a=0 if (self.numberOfCriticalBugsUpToDate <=0) else 1 

        b=0 if (self.numberOfMajorBugsUpToDate <=bb) else 1

        c=0 if (self.numberOfCriticalBugsUpToDate <=bb) else 1

        d=0 if (self.numberOfMajorBugsUpToDate<=bc) else 1
        
        e=1 if (self.numberOfCriticalBugsUpToDate > bb ) else 0
        
        f=1 if (self.numberOfMajorBugsUpToDate> bc) else 0
        
        x = a + b + c + d + e + f
        
        if x<= 0 :
            self.previewState="GOOD"
        elif x <= 2 :
            self.previewState="MEDIUM"
        else :
            self.previewState="BAD"
            
        ch = []
        ch = self.version_used.split(",")
        if ch.__len__() > 1:
            self.previewState="INC."+self.previewState


    def setState(self):
        
        
        bb=(self.numberOfTotalPassed+self.numberOfTotalFailed-self.numberOfTotalBlocked)*0.01
        bx = round(self.numberOfTotalPassed + self.numberOfTotalFailed-self.numberOfTotalBlocked)*0.05
        
        
        bc = 2 if (bx<=2) else bx
        
        a=0 if (self.numberOfCriticalBugs <=0) else 1 

        b=0 if (self.numberOfMajorBugs <=bb) else 1

        c=0 if (self.numberOfCriticalBugs <=bb) else 1

        d=0 if (self.numberOfMajorBugs<=bc) else 1
        
        e=1 if (self.numberOfCriticalBugs > bb ) else 0
        
        f=1 if (self.numberOfMajorBugs> bc) else 0
        
        x = a + b + c + d + e + f
        
        if x<= 0 :
            self.state="GOOD"
        elif x <= 2 :
            self.state="MEDIUM"
        else :
            self.state="BAD"
            
        ch = []
        ch = self.version_used.split(",")
        if ch.__len__() > 1:
            self.state="INC."+self.state




        

       
        
    def setbugsSettings(self):
        bugsID=[]
        for i in self.bugs :
            if i.bugId in bugsID:
                i.remove_duplicate='No'
            else :
                i.remove_duplicate='Yes'
                bugsID.append(i.bugId)
            i.testcaseaffected=sum(p.bugId == i.bugId for p in self.bugs)
        self.bugsNonDuplicated=list(set(self.bugs))
        
        for i in self.bugsNonDuplicated:
            
            if i.priority == 'Critical (P0)':
                self.numberOfCriticalBugs=self.numberOfCriticalBugs+1
            if i.priority == 'Major (P1)':
                self.numberOfMajorBugs=self.numberOfMajorBugs+1
            if i.priority == 'Medium (P2)':
                self.numberOfMediumBugs=self.numberOfMediumBugs+1
            if i.priority == 'Minor (P3)':
                self.numberOfMinorBugs=self.numberOfMinorBugs+1
                
                
        self.numberofbugs=len(self.bugsNonDuplicated)
        self.numberofbugsUpToDate=self.numberofbugs
        self.numberOfCriticalBugsUpToDate=self.numberOfCriticalBugs
        self.numberOfMajorBugsUpToDate=self.numberOfMajorBugs
        self.numberOfMediumBugsUpToDate=self.numberOfMediumBugs
        self.numberOfMinorBugsUpToDate=self.numberOfMinorBugs
        
        for i in self.bugsNonDuplicated:
                
            if i.state == 'RESOLVED' or i.state == 'INTEGRATED':
                    self.numberofbugsUpToDate=self.numberofbugsUpToDate-1
                    
                    if i.priority == 'Critical (P0)':
                        self.numberOfCriticalBugsUpToDate=self.numberOfCriticalBugsUpToDate-1
                    if i.priority == 'Major (P1)':
                        self.numberOfMajorBugsUpToDate=self.numberOfMajorBugsUpToDate-1
                    if i.priority == 'Medium (P2)':
                        self.numberOfMediumBugsUpToDate=self.numberOfMediumBugsUpToDate-1
                    if i.priority == 'Minor (P3)':
                        self.numberOfMinorBugsUpToDate=self.numberOfMinorBugsUpToDate-1
        
        
        
          

    
    def setAssignedTests(self):
        res = self.es.search(index="testplan_tcversions", doc_type="testplan_tcversions",size=10000, from_=0, body={"query": {"bool": {"must":[{ "match": { "testplan_id": self.testPlanId }} ,{ "match": { "platform_id": self.platformID }} ]}}})
        j = 0
        k = 0
        for doc in res['hits']['hits']:
            #print(doc['_source']['tcversion_id'])
            #s = doc['_source']['tcversion_id']
            resultat = self.es.search(index="tcversions", doc_type="tcversions",size=10000, from_=0, body={"query": {"bool": {"must":[{ "match": { "id": doc['_source']['tcversion_id'] }} ]}}})
            for i in resultat['hits']['hits']:
                #print (i['_source']['execution_type'])
                if i['_source']['execution_type'] == 2:
                    j=j+1
                    #print ("Automated test")
                if i['_source']['execution_type'] == 1:
                    k=k+1
                    #print("Manuel test ",k)
        self.numberOfAssignedAutomatedTests=j
        self.numberOfAssignedManualTests = k
        self.numberOfTotalAssigned=self.numberOfAssignedAutomatedTests + self.numberOfAssignedManualTests
        
        #print ("Number of Automated tests ",j)
        #print ("Number of Manual tests ",k)
    def getRedundantTests(self,testList):
        redundantList = []
        tc_versionlist = []
        for i in testList :
            if i.tcversion_id in tc_versionlist :
              redundantList.append(i.tcversion_id) 
            tc_versionlist.append(i.tcversion_id)
        #print (list(set(redundantList)))
        return list(set(redundantList))
    
    def getLastExecutionFromRdundantTests(self,redundantList):
        result = []
        for i in redundantList:
            search = self.es.search(index="executions", doc_type="executions",size=10000, from_=0, body={"query": {"bool": {"must":[{ "match": { "testplan_id": self.testPlanId }} ,{ "match": { "platform_id": self.platformID }},{ "match": { "build_id": self.buildID }},{ "match": { "tcversion_id": i }} ]}}})
            Mylist = []
            for doc in search['hits']['hits']:
                Mylist.append(Test(doc['_source']['id'],doc['_source']['tcversion_id'],doc['_source']['execution_ts'],doc['_source']['execution_type'],doc['_source']['status']))
                #print("Hello")
            result.append(self.getMaxDate(Mylist))
        return result
    
    
    def getMaxDate(self,Mylist):
        max = Mylist[0]
        #print("max",max.execution_ts)
        for i in Mylist :
            firtdate = i.execution_ts.split("+")
            seconddate = max.execution_ts.split("+")
            #print(firtdate)
            if datetime.strptime(firtdate[0], '%Y-%m-%dT%H:%M:%S') >  datetime.strptime(seconddate[0], '%Y-%m-%dT%H:%M:%S'):
                max = i
        #print ("Max is "+max.execution_ts)
        return max
        
        
    def setOtherStatus(self):
        testList = []
        self.trueExecution=0
        tcVersionList = []
        for doc in self.globalSearch['hits']['hits']:
            oneTest= Test(doc['_source']['id'],doc['_source']['tcversion_id'],doc['_source']['execution_ts'],doc['_source']['execution_type'],doc['_source']['status'])
            self.date=doc['_source']['execution_ts'].split("T")[0]
            testList.append(oneTest)

        
        tc_versionlist = []
        final_testList=[]
        non_duplicated_list = []
        self.testList = testList
        redundantList = self.getRedundantTests(testList)
        plusList = self.getLastExecutionFromRdundantTests(redundantList)
        
        
        for i in testList :
            if i.tcversion_id in redundantList :
                #print("this is the redondante")
                #print (i.tcversion_id,i.execution_ts)
                continue
            non_duplicated_list.append(i)
        
        final_testList = plusList + non_duplicated_list
            
        for i in final_testList :
            #print (i.execution_type)
            result = self.es.search(index="cfield_execution_values", doc_type="cfield_execution_values",size=100, from_=0, body={"query": {"bool": {"must":[{ "match": { "field_id": 9 }},{ "match": { "execution_id": i.id }}]}}})
            for doc in result['hits']['hits']:
                #print(doc['_source']['value'])
                self.version_used.append(format_version(doc['_source']['value']))
            if int(i.execution_type) == 1 :
                #print('Manual execution')
                if i.status == "p":
                    self.numberOfPassedManualTests = self.numberOfPassedManualTests + 1
                if i.status == "b":
                    self.numberOfBlockedManualTests=self.numberOfBlockedManualTests+1
                    if self.getBugByExecutionId(i.id) == None :
                        print("")
                    else: 
                        onebug = self.getBugByExecutionId(i.id)
                            #print(" TestPlanName :"+ onebug.testPlanName+" bug_status "+onebug.state)
                        self.bugs.append(onebug) 
                        
                if i.status == "f" :
                    self.numberOfFailedManualTests = self.numberOfFailedManualTests + 1
                
                    if self.getBugByExecutionId(i.id) == None :
                        print("")
                    else: 
                        onebug = self.getBugByExecutionId(i.id)
                            #print(" TestPlanName :"+ onebug.testPlanName+" bug_status "+onebug.state)
                        self.bugs.append(onebug)
                        
            if i.execution_type == 2 :
                self.trueExecution = self.trueExecution+1 
                #print('Automated execution')
                if i.status == "p":
                    self.numberOfPassedAutomatedTests = self.numberOfPassedAutomatedTests + 1
                    
                if i.status == "b":
                    self.numberOfBlockedAutomatedTests=self.numberOfBlockedAutomatedTests+1
                    if self.getBugByExecutionId(i.id) == None :
                        print("")
                    else: 
                        onebug = self.getBugByExecutionId(i.id)
                            #print(" TestPlanName :"+ onebug.testPlanName+" bug_status "+onebug.state)
                        self.bugs.append(onebug)
                    
                if i.status == "f" :
                    self.numberOfFailedAutomatedTests = self.numberOfFailedAutomatedTests + 1
                    if self.getBugByExecutionId(i.id) == None :
                        print("")
                    else: 
                        onebug = self.getBugByExecutionId(i.id)
                            #print(" TestPlanName :"+ onebug.testPlanName+" bug_status "+onebug.state)
                        self.bugs.append(onebug)
                    
  
        
        self.numberOfAutomatedNotExecuted=self.numberOfAssignedAutomatedTests-self.numberOfPassedAutomatedTests-self.numberOfFailedAutomatedTests-self.numberOfBlockedAutomatedTests
        self.numberOfManualNotExecuted=self.numberOfAssignedManualTests-self.numberOfPassedManualTests-self.numberOfFailedManualTests-self.numberOfBlockedManualTests
        
        self.numberOfTotalPassed=self.numberOfPassedAutomatedTests+self.numberOfPassedManualTests
        self.numberOfTotalFailed=self.numberOfFailedAutomatedTests+self.numberOfFailedManualTests
        self.numberOfTotalBlocked=self.numberOfBlockedManualTests+self.numberOfBlockedAutomatedTests
        self.numberOfTotalNotExecuted=self.numberOfTotalAssigned-self.numberOfTotalPassed-self.numberOfTotalFailed-self.numberOfTotalBlocked
        
        
        ###################################################################################################
        #### Correction for some database incoherent data (assigned test are manual but execution is not)##
        ###################################################################################################
        
        if self.numberOfAutomatedNotExecuted < 0 and self.trueExecution == self.numberOfTotalPassed+self.numberOfTotalFailed+self.numberOfTotalBlocked :
            self.numberOfAssignedAutomatedTests=self.numberOfTotalAssigned
            self.numberOfPassedAutomatedTests=self.numberOfTotalPassed
            self.numberOfFailedAutomatedTests=self.numberOfTotalFailed
            self.numberOfAutomatedNotExecuted=self.numberOfTotalNotExecuted
            self.numberOfBlockedAutomatedTests=self.numberOfTotalBlocked
            self.numberOfBlockedManualTests=0
            self.numberOfAssignedManualTests=0
            self.numberOfFailedManualTests=0
            self.numberOfPassedManualTests=0
            self.numberOfManualNotExecuted=0
            
        elif self.numberOfAutomatedNotExecuted < 0 or self.numberOfManualNotExecuted < 0:
            
            self.numberOfAssignedManualTests=self.numberOfFailedManualTests+self.numberOfPassedManualTests+self.numberOfBlockedManualTests
            self.numberOfAssignedAutomatedTests=self.numberOfPassedAutomatedTests+self.numberOfFailedAutomatedTests+self.numberOfBlockedAutomatedTests
            self.numberOfAutomatedNotExecuted=0
            self.numberOfManualNotExecuted=self.numberOfTotalNotExecuted
            
        if self.numberOfAssignedAutomatedTests < self.numberOfAutomatedNotExecuted :
            self.numberOfAutomatedNotExecuted = self.numberOfAssignedAutomatedTests - (self.numberOfFailedAutomatedTests +self.numberOfBlockedAutomatedTests+self.numberOfPassedAutomatedTests)
         
        if self.numberOfAssignedManualTests < self.numberOfManualNotExecuted :
            self.numberOfManualNotExecuted = self.numberOfAssignedManualTests - (self.numberOfFailedManualTests + self.numberOfBlockedManualTests + self.numberOfPassedManualTests )
            
        if self.numberOfTotalAssigned != (self.numberOfAssignedAutomatedTests + self.numberOfAssignedManualTests):
            if "Automated" in self.testPlanName or "automated" in self.testPlanName:
                self.numberOfAssignedAutomatedTests=self.numberOfTotalAssigned-self.numberOfAssignedManualTests
                self.numberOfAutomatedNotExecuted = self.numberOfAssignedAutomatedTests - (self.numberOfFailedAutomatedTests +self.numberOfBlockedAutomatedTests+self.numberOfPassedAutomatedTests)
                self.numberOfManualNotExecuted = self.numberOfAssignedManualTests - (self.numberOfFailedManualTests + self.numberOfBlockedManualTests + self.numberOfPassedManualTests )
            else : 
                self.numberOfAssignedManualTests = self.numberOfTotalAssigned-self.numberOfAssignedAutomatedTests
                self.numberOfManualNotExecuted = self.numberOfAssignedManualTests - (self.numberOfFailedManualTests + self.numberOfBlockedManualTests + self.numberOfPassedManualTests )
                self.numberOfAutomatedNotExecuted = self.numberOfAssignedAutomatedTests - (self.numberOfFailedAutomatedTests +self.numberOfBlockedAutomatedTests+self.numberOfPassedAutomatedTests)
        ###############################    
        #### Ending correction Bloc ###
        ###############################
        
        self.version_used = map(str.strip, self.version_used)
        self.version_used = list(set(self.version_used))
        if len(self.version_used) > 2:
            self.version_used=self.version_used[0:2]
            self.version_used.append("*")
        self.version_used = ",".join(str(x) for x in self.version_used)
        
    def getBugByExecutionId(self,executionID):
        bugId=""
        res = self.es.search(index="execution_bugs", doc_type="execution_bugs",size=10000, from_=0, body={"query": {"bool": {"must":[{ "match": { "execution_id": executionID }}]}}})
        for doc in res['hits']['hits']:
            bugId=doc['_source']['bug_id']
            #print(doc['_source']['execution_id'],doc['_source']['bug_id'])
        
        #print ("hhhhhhhhhhhhhhhhhhhhhh"+bugId)
        if bugId == "":
            # ("NOOOOOOOOOOOOOOOOOOOOOOOOOOO"+bugId)
            return None
        
        result = self.es.search(index="bugs", doc_type="bugs",size=500, from_=0, body={"query": {"bool": {"must":[{ "match": { "bug_id": bugId }}]}}})
        
        if(len(result['hits']['hits'])==0):
            onebug = Bug(self.testPlanName,bugId,"N/A","N/A","N/A","N/A",self.buildName,"N/A",self.plateformName,"N/A")
            return onebug
        
        for i in result['hits']['hits']:
            #print("Yeeeeeeeeeeeeeeeeeeeeees",i['_source']['short_desc'])
            onebug = Bug(self.testPlanName,bugId,i['_source']['short_desc'],i['_source']['bug_status'],i['_source']['priority'],i['_source']['bug_severity'],self.buildName,i['_source']['version'],self.plateformName,i['_source']['cf_external_reference'])
            return onebug
        
#        print(str(j))

          
class Test():
    def __init__(self,id,tcversion_id,execution_ts,execution_type,status):
        self.id=id
        self.tcversion_id = tcversion_id
        self.execution_ts = execution_ts
        self.execution_type = execution_type
        self.status=status
        

        
        
        
class Build ():
    def __init__(self,buildName,buildId):
        self.buildName = buildName
        self.buildId = buildId
        
class Project ():
    def __init__(self,projectId,start,end):
        global start_day 
        global end_day 
        start_day= start
        end_day = end
        
        self.es = Elasticsearch()
        self.projectId = projectId
        res = self.es.search(index="nodes_hierarchy", doc_type="nodes_hierarchy",size=2, from_=0, body={"query": {"bool": {"must":[{ "match": { "node_type_id": "1"}},{ "match": { "id": self.projectId }}]}}})
        for doc in res['hits']['hits']:
            self.projectName = doc['_source']['name']
        self.testPlans = None
        self.setTestPlans()
        
    def setTestPlans(self):
        res = self.es.search(index="nodes_hierarchy", doc_type="nodes_hierarchy",size=10000, from_=0, body={"query": {"bool": {"must":[{ "match": { "node_type_id": "5"}},{ "match": { "parent_id": self.projectId }}]}}})
        testPlansList = []
        for doc in res['hits']['hits']:
            name = doc['_source']['name']
            id = doc['_source']['id']
            oneTestPlan = TestPlan(name,id)
            testPlansList.append(oneTestPlan)
        self.testPlans = testPlansList
        
class Project_list():
    def __init__(self,project_list):
        self.prj_list =[]
        for i in project_list:
             self.prj_list.append(Project(i))   

class Bug():
    def __init__(self,testPlanName,bugId,description,state,priority,severity,cycle,version_detected,plateform,cf_external_reference):
        self.testPlanName=testPlanName
        self.bugId=bugId
        self.description=description
        self.state=state
        self.priority=priority
        self.severity=severity
        self.cycle=cycle
        self.version_detected=version_detected
        self.plateform=plateform
        self.testcaseaffected=0
        self.remove_duplicate=""
        self.externalId=cf_external_reference
        
    def __hash__(self):
        return hash(self.bugId)

    def __eq__(self, other):
        return self.bugId == other
        


#a = TestcasesStatus("460","1752984","16028","testPlanName","plateformName","buildName") ## HGW SAH Generic automated
#a = TestcasesStatus("118","89411","1692","testPlanName","plateformName","buildName") ## total automated

#a = TestcasesStatus("66","42391","502","testPlanName","plateformName","buildName") ## cas parfait pour test automated + manual
"""
a = TestcasesStatus("143","135164","460","testPlanName","plateformName","buildName")

print("TOTAL ASSIGNED : "+str(a.numberOfTotalAssigned)+" TOTAL PASSED : "+str(a.numberOfTotalPassed)+" TOTAL FAILED : "+str(a.numberOfTotalFailed)+ " TOTAL NOT EXECUTED : "+str(a.numberOfTotalNotExecuted))
print("MANUAL ASSIGNED : "+str(a.numberOfAssignedManualTests)+" MANUAL PASSED : "+str(a.numberOfPassedManualTests)+" MANUAL FAILED : "+str(a.numberOfFailedManualTests)+ " MANUAL NOT EXECUTED : "+str(a.numberOfManualNotExecuted))
print("AUTOMATED ASSIGNED : "+str(a.numberOfAssignedAutomatedTests)+" AUTOMATED PASSED : "+str(a.numberOfPassedAutomatedTests)+" AUTOMATED FAILED : "+str(a.numberOfFailedAutomatedTests)+ " AUTOMATED NOT EXECUTED : "+str(a.numberOfAutomatedNotExecuted))
print ("Number of bugs detected "+str(a.numberofbugs))
print('Number of critical bugs '+str(a.numberOfCriticalBugs))
print('Number of Major bugs '+str(a.numberOfMajorBugs))
print('Number of Medium bugs '+str(a.numberOfMediumBugs))
print('Number of Minor bugs '+str(a.numberOfMinorBugs))
print('Version used :\n')
print(a.version_used)
#print(a.testList)
#print(a.getLastExecutionFromRdundantTests(a.getRedundantTests(a.testList)))
#print(a.getRedundantTests(a.testList))
  
""" 
"""
import time
start_time = time.time()

#prj = Project("1119099")  ## StarLite
#prj = Project("1902280","2017-10-01","2018-01-01")  ## Telenor
prj = Project("901686","2017-11-01","2018-10-15")  ## MIB4
print("Project Name :",prj.projectName,"Project ID :",prj.projectId)
for i in prj.testPlans:
    print("*******************"+ i.testPlanName +"*********************\n")

    for a in i.testCases:
        print("Test Name:"+a.testPlanName,"Platforme Name :"+a.plateformName,"Build :"+a.buildName+"\n")

        print("\nTestPlanId :"+str(a.testPlanId)+" BuildID :"+str(a.buildID)+" PlatformId :"+str(a.platformID)+"\n")
        print('\nNumber of bugs '+str(a.numberofbugs))
        print('\nNumber of critical bugs '+str(a.numberOfCriticalBugs))
        print('\nNumber of Major bugs '+str(a.numberOfMajorBugs))
        print('\nNumber of Medium bugs '+str(a.numberOfMediumBugs))
        print('\nNumber of Minor bugs '+str(a.numberOfMinorBugs))
        
        print('\nNumber of bugs Up to date '+str(a.numberofbugsUpToDate))
        print('\nNumber of critical bugs Up to date '+str(a.numberOfCriticalBugsUpToDate))
        print('\nNumber of Major bugs Up to date '+str(a.numberOfMajorBugsUpToDate))
        print('\nNumber of Medium bugs Up to date '+str(a.numberOfMediumBugsUpToDate))
        print('\nNumber of Minor bugs Up to date '+str(a.numberOfMinorBugsUpToDate))
        print('\nVersion used :\n')
        print(a.version_used)
        print("\n")
        print('Date :\n')
        print(a.date)
        print("\n")
        for k in a.bugs : 
            print(str(k.bugId)+ " "+str(k.testcaseaffected)+ " Remove :"+k.remove_duplicate)
        
        print('\nPreview State  '+str(a.previewState))
        print('\nState  '+str(a.state)+"\n")


print("--- %s seconds ---" % (time.time() - start_time))

"""
"""
test = TestPlan("Common","216939")  

for i in test.platforms:
    print(i.platformName,i.platformId)
"""
#s = Search()
#print(s.getplatformname("26"))
#s.getPlatformIdsFromTestPlanID("226149")
#res = s.getallprojects("HGW") 
#res = s.gettestplanfromprojectID("187076")
#res=s.getplatformfromprojectID("187076")
#res=s.getbuildfromtestplanid("216939")



"""

resul = s.getAllAssignedtests("216939","180")
print("%d Assigned tests found" % resul['hits']['total'])
res = s.getExecutions("216939","180","1599")
i = 1
print("%d documents found" % res['hits']['total'])
for doc in res['hits']['hits']:
    #print(doc['_source']['name'], doc['_source']['id'])
    print(i ,doc['_source']['status'], doc['_source']['id'])
    i = i+1
"""
"""
a= getprojectsHGW()
j=0
for i in a :
    j=j+1
    print(i.name ,j)


mylist=['1902280']
a = Project_list(mylist)

for i in a.prj_list:
    print(i.projectName)

"""
#es = Elasticsearch()
#globalSearch = es.search(index="executions", doc_type="executions",size=1000, from_=0, body={"query": {"bool": {"must":[{ "match": { "testplan_id": "1752984" }} ,{ "match": { "platform_id": "460" }},{ "match": { "build_id": "16028" }}]}},"filter": {"range" : { "execution_ts" : {"from": "2017-03-28","to": "2022-01-01","time_zone": "+01:00"}}}})
#print(globalSearch)


