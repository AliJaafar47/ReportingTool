from django.db import models

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

import uuid
from django.template.defaultfilters import default
from platform import platform

# Create your models here.
    
class Project(models.Model):
    name = models.CharField(max_length=200, help_text="Name of project")
    projectID = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    def save_project(self):
        if self.name_present(self.name):
            print("Name exists")
            return (Project.objects.get(projectID=self.projectID))
        else :
            print("Name don't exist")
            self.save()
            return self
            
        
    def name_present(self,name):
        if Project.objects.filter(name=name).exists():
            return True
    
        return False
    
class Test_Plan(models.Model):

    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200,help_text="Test Plan name")
    platform = models.CharField(max_length=200,help_text="Test Plan Platform")
    cycle = models.CharField(max_length=200,help_text="Cycle")
    version = models.CharField(max_length=2000,help_text="Version")
    state = models.CharField(max_length=200,help_text="State")
    preview_state = models.CharField(max_length=200,help_text="Preview State")
    
    assigned_total = models.IntegerField(help_text="assigned_total")
    passed_total = models.IntegerField(help_text="passed_total")
    not_executed_total = models.IntegerField(help_text="not_executed_total")
    failed_total = models.IntegerField(help_text="failed_total")
    blocked_total = models.IntegerField(help_text="blocked_total")
    
    passed_total_pr = models.CharField(max_length=200)
    not_executed_total_pr = models.CharField(max_length=200)
    failed_total_pr = models.CharField(max_length=200)
    blocked_total_pr = models.CharField(max_length=200)
    
    
    assigned_manual = models.IntegerField(help_text="assigned_manual")
    passed_manual = models.IntegerField(help_text="passed_manual")
    not_executed_manual = models.IntegerField(help_text="not_executed_manual")
    failed_manual = models.IntegerField(help_text="failed_manual")
    blocked_manual = models.IntegerField(help_text="blocked_manual")
    
    passed_manual_pr = models.CharField(max_length=200)
    not_executed_manual_pr = models.CharField(max_length=200)
    failed_manual_pr = models.CharField(max_length=200)
    blocked_manual_pr = models.CharField(max_length=200)
    
    assigned_automated = models.IntegerField(help_text="assigned_automated")
    passed_automated = models.IntegerField(help_text="passed_automated")
    not_executed_automated = models.IntegerField(help_text="not_executed_automated")
    failed_automated = models.IntegerField(help_text="failed_automated")
    blocked_automated = models.IntegerField(help_text="blocked_automated")
    
    passed_automated_pr = models.CharField(max_length=200)
    not_executed_automated_pr = models.CharField(max_length=200)
    failed_automated_pr = models.CharField(max_length=200)
    blocked_automated_pr = models.CharField(max_length=200)
    
    number_of_bug_up_to_date = models.IntegerField(help_text="number_of_bug_up_to_date")
    number_of_critical_bug_up_to_date = models.IntegerField(help_text="number_of_critical_bug_up_to_date")
    number_of_major_bug_up_to_date = models.IntegerField(help_text="number_of_major_bug_up_to_date")
    number_of_medium_bug_up_to_date = models.IntegerField(help_text="number_of_medium_bug_up_to_date")
    number_of_minor_bug_up_to_date = models.IntegerField(help_text="number_of_minor_bug_up_to_date")
    
    number_of_bug = models.IntegerField(help_text="number_of_bug")
    number_of_critical_bug = models.IntegerField(help_text="number_of_critical")
    number_of_major_bug = models.IntegerField(help_text="number_of_major_bug")
    number_of_medium_bug = models.IntegerField(help_text="number_of_medium_bug")
    number_of_minor_bug = models.IntegerField(help_text="number_of_minor_bug")
    reviwed=models.BooleanField(default=False)
    xdate=models.DateField()
    
    
    
    
    def __str__(self):
        return self.name +" "+self.platform +" "+self.cycle
    
    def as_dict(self):
        return {
            "project": self.project.name,
            "name":self.name,
            "platform":self.platform,
            "cycle":self.cycle,
            "version":self.version,
            "state":self.state,
            "preview_state":self.preview_state,
            
            "assigned_total":self.assigned_total,
            "passed_total":self.passed_total,
            "not_executed_total":self.not_executed_total,
            "failed_total":self.failed_total,
            "blocked_total":self.blocked_total,
            
            "passed_total_pr":self.passed_total_pr,
            "not_executed_total_pr":self.not_executed_total_pr,
            "failed_total_pr":self.failed_total_pr,
            "blocked_total_pr":self.blocked_total_pr,
            
            "assigned_manual":self.assigned_manual,
            "passed_manual" : self.passed_manual,
            "not_executed_manual" : self.not_executed_manual,
            "failed_manual": self.failed_manual,
            "blocked_manual":self.blocked_manual,
            
            "passed_manual_pr" : self.passed_manual_pr,
            "not_executed_manual_pr" : self.not_executed_manual_pr,
            "failed_manual_pr": self.failed_manual_pr,
            "blocked_manual_pr":self.blocked_manual_pr,
            
            "assigned_automated":self.assigned_automated,
            "passed_automated":self.passed_automated,
            "not_executed_automated":self.not_executed_automated,
            "failed_automated":self.failed_automated,
            "blocked_automated": self.blocked_automated,
            
            "passed_automated_pr":self.passed_automated_pr,
            "not_executed_automated_pr":self.not_executed_automated_pr,
            "failed_automated_pr":self.failed_automated_pr,
            "blocked_automated_pr": self.blocked_automated_pr,
    
            "number_of_bug_up_to_date":self.number_of_bug_up_to_date,
            "number_of_critical_bug_up_to_date":self.number_of_critical_bug_up_to_date,
            "number_of_major_bug_up_to_date":self.number_of_major_bug_up_to_date,
            "number_of_medium_bug_up_to_date":self.number_of_medium_bug_up_to_date,
            "number_of_minor_bug_up_to_date":self.number_of_minor_bug_up_to_date,
                
            "number_of_bug":self.number_of_bug,
            "number_of_critical_bug":self.number_of_critical_bug,
            "number_of_major_bug":self.number_of_major_bug,
            "number_of_medium_bug":self.number_of_medium_bug,
            "number_of_minor_bug":self.number_of_minor_bug,
            "reviwed":self.reviwed,
            "xdate":str(self.xdate),

        }
    def TestPlanExists(self,project,name,platform,cycle):
        if Test_Plan.objects.filter(project=project,name=name,platform=platform,cycle=cycle).exists():
            return True
    
        return False
    
    def save_TestPlan(self):
        if self.TestPlanExists(self.project,self.name,self.platform,self.cycle):
            #print("Name exists")
            Test_Plan.objects.filter(project=self.project,name=self.name,platform=self.platform,cycle=self.cycle).update(reviwed=self.reviwed,state=self.state,preview_state=self.preview_state,assigned_total=self.assigned_total,passed_total=self.passed_total,not_executed_total=self.not_executed_total,failed_total=self.failed_total,blocked_total=self.blocked_total,passed_total_pr=self.passed_total_pr,not_executed_total_pr=self.not_executed_total_pr,failed_total_pr=self.failed_total_pr,blocked_total_pr=self.blocked_total_pr,assigned_manual=self.assigned_manual,passed_manual=self.passed_manual,not_executed_manual=self.not_executed_manual,failed_manual=self.failed_manual,blocked_manual=self.blocked_manual,passed_manual_pr=self.passed_manual_pr,not_executed_manual_pr=self.not_executed_manual_pr,failed_manual_pr=self.failed_manual_pr,blocked_manual_pr=self.blocked_manual_pr,assigned_automated=self.assigned_automated,passed_automated=self.passed_automated,not_executed_automated=self.not_executed_automated,failed_automated=self.failed_automated,blocked_automated=self.blocked_automated,passed_automated_pr=self.passed_automated_pr,not_executed_automated_pr=self.not_executed_automated_pr,failed_automated_pr=self.failed_automated_pr,blocked_automated_pr=self.blocked_automated_pr,number_of_bug_up_to_date=self.number_of_bug_up_to_date,number_of_critical_bug_up_to_date=self.number_of_critical_bug_up_to_date,number_of_major_bug_up_to_date=self.number_of_major_bug_up_to_date,number_of_medium_bug_up_to_date=self.number_of_medium_bug_up_to_date,number_of_minor_bug_up_to_date=self.number_of_minor_bug_up_to_date,number_of_bug=self.number_of_bug,number_of_critical_bug=self.number_of_critical_bug,number_of_major_bug=self.number_of_major_bug,number_of_medium_bug=self.number_of_medium_bug,number_of_minor_bug=self.number_of_minor_bug)
            #print("Object updated")
            return Test_Plan.objects.get(project=self.project,name=self.name,platform=self.platform,cycle=self.cycle)
            
        else :
            #print("Name don't exist")
            self.save()
            #print("Object saved")
            return self
    def update_test_Plan(self,reviwed,version,state,preview_state,assigned_total,not_executed_total,not_executed_total_pr,passed_total,passed_total_pr,failed_total,failed_total_pr,blocked_total,blocked_total_pr,assigned_manual,not_executed_manual,not_executed_manual_pr,passed_manual,passed_manual_pr,failed_manual,failed_manual_pr,blocked_manual,blocked_manual_pr,assigned_automated,not_executed_automated,not_executed_automated_pr,passed_automated,passed_automated_pr,failed_automated,failed_automated_pr,blocked_automated,blocked_automated_pr,number_of_bug_up_to_date,number_of_critical_bug_up_to_date,number_of_major_bug_up_to_date,number_of_medium_bug_up_to_date,number_of_minor_bug_up_to_date,number_of_bug,number_of_critical_bug,number_of_major_bug,number_of_medium_bug,number_of_minor_bug):
        Test_Plan.objects.filter(project=self.project,name=self.name,platform=self.platform,cycle=self.cycle).update(reviwed=reviwed,version=version,state=state,preview_state=preview_state,assigned_total=assigned_total,not_executed_total=not_executed_total,not_executed_total_pr=not_executed_total_pr,passed_total=passed_total,passed_total_pr=passed_total_pr,failed_total=failed_total,failed_total_pr=failed_total_pr,blocked_total=blocked_total,blocked_total_pr=blocked_total_pr,assigned_manual=assigned_manual,not_executed_manual=not_executed_manual,not_executed_manual_pr=not_executed_manual_pr,passed_manual=passed_manual,passed_manual_pr=passed_manual_pr,failed_manual=failed_manual,failed_manual_pr=failed_manual_pr,blocked_manual=blocked_manual,blocked_manual_pr=blocked_manual_pr,assigned_automated=assigned_automated,not_executed_automated=not_executed_automated,not_executed_automated_pr=not_executed_automated_pr,passed_automated=passed_automated,passed_automated_pr=passed_automated_pr,failed_automated=failed_automated,failed_automated_pr=failed_automated_pr,blocked_automated=blocked_automated,blocked_automated_pr=blocked_automated_pr,number_of_bug_up_to_date=number_of_bug_up_to_date,number_of_critical_bug_up_to_date=number_of_critical_bug_up_to_date,number_of_major_bug_up_to_date=number_of_major_bug_up_to_date,number_of_medium_bug_up_to_date=number_of_medium_bug_up_to_date,number_of_minor_bug_up_to_date=number_of_minor_bug_up_to_date,number_of_bug=number_of_bug,number_of_critical_bug=number_of_critical_bug,number_of_major_bug=number_of_major_bug,number_of_medium_bug=number_of_medium_bug,number_of_minor_bug=number_of_minor_bug)

        
    
class Bug(models.Model):
    test_plan = models.ForeignKey('Test_Plan', on_delete=models.SET_NULL, null=True)
    bugID = models.IntegerField(help_text="bugID")
    description = models.CharField(max_length=5000)
    state = models.CharField(max_length=200)
    priority=models.CharField(max_length=200)
    severity=models.CharField(max_length=200)
    test_Cases_Affected= models.IntegerField()
    remove_Duplicate = models.CharField(max_length=5)
    external_ID = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.bugID)+"  "+str(self.description) +"  "+str(self.state)
    
    def as_dict(self):
        return {
            "test_plan": self.test_plan.name,
            "cycle_used":self.test_plan.cycle,
            "version_detected":self.test_plan.version,
            "platform_used":self.test_plan.platform,
            "bugID":self.bugID,
            "description" :self.description,
            "state" : self.state,
            "priority":self.priority,
            "severity" : self.severity,
            "test_Cases_Affected":self.test_Cases_Affected,
            "remove_Duplicate" : self.remove_Duplicate,
            "external_ID" : self.external_ID
            }
    def BugExist(self,bugID,test_plan):
        if Bug.objects.filter(bugID=bugID,test_plan=test_plan).exists():
            return True
    
        return False
        
    def save_Bug(self):
        if self.BugExist(self.bugID,self.test_plan):
            print("Name exists")
            Bug.objects.filter(test_plan=self.test_plan,bugID=self.bugID).update(description=self.description,state=self.state,priority=self.priority,severity=self.severity,test_Cases_Affected=self.test_Cases_Affected,external_ID=self.external_ID)
            print("Object updated")
            
        else :
            print("Name don't exist")
            self.save()
            print("Object saved")
            
    
class Topic(models.Model):
    name = models.CharField(max_length=200,unique=True, help_text="Name of the Topic")
    
    def __str__(self):
        return self.name
    
class Test_Classification(models.Model):
    name = models.CharField(max_length=200,unique=True, help_text="Name of Test-Plan")
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    choix = (("Common", 'Common'),("Uncommon", 'Uncommon'),("Very Uncommon", 'Very Uncommon'))
    frequency = models.CharField(choices=choix,max_length=200)
    
    def __str__(self):
        return self.name +" "+ self.topic.name + " "+self.frequency
    
    def as_dict(self):
        return {
            "test_plan_name": self.name,
            "topic":self.topic.name,
            "frequency":self.frequency,
            }
        
        
class Short_Name (models.Model):
    name = models.CharField(max_length=200,unique=True, help_text="Project Name")
    shortName = models.CharField(max_length=200, help_text="shortName",null=False)
    
    def __str__(self):
        return self.name +" "+ self.shortName
    
    def as_dict(self):
        return {
            "project_name": self.name,
            "shortName":self.shortName,
            
            }
