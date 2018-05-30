from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from . import elasticsearchAPI as api
from django.http import HttpResponse
from .models import Project, Test_Plan,Bug, Topic,Test_Classification,Short_Name
from django.http import JsonResponse
from django.core import serializers
import json
from django.template.context_processors import request
from datetime import datetime
import os
import subprocess

def index(request):
    return render(request,'index.html',context={})



@login_required(login_url='/accounts/login/')
def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    value = False
    global data 
    global project_name_list
    a = api.getprojectsSTB()
    b= api.getprojectsHGW()
    
    if request.is_ajax():
        print("ajax")
        data = json.loads(request.POST.get('json_items'))
        bugs = json.loads(request.POST.get('json_bugs'))
        for i in data:

            if (Project.objects.filter(name=i[1]).exists()):
                oneProject=Project.objects.get(name=i[1])
                if(Test_Plan.objects.filter(project=oneProject,name=i[2],platform=i[3],cycle=i[4]).exists()):
                    oneTest = Test_Plan.objects.get(project=oneProject,name=i[2],platform=i[3],cycle=i[4])
                    oneTest.update_test_Plan(i[0],i[5],i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],i[25],i[26],i[27], i[28], i[29], i[30], i[31], i[32], i[33], i[34], i[35], i[36], i[37], i[38], i[39], i[40], i[41], i[42], i[43], i[44])
                
                else : 
                    date = datetime.strptime(i[45], '%Y-%m-%d')
                    
                    oneTestplan= Test_Plan(reviwed=i[0],project=oneProject,name=i[2],platform=i[3],cycle=i[4],version=i[5], state=i[6],preview_state=i[7],assigned_total=i[8],not_executed_total=i[9],not_executed_total_pr=i[10],passed_total=i[11],passed_total_pr=i[12],failed_total=i[13],failed_total_pr=i[14],blocked_total=i[15],blocked_total_pr=i[16],assigned_manual=i[17],not_executed_manual=i[18],not_executed_manual_pr=i[19],passed_manual=i[20],passed_manual_pr=i[21],failed_manual=i[22],failed_manual_pr=i[23],blocked_manual=i[24],blocked_manual_pr=i[25],assigned_automated=i[26],not_executed_automated=i[27],not_executed_automated_pr=i[28],passed_automated=i[29],passed_automated_pr=i[30],failed_automated=i[31],failed_automated_pr=i[32],blocked_automated=i[33],blocked_automated_pr=i[34],number_of_bug_up_to_date=i[35],number_of_critical_bug_up_to_date=i[36],number_of_major_bug_up_to_date=i[37],number_of_medium_bug_up_to_date=i[38],number_of_minor_bug_up_to_date=i[39],number_of_bug=i[40],number_of_critical_bug=i[41],number_of_major_bug=i[42],number_of_medium_bug=i[43],number_of_minor_bug=i[44],xdate=date)
                    #print(oneTestplan)
                    savedTestplan = oneTestplan.save_TestPlan()
                    
            else : 
                oneProject=Project(name=i[1],projectID=api.getIDNameFromProjectName(i[1]))
                savedProject = oneProject.save_project()
                date = datetime.strptime(i[45], '%Y-%m-%d')
                print(i)
                oneTestplan= Test_Plan(reviwed=i[0],project=oneProject,name=i[2],platform=i[3],cycle=i[4],version=i[5], state=i[6],preview_state=i[7],assigned_total=i[8],not_executed_total=i[9],not_executed_total_pr=i[10],passed_total=i[11],passed_total_pr=i[12],failed_total=i[13],failed_total_pr=i[14],blocked_total=i[15],blocked_total_pr=i[16],assigned_manual=i[17],not_executed_manual=i[18],not_executed_manual_pr=i[19],passed_manual=i[20],passed_manual_pr=i[21],failed_manual=i[22],failed_manual_pr=i[23],blocked_manual=i[24],blocked_manual_pr=i[25],assigned_automated=i[26],not_executed_automated=i[27],not_executed_automated_pr=i[28],passed_automated=i[29],passed_automated_pr=i[30],failed_automated=i[31],failed_automated_pr=i[32],blocked_automated=i[33],blocked_automated_pr=i[34],number_of_bug_up_to_date=i[35],number_of_critical_bug_up_to_date=i[36],number_of_major_bug_up_to_date=i[37],number_of_medium_bug_up_to_date=i[38],number_of_minor_bug_up_to_date=i[39],number_of_bug=i[40],number_of_critical_bug=i[41],number_of_major_bug=i[42],number_of_medium_bug=i[43],number_of_minor_bug=i[44],xdate=date)
                #print(oneTestplan)
                savedTestplan = oneTestplan.save_TestPlan()
                
        for j in bugs :
            #print(j)
            testplan= Test_Plan.objects.get(name=j[0],platform=j[8],cycle=j[6])
            oneBug= Bug(test_plan=testplan,bugID=j[1],description=j[2],state=j[3],priority=j[4],severity=j[5],test_Cases_Affected=j[9],remove_Duplicate=j[10],external_ID=j[11])
            oneBug.save_Bug()
        return HttpResponse("OK")
        
    if request.POST.get("final_view"):
        project_name_list = []
        final_dic =[]
        final_dic_bug = []
        bugs = []
        final_dic_bugs = []
        projects=[]
        for key, value in request.POST.items():
            #print("key "+key+"value "+value)
            if key == "start_date":
                start_date = value
            if key == "end_date":
                end_date = value
            if key == "projects":
                projects = value.split(",")
        if not projects:
            return (final_view(request))
        
        for i in projects:
            
            try :
                project = Project.objects.get(name=i)
                project_name_list.append(project)
            except :
                pass
            print(i)
            test_plans = Test_Plan.objects.all().filter(project=project,xdate__range=[start_date, end_date],reviwed=True)
            for j in test_plans : 
                bug = Bug.objects.all().filter(test_plan=j)
                dictionaries_bug = [ obj.as_dict() for obj in bug]
                final_dic_bug = dictionaries_bug + final_dic_bug 
                    
            dictionaries = [ obj.as_dict() for obj in test_plans] 
            final_dic = dictionaries + final_dic
            final_dic_bugs = final_dic_bug + final_dic_bugs

                
        bugs_final = json.dumps({"data": final_dic_bugs})
        data = json.dumps({"data": final_dic})
        classification = Test_Classification.objects.all()
        dictionaries_class = [ obj.as_dict() for obj in classification]
        class_final = json.dumps({"data": dictionaries_class})
        print(bugs_final)
        print(data)
        project_name_list.sort(key=lambda Project: Project.name.lower())
        
        # abreviation 
        abr = Short_Name.objects.all().order_by('name')
        dictionaries_abr = [ obj.as_dict() for obj in abr]
        abr_final = json.dumps({"data": dictionaries_abr})
        
        return render(request,'final_view_result.html',context={'projects_list':project_name_list ,'projects_content': data,'projects_bugs': bugs_final,'test_classification':class_final,'abbreviation':abr_final})

    
    if request.POST.get("sava_button"):
        print("save button")
    if request.POST.get("stop"):
        value = True
        print("STOP")
    if request.POST.get("report_generator"):
        # <view logic>
            
            project_content=[]
            project_name_list = []
            prj_list=[]
            test_list=[]
            bugs_list=[]
            for key, value in request.POST.items():
                if(key=="start_day"):
                    start_day=value
                if(key=="end_day"):
                    end_day=value
                
                
            print("start_day :"+start_day+ " end_day :"+end_day)
            
            for key, value in request.POST.items():
                
 
                if value == True : 
                    break
                    
                if key.isdigit() and value == "on":
                    print (key, value)
                    
                    projectName=api.getProjectNameFromId(key)
                    oneProject=Project(name=projectName,projectID=key)
                    #savedProject = oneProject.save_project()
                    prj_list.append(oneProject)
                    project_name_list.append(oneProject)
                    print(oneProject.projectID)
                    
                    ElasticProject = api.Project(key,start_day,end_day) 
                                       
                    for i in ElasticProject.testPlans:
                        for a in i.testCases:

                            oneTestplan= Test_Plan(project=oneProject,name=a.testPlanName,platform=a.plateformName,cycle=a.buildName,version=a.version_used, state=a.state,preview_state=a.previewState,assigned_total=a.numberOfTotalAssigned,passed_total=a.numberOfTotalPassed,not_executed_total=a.numberOfTotalNotExecuted,failed_total=a.numberOfTotalFailed,blocked_total=a.numberOfTotalBlocked,passed_total_pr=a.numberOfTotalPassed_pr,not_executed_total_pr=a.numberOfTotalNotExecuted_pr,failed_total_pr=a.numberOfTotalFailed_pr,blocked_total_pr=a.numberOfTotalBlocked_pr,assigned_manual=a.numberOfAssignedManualTests,passed_manual=a.numberOfPassedManualTests,not_executed_manual=a.numberOfManualNotExecuted,failed_manual=a.numberOfFailedManualTests,blocked_manual=a.numberOfBlockedManualTests,passed_manual_pr=a.numberOfPassedManualTests_pr,not_executed_manual_pr=a.numberOfManualNotExecuted_pr,failed_manual_pr=a.numberOfFailedManualTests_pr,blocked_manual_pr=a.numberOfBlockedManualTests_pr,assigned_automated=a.numberOfAssignedAutomatedTests,passed_automated=a.numberOfPassedAutomatedTests,not_executed_automated=a.numberOfAutomatedNotExecuted,failed_automated=a.numberOfFailedAutomatedTests,blocked_automated=a.numberOfBlockedAutomatedTests,passed_automated_pr=a.numberOfPassedAutomatedTests_pr,not_executed_automated_pr=a.numberOfAutomatedNotExecuted_pr,failed_automated_pr=a.numberOfFailedAutomatedTests_pr,blocked_automated_pr=a.numberOfBlockedAutomatedTests_pr,number_of_bug_up_to_date=a.numberofbugsUpToDate,number_of_critical_bug_up_to_date=a.numberOfCriticalBugsUpToDate,number_of_major_bug_up_to_date=a.numberOfMajorBugsUpToDate,number_of_medium_bug_up_to_date=a.numberOfMediumBugsUpToDate,number_of_minor_bug_up_to_date=a.numberOfMinorBugsUpToDate,number_of_bug=a.numberofbugs,number_of_critical_bug=a.numberOfCriticalBugs,number_of_major_bug=a.numberOfMajorBugs,number_of_medium_bug=a.numberOfMediumBugs,number_of_minor_bug=a.numberOfMinorBugs,xdate=a.date)
                            #savedTestplan = oneTestplan.save_TestPlan()
                            
                            print(oneTestplan.platform)
                            print(Test_Plan.objects.all().filter(project=oneProject,name=oneTestplan.name).count())
                            if(Project.objects.all().filter(projectID=oneProject.projectID).exists()):

                                project = Project.objects.get(projectID=oneProject.projectID)
                                #print(Test_Plan.objects.all().filter(project=project,name=oneTestplan.name,platform=oneTestplan.platform,cycle=oneTestplan.cycle,version=oneTestplan.version).exists())
                                if(Test_Plan.objects.all().filter(project=project,name=oneTestplan.name,platform=oneTestplan.platform,cycle=oneTestplan.cycle).exists()):
                                    print("Exissst")
                                    extraTest= Test_Plan.objects.get(project=project,name=oneTestplan.name,platform=oneTestplan.platform,cycle=oneTestplan.cycle)
                                    oneTestplan.reviwed=extraTest.reviwed
                            

                            test_list.append(oneTestplan)
                            for j in a.bugs:
                                #print(j.bugId)
                                
                                oneBug= Bug(test_plan=oneTestplan,bugID=j.bugId,description=j.description,state=j.state,priority=j.priority,severity=j.severity,test_Cases_Affected=j.testcaseaffected,remove_Duplicate=j.remove_duplicate,external_ID=j.externalId)
                                #oneBug.save_Bug()
                                bugs_list.append(oneBug)

                
                
                
            dictionaries = [ obj.as_dict() for obj in test_list]
            dictionaries_bugs = [ obj.as_dict() for obj in bugs_list]
            
            bugs_final = json.dumps({"data": dictionaries_bugs})
            data = json.dumps({"data": dictionaries})
            print(data)
            print(bugs_final)
            classification = Test_Classification.objects.all()
            dictionaries_class = [ obj.as_dict() for obj in classification]
            class_final = json.dumps({"data": dictionaries_class})
            print (class_final)
            if len(project_name_list)==0:
                message='Please Select a project'
                return render(request,'design_view.html',context={'projectsHGW':b,'projectsSTB':a,'message':message})
            
            start = json.dumps({"data": start_day})
            
            end = json.dumps({"data": end_day})
            project_name_list.sort(key=lambda Project: Project.name.lower())
            
            # abreviation 
            abr = Short_Name.objects.all().order_by('name')
            dictionaries_abr = [ obj.as_dict() for obj in abr]
            abr_final = json.dumps({"data": dictionaries_abr})
            
            return render(request,'design_view_result.html', context={'projects_list':project_name_list ,'projects_content': data,'projects_bugs': bugs_final,'test_classification':class_final,'start':start,'end':end,'abbreviation':abr_final})
    else : 
            if request.user.groups.filter(name="admins").exists():
                return (design_view(request))
            else :
                return (final_view(request))
            
            
            
            
@login_required(login_url='/accounts/login/')
def login_success_final(request):
    val = False
    project_name_list = []
    final_dic =[]
    final_dic_bug = []
    bugs = []
    final_dic_bugs = []
    if request.POST.get("stop"):
        val = True
        print("STOP")
        return (final_view(request))
    if request.POST.get("re_report_generator"):
        return (final_view(request))
        
        
    if request.POST.get("report_generator"):
        project_content=[]
        project_name_list = []
        
        for key, value in request.POST.items():
            if(key=="start_day"):
                start_day=value
            if(key=="end_day"):
                end_day=value
        
        
        print("start_day"+start_day+"end_day"+end_day)
        
        
        for key, value in request.POST.items():
            if val == True : 
                break            
            if key.isdigit() and value == "on":
                print (key, value)
                
                

                if value == True : 
                    break
                print(key)
                project = Project.objects.get(id=key)
                project_name_list.append(project)
            
                test_plans = Test_Plan.objects.all().filter(project=project,xdate__range=[start_day, end_day],reviwed=True)
                for j in test_plans : 
                    bug = Bug.objects.all().filter(test_plan=j)
                    dictionaries_bug = [ obj.as_dict() for obj in bug]
                    final_dic_bug = dictionaries_bug + final_dic_bug 
                    
                dictionaries = [ obj.as_dict() for obj in test_plans] 
                final_dic = dictionaries + final_dic
                final_dic_bugs = final_dic_bug + final_dic_bugs
                
        if len(project_name_list)==0:
            message='Please Select a project'
            return (final_view_error(request,message))
               
        bugs_final = json.dumps({"data": final_dic_bugs})
        data = json.dumps({"data": final_dic})
        classification = Test_Classification.objects.all()
        dictionaries_class = [ obj.as_dict() for obj in classification]
        class_final = json.dumps({"data": dictionaries_class})
        print(bugs_final)
        print(data)
    project_name_list.sort(key=lambda Project: Project.name.lower())
                
    # abreviation 
    abr = Short_Name.objects.all().order_by('name')
    dictionaries_abr = [ obj.as_dict() for obj in abr]
    abr_final = json.dumps({"data": dictionaries_abr})
    return render(request,'final_view_result.html',context={'projects_list':project_name_list ,'projects_content': data,'projects_bugs': bugs_final,'test_classification':class_final,'abbreviation':abr_final})

    
    
def save_object(request):
    print ('!!!')
    print (request.POST)
    print ('!!!')
    print ('\\\\\\')
    print (request.POST.getlist('google_news_articles[]'))
    print ('\\\\\\')
    return
    
def design_view(request):
    a = api.getprojectsSTB()
    b= api.getprojectsHGW()
    print(b)
    message=""
    if not is_service_running('elasticsearchsync'):
        message="We lost synch with MySQL Distante Databases please contact the adminnistrator"
    return render(request,'design_view.html',context={'projectsHGW':b,'projectsSTB':a,'mess':message})


def final_view(request):
    a = Project.objects.all().filter(name__startswith="HGW").order_by('name')
    b = Project.objects.all().filter(name__startswith="STB").order_by('name')
    message=""
    if not is_service_running('elasticsearchsync'):
        message="We lost synch with MySQL Distante Databases please contact the adminnistrator"

    return render(request,'final_view.html',context={'projectsHGW':a,'projectsSTB':b,'mess':message})

def final_view_error(request,message):
    a = Project.objects.all().filter(name__startswith="HGW").order_by('name')
    b = Project.objects.all().filter(name__startswith="STB").order_by('name')
    #a.sort(key=lambda Project: Project.name.lower())
    #b.sort(key=lambda Project: Project.name.lower())
    return render(request,'final_view.html',context={'projectsHGW':a,'projectsSTB':b,'message':message})

def is_service_running(name):
    with open(os.devnull, 'wb') as hide_output:
        exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()
        return exit_code == 0

