from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView, TemplateView, ListView, DetailView, FormView
from django.views.decorators.csrf import csrf_exempt
from Level_Up_App.forms import NewUserForm, QuestionaireForm
from Level_Up_App.models import User, Questionaire, Course, Job, Skill, JobAndNextHigherPair
from Level_Up_App.courserecommendationrules import SkillGapsFact, CourseRecommender, recommendedcourses
from Level_Up_App.careerknowledgegraph import CareerPathKnowledgeGraph
from Level_Up_App.CareerPathASTARSearch import searchCareerPath
from Level_Up_App.library.df_response_lib import *
import json

### Global Variables
persona = ""
currentPosition = ""
yearsOfWorkingExperience = ""
companyName = ""
emailAddress = ""
jobInterestedIn = ""
careerEndGoalPosition = ""
currentSkillSet = []
careerPref = ""
courseSkillRecommend = list()
jobSkillRecommend = list()

# Create your views here.
def index(request):
    form = NewUserForm()
    form_dict = {'userForm': form}
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['name']
            request.session['careeraspiration'] = form.cleaned_data['careeraspiration']
            form.save()
            return redirect('Level_Up_App:questionaire')
        else:
            return redirect('Level_Up_App:index')
    return render(request, 'Level_Up_App/index.html', form_dict)

def questionaire(request):
    form = QuestionaireForm()
    username = request.session['username']
    user = User.objects.get(name=username)
    form_dict = {'username': username, 'questionaire': form}
    if request.method == 'POST':
        form = QuestionaireForm(request.POST)
        if form.is_valid():
            qform = form.save(commit=False)
            request.session['currPosition'] = str(form.cleaned_data['currPosition'])
            # if user checks the have career aspiration checkbox
            if request.session['careeraspiration'] == True:
                request.session['careerendpoint'] = str(form.cleaned_data['careerGoal'])
            else:
                #TODO:replace with career end point from questionaire
                request.session['careerendpoint'] = 'Chief Information Officer'
            qform.user = user
            qform.save()
            return redirect('Level_Up_App:results')
        else:
            print("Error: Questionaire form invalid!")
    return render(request, 'Level_Up_App/questionaire.html', context=form_dict)

def result(request):
    currPos = request.session['currPosition']
    # Search Career End Point
    # cpkg = CareerPathKnowledgeGraph()
    # careerkg = cpkg.getCareerKnowledgeMap()
    # careerph = cpkg.getCareerPathHeuristic()
    # currPos = request.session['currPosition']
    # endpt = request.session['careerendpoint']
    # print("CurrPos: " + str(currPos))
    # print("EndPt: " + str(endpt))
    # searchCareerPath(careerkg, careerph, currPos, endpt)
    careerendpoint = 'CIO' #TODO

    # Filter job recommendations
    jobs = filterjobs(currPos)

    skills = list()
    skills.append('ARTIFICIAL INTELLIGENCE')
    skills.append('MACHINE LEARNING')
    skills.append('DEEP LEARNING')
    # Filter course recommendation
    courses = filtercourse(skills)

    user = request.session['username']
    result_dict = {'username': user,
                'careerendpoint': careerendpoint,
                'courses': courses,
                'jobs': jobs}
    return render(request, 'Level_Up_App/results.html', result_dict)

def signup(request):
    if request.method == 'POST':
        return redirect('Level_Up_App/signupthanks')
    return render(request, 'Level_Up_App/signup.html')

def signupthanks(request):
    return render(request, 'Level_Up_App/signupthanks.html')

def courserecommendresult(request):
    courses = filtercourse(skills)
    courses_dict = {'courses': courses}
    return render(request, 'Level_Up_App/courserecommend.html', courses_dict)

def jobrecommendresult(request):
    pass

def chatbot(request):
    return render(request, 'Level_Up_App/chatbot.html')
# ************************
# DialogFlow block : START
# ************************

# dialogflow webhook fulfillment
@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    # req = request.get_json(silent=True, force=True)
    # get action from json
    # action = req.get('queryResult').get('action')
    intent_name = req["queryResult"]["intent"]["displayName"]
    # return a fulfillment message
    # if action == 'get_suggestion_chips':
    #     # set fulfillment text
    #     fulfillmentText = 'Suggestion chips Response from webhook'
    #     aog = actions_on_google_response()
    #     aog_sr = aog.simple_response([
    #         [fulfillmentText, fulfillmentText, False]
    #     ])
    #     #create suggestion chips
    #     aog_sc = aog.suggestion_chips(["suggestion1", "suggestion2"])
    #     ff_response = fulfillment_response()
    #     ff_text = ff_response.fulfillment_text(fulfillmentText)
    #     ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    #     reply = ff_response.main_response(ff_text, ff_messages)
    # else:
    #     reply = {'fulfillmentText': 'This is Django test response from webhook. Action or Intent not found'}
    # # return generated response
    # return JsonResponse(reply, safe=False)

# **********************
# DialogFlow Variables : DEFINE
# **********************
    global persona
    global currentPosition
    global yearsOfWorkingExperience
    global companyName
    global emailAddress
    global jobInterestedIn
    global careerEndGoalPosition
    global currentSkillSet
    global careerPref
    global courseSkillRecommend
    global jobSkillRecommend
    resp_text = ""

# **********************
# DialogFlow intents : START
# **********************

    # Persona Curious Explorer
    if intent_name == "A_GetCareerRoadMapInfo":
        persona = "Curious Explorer"
        resp_text = "The Career Road Map shows you a career path to achieve your career aspiration in the shortest time. It is generated based on anonymised data of real career advancement. Would you be interested to discover your career road map?"
    elif intent_name == "A_GetCareerRoadMapInfo - yes":
        resp_text = "Great! First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_GetCareerRoadMapInfo - no":
        resp_text = "Okay what else can I do for you?"
    elif intent_name == "A_GetHighestDemandJob":
        #jobtitle = getHighestDemandJob()
        resp_text =  f"Currently the highest demand job is {jobtitle}"

    # Persona Go Getter
    elif intent_name == "A_GetJobCompetency":
        persona = "Go Getter"
        jobInterestedIn = req["queryResult"]["parameters"]["jobtitle"]
        #competency = getJobCompentency(jobInterestedIn)
        resp_text =  f"{jobInterestedIn} requires the following competencies: {competency}. Would you be interested to see a road map on how to get there?"
    elif intent_name == "A_GetJobCompetency - yes":
        resp_text = "Great! First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_GetJobCompetency - no":
        resp_text = "Okay what else can I do for you?"
    elif intent_name == "A_GetJobDifference":
        persona = "Go Getter"
        jobtitle1 = req["queryResult"]["parameters"]["jobtitle1"]
        jobtitle2 = req["queryResult"]["parameters"]["jobtitle2"]
        print(jobtitle1)
        print(jobtitle2)
        jd1 = getJobDescription(jobtitle1)
        jd2 = getJobDescription(jobtitle2)
        resp_text = f"{jobtitle1} \n {jd1} \n {jobtitle2} \n {jd2} \n Which position are you more interested in?"
        #getJobDescription(job1)
        #getJobDescription(job2)
    elif intent_name == "A_GetJobDifference - custom":
        jobInterestedIn = req["queryResult"]["parameters"]["jobtitle"]
        resp_text = "I see, would you like me to show you a road map on how you can get there?"
    elif intent_name == "A_GetJobDifference - custom - yes":
        resp_text = "Great! First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_GetJobDifference - custom - no":
        resp_text = "Okay what else can I do for you?"
    elif intent_name == "A_GetJobEducation":
        persona = "Go Getter"
        jobInterestedIn = req["queryResult"]["parameters"]["jobtitle"]
        #education = getJobEducationLevel(jobInterestedIn)
        resp_text =  f"{jobInterestedIn} requires {education}. Would you be interested to see a road map on how to get there?"
    elif intent_name == "A_GetJobEducation - yes":
        resp_text = "Great! First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_GetJobEducation - no":
        resp_text = "Okay what else can I do for you?"
    elif intent_name == "A_GetJobPath":
        persona = "Go Getter"
        jobInterestedIn = req["queryResult"]["parameters"]["jobtitle"]
        resp_text = "I can help you with that! First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_GetJobSalary":
        persona = "Go Getter"
        jobInterestedIn = req["queryResult"]["parameters"]["jobtitle"]
        #salary = getJobSalary(jobInterestedIn)
        #resp_text = f"On average, {jobInterestedIn} earns {salary} a month. Would you be interested to see a road map on how to get there?"
    elif intent_name == "A_GetJobSalary - yes":
        resp_text = "Great! First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_GetJobSalary - no":
        resp_text = "Okay what else can I do for you?"
    elif intent_name == "A_GetJobScope":
        persona = "Go Getter"
        jobInterestedIn = req["queryResult"]["parameters"]["jobtitle"]
        #jd = getJobDescription(jobInterestedIn)
        resp_text = f"Below is the job description of a {jobInterestedIn}: \n {jd}. \n Would you be interested to see a road map on how to get there?"
    elif intent_name == "A_GetJobScope - yes":
        resp_text = "Great! First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_GetJobScope - no":
        resp_text = "Okay what else can I do for you?"
    elif intent_name == "A_GetJobYears":
        persona = "Go Getter"
        jobInterestedIn = req["queryResult"]["parameters"]["jobtitle"]
        #years = getJobMinYearsExperience(jobInterestedIn)
        resp_text =  f"{jobInterestedIn} typically requires {years} years of experience. Would you be interested to see a road map on how to get there?"
    elif intent_name == "A_GetJobYears - yes":
        resp_text = "Great! First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_GetJobYears - no":
        resp_text = "Okay what else can I do for you?"

    # Persona Curious Explorer
    elif intent_name == "A_GetServicesInfo":
        persona = "Curious Explorer"
        resp_text = "I can help you develop a personalised career road map and help you look for suitable jobs and training courses. Would you like to give it a go?"
    elif intent_name == "A_GetServicesInfo - yes":
        resp_text = "Great! First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_GetServicesInfo - no":
        resp_text = "Okay what else can I do for you?"
    elif intent_name == "A_LookforCareerPath":
        persona = "Curious Explorer"
        resp_text = "I can help you develop a personalised career road map. First, I need to know what is your current position and how long you have been in it?"

    # Persona Unemployed Job Seeker
    elif intent_name == "A_LookforJob":
        persona = "Unemployed Job Seeker"
        resp_text = "I know, its tough finding a job these days. Let me help you find a suitable job! First, I need to know what was your last position and how long you had been in it?"

    # Persona Jaded Employee
    elif intent_name == "A_LookforJobChange":
        persona = "Jaded Employee"
        resp_text = "I am sorry to hear that. I think I can help you. First, I need to know what is your current position and how long you have been in it?"
    elif intent_name == "A_LookforSelfImprovement":
        persona = "Eager Learner"
        resp_text = "I am glad you are actively seeking to improve yourself. I can help you with that. First, I need to know what is your current position and how long you have been in it?"

    # elif intent_name == "ShowCareerRoadMap":
    #     if persona == "Jaded Employee" or persona == "Go Getter" or persona == "Curious Explorer":
    #         resp_text = "Now lets find out what competencies you have"
    #     elif persona == "Unemployed Job Seeker":
    #         resp_text = "This is the list of Course Recommendations"
    #     elif persona == "Eager Learner":
    #         resp_text = "This is the list of Job Recommendations"

    # elif intent_name =="GivePositionDetails":
    #     currentPosition = req["queryResult"]["parameters"]["currentPosition"]
    #     yearsOfWorkingExperience = req["queryResult"]["parameters"]["yearsOfWorkingExperience"]
    #     if persona == "Unemployed Job Seeker":
    #         resp_text = "I have a found a few potential jobs for you. To narrow the search, I would need you to select the competencies that you have."
    #     elif persona == "Jaded Employee":
    #         resp_text = "Do you have any pinnacle position in mind?"

    elif intent_name =="GiveEmailAddress":
        emailAddress = req["queryResult"]["parameters"]["emailAddress"]

    # Elicit Employment Details Intent
    elif intent_name == "D_ElicitEmployDetails":
        currentPosition = req["queryResult"]["parameters"]["job_roles"]
        yearsOfWorkingExperience = req["queryResult"]["parameters"]["duration"]

        if persona == "Jaded Employee" or persona == "Curious Explorer" or persona == "Go Getter":
            #Lead to Career Aspiration Intent
            resp_text = "D_ElicitEmployDetails:JECEGG - I have noted on your employment details. If given an opportunity, who do you aspire to be?"
        elif persona == "Unemployed Job Seeker" or persona == "Eager Learner":
            #Lead to Competencies Intent
            resp_text = "D_ElicitEmployDetails:UJS - I have noted your employment details. Next, would you share with me more about your competency?"


    # Elicit Career Preferences Intent Combined
    elif intent_name == "D_ElicitEmployDetails - no":
        resp_text = "D_ElicitEmployDetails - no - That's alright. Perhaps you can share with me if you enjoy management, technical or people roles and I can advise you a direction."
    elif intent_name == "K_GetCareerPref":
        #Get Career Preference
        careerPref = req["queryResult"]["parameters"]["career_type"]
        if careerPref == "management":
            resp_text = "I will suggest you gunning for the Managing Director. Sounds good?"
        elif careerPref == "sales":
            resp_text = "I will recommend to aim for the Sales Director. Do you think that's great?"
        elif careerPref == "technical":
            resp_text = "I will suggest you to become either a Technical Director or CTO. Yes?"
    elif intent_name == "K_GetCareerPref - yes":
        # call function and return Careerpath getCareerPath(currentPosition, careerEndGoalPosition)
        resp_text = "D_GetCareerPreferences - yes - Great to hear that. Based on the role, perhaps you can share some of your competencies with me we can check where we should be going next."
    elif intent_name == "K_GetCareerPref - no":
        resp_text = "D_GetCareerPreferences - no - That's cool. Is there any help that I can render to you?"


    # Get Aspiration Intent Combined
    elif intent_name == "D_GetAspiration":
        #Lead to D_GetAspiration - yes Intent
        careerEndGoalPosition = req["queryResult"]["parameters"]["job_roles"]
        resp_text = "D_GetAspiration - This is your career road map."
        # call function and return Careerpath getCareerPath(currentPosition, careerEndGoalPosition)
        resp_text = resp_text + "I think I can value add more in terms of career advice. Would you like to share more about your competency?"
    elif intent_name == "D_GetAspiration - yes":
        #Lead to Competency Intent
        resp_text = "D_GetAspiration - yes - Great to hear that. Based on the following list, please key in your relevant competencies."
    elif intent_name == "D_GetAspiration - no":
        resp_text = "D_GetAspiration - no - That's alright. Perhaps you can share with me if you enjoy management, technical or people roles and I can advise you a direction."

    # Elicit Competencies Intent
    elif intent_name == "Wang_elicit_comp":
        currentSkillSet = req["queryResult"]["parameters"]['skills']
        # call function and return jobs matching currentSkillSet
        resp_text = "That's a great set of skills, here are some jobs you might find interesting."
        resp_text = resp_text + "I think I can show you some courses that might help improve you skillsets too. Would you be interested to find out more?"
    # Follow up to Jobs Recommendation
    elif intent_name == "Wang_elicit_comp - yes":
        resp_text = "Here are some courses that will help improve your current standing and further your knowledge."
        # call function and return skills not matching currentSkillSet
        resp_text = resp_text + "Sign up HERE so that we can notify you when we find more jobs suitable for you!"
    elif intent_name == "Wang_elicit_comp - no":
        resp_text = "Sure no worries. Sign up HERE so that we can notify you when we find more jobs suitable for you!"

    ## cust_type intents - personas
    # jaded employee
    elif intent_name == "k_career_coach_cust_type_jaded":
        persona = "Jaded Employee"
        resp_text = "I am sorry to hear that. I think I can help you. First, tell me more about your current position and work experience."
    # guide to cust_employment_details intent

    # curious explorer
    elif intent_name == "k_career_coach_cust_type_explorer":
        persona = "Curious Explorer"
        resp_text = "The Career Road Map shows you a career path to achieve your career aspiration in the shortest time. It is generated based on anonymised data of real career advancement. Can I know more about your current employment?"
    # guide to cust_employment_details intent

    # Go Getter
    elif intent_name == "k_career_coach_cust_type_gogetter":
        persona = "Go Getter"
        resp_text = "The Career Road Map shows you a career path to achieve your career aspiration in the shortest time. It is generated based on anonymised data of real career advancement. Do you have any career aspiration?"
    # guide to cust_aspiration intent

    # The Unemployed Job Seeker
    elif intent_name == "k_career_coach_cust_type_unemployed":
        persona = "The Unemployed Job Seeker"
        resp_text = "Do not worry, we are here to help. /n Please help us to know more about your previous employment."

    # The Eager Learner
    elif intent_name == "k_career_coach_cust_type_eagerlearner_job":
        persona = "The Eager Learner"
        resp_text = "Let's work together to improve ourselves. /n Please help us to know more about your previous employment."

    # from cust_employment details intent
    elif intent_name == "k_career_coach_cust_aspiration-fallback":
        resp_text = "Help me to answer a few questions and I can suggest a career goal for you! /n"
        # trigger

    # trigger career pref
    elif intent_name == "k_career_pref_mgmt_tech_sales":
        resp_text = "Help me to answer a few questions and I can suggest a career goal for you! /n"


    # **********************
    # DialogFlow block : Start Raymond and Zilong
    # **********************

    # trigger elicit competence
    elif intent_name == "Wang_elicit_competence":
        skillset = req["queryResult"]["parameters"]
        skills = processIncomingSkillset(skillset)
        if persona == "Jaded Employee" and persona == "Go Getter":
            redirect(request, 'Level_Up_App:courserecommendresult')



    # catch all response
    else:
        resp_text = "Unable to find a matching intent. Try again."

    resp = {"fulfillmentText": resp_text}
    return JsonResponse(resp, status=200, content_type="application/json", safe=False)
    # return Response(json.dumps(resp), status=200, content_type="application/json")


   # return JsonResponse(resp, status=200, content_type="application/json", safe=False)
# return Response(json.dumps(resp), status=200, content_type="application/json")

# **********************
# DialogFlow intents : END
# **********************


# **********************
# UTIL FUNCTIONS : START
# **********************
def filtercourse(skills):
    # Declare course recommendation rules and build facts
    engine = CourseRecommender()
    engine.reset()
    engine.declare(SkillGapsFact(skills=skills))
    engine.run()
    return recommendedcourses

def filterjobs(currPos):
    jobs = list()
    currCareerPos = CareerPosition.objects.get(name=currPos)
    careerpair = JobAndNextHigherPair.objects.get(currentpos=currCareerPos)
    nextpos = getattr(careerpair, 'nextpos')
    nextCareerPos = CareerPosition.objects.get(name=nextpos)

    skillreq = getJobSkillRequired(nextCareerPos)
    return jobs

def getJobSkillRequired(jobtitle):
    skillreq = list()
    careerpos = CareerPosition.objects.get(name=jobtitle)
    filterCareerPos = CareerSkills.objects.get(careerpos=careerpos)
    for skill in filterCareerPos.skillRequired.all():
        skillreq.append(str(skill))
    return skillreq

def processIncomingSkillset(skillset):
    userSkill=list()
    for skill in skillset:
        userSkill.append(skill.upper())
    return userSkill

# **********************
# UTIL FUNCTIONS : END
# **********************
