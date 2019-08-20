from django.shortcuts import render, redirect, reverse
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

    # Filter course recommendation
    courses = filtercourse()

    user = request.session['username']
    result_dict = {'username': user,
                'careerendpoint': careerendpoint,
                'courses': courses,
                'jobs': jobs}
    return render(request, 'Level_Up_App/results.html', result_dict)


# ************************
# DialogFlow block : START
# ************************
# dialogflow webhook fulfillment
@csrf_exempt
def webhook(request):
        # build a request object
    req = json.loads(request.body)
    # get action from json
    action = req.get('queryResult').get('action')
    # return a fulfillment message
    if action == 'get_suggestion_chips':
        # set fulfillment text
        fulfillmentText = 'Suggestion chips Response from webhook'
        aog = actions_on_google_response()
        aog_sr = aog.simple_response([
            [fulfillmentText, fulfillmentText, False]
        ])
        #create suggestion chips
        aog_sc = aog.suggestion_chips(["suggestion1", "suggestion2"])
        ff_response = fulfillment_response()
        ff_text = ff_response.fulfillment_text(fulfillmentText)
        ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
        reply = ff_response.main_response(ff_text, ff_messages)
    else:
        reply = {'fulfillmentText': 'This is Django test response from webhook. Action or Intent not found'}
    # return generated response
    return JsonResponse(reply, safe=False)

    
# **********************
# DialogFlow block : START_KENNETH
# **********************
    ## cust_type intents - personas
    # jaded employee
    if intent_name == "k_career_coach_cust_type_jaded":
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
    


    ## employment details intents
    # from cust_type_jaded intent
    elif intent_name == "k_career_coach_cust_employment_details":
        currentPosition = req["queryResult"]["parameters"]["job_roles"]
        yearsOfWokringExperience = req["queryResult"]["parameters"]["duration"]
        if persona == "Jaded Employee":
            resp_text = "I see that you have worked as $job_roles for $duration? Do you have any career aspiration?"
        elif persona == "The Unemployed Job Seeker" or persona == "The Eager Learner":
            # elicity competency
            pass
        else:
            # show career roadmap
            pass

    ## cust_aspiration intents
    # from cust_employment_details intent
    elif intent_name == "k_career_coach_cust_aspiration_yes":
        careerEndGoalPosition = req["queryResult"]["parameters"]["job_roles"]
        if persona == "Jaded Employee" or persona == "Curious Explorer":
            resp_text = "That's great, let us see how we can explore getting to $job_roles from where you are now. This is your career roadmap."
            # show career roadmap
        elif persona == "The Eager Learner":
            resp_text = "That's great, let us see how we can explore getting to $job_roles from where you are now. This is your career roadmap."
            # show career roadmap
        elif persona == "The Unemployed Job Seeker"
            # elicit competency
    # guide to career_roadmap intent/engine

    # from cust_employment details intent
    elif intent_name == "k_career_coach_cust_aspiration-fallback":
        resp_text = "Help me to answer a few questions and I can suggest a career goal for you! /n"
        # trigger
    
    # trigger career pref 
    elif intent_name == "k_career_pref_mgmt_tech_sales":
        resp_text = "Help me to answer a few questions and I can suggest a career goal for you! /n"
    
    # catch all response
    else:
        resp_text = "Unable to find a matching intent. Try again."

    resp = {
        "fulfillmentText": resp_text
    }

    return Response(json.dumps(resp), status=200, content_type="application/json")

# **********************
# DialogFlow block : END
# **********************


# **********************
# UTIL FUNCTIONS : START
# **********************
def filtercourse():
    # skill = Skill.objects.get(name="C++") #TODO add career end point skills
    skills = list()
    skills.append('ARTIFICIAL INTELLIGENCE')
    skills.append('MACHINE LEARNING')
    skills.append('DEEP LEARNING')

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
# **********************
# UTIL FUNCTIONS : END
# **********************
