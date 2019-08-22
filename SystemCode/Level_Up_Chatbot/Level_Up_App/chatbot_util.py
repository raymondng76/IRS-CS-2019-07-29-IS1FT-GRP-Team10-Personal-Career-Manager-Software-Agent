from django.db.models import Count
from Level_Up_App.models import CareerSkills, CareerPosition, Skill, Job, GenericInfo, CareerPathMap
from Level_Up_App.courserecommendationrules import CourseRecommender, SkillGapsFact, recommendedcourses
from Level_Up_App.jobrecommendationrules import getJobRecommendation
from Level_Up_App.careerknowledgegraph import *
from Level_Up_App.CareerPathASTARSearch import *


def getJobCompetency(jobtitle):
    jobcompetency = list()
    careerpos = CareerPosition.objects.get(name=jobtitle)
    filterCareerPos = CareerSkills.objects.get(careerpos=careerpos)
    for skill in filterCareerPos.skillRequired.all():
        jobcompetency.append(str(skill))
    return jobcompetency

def getHighestDemandJob():
    highest = 0
    allcareerpos = CareerPosition.objects.all()
    hdjob = allcareerpos[0].name
    for pos in allcareerpos:
        count = Job.objects.filter(name=pos).count()
        if count > highest:
            highest = count
            hdjob = pos.name
    return hdjob

def getJobEducationLevel(jobtitle):
    return str(queryGenericInfo(jobtitle).eduLvl)

def getJobSalary(jobtitle):
    return str(queryGenericInfo(jobtitle).salaryRange)

def getJobDescription(jobtitle):
    return str(queryGenericInfo(jobtitle).description)

def getJobMinYearsExperience(jobtitle):
    return str(queryGenericInfo(jobtitle).minYears)

def queryGenericInfo(jobtitle):
    careerpos = CareerPosition.objects.get(name=jobtitle)
    return GenericInfo.objects.get(title=careerpos)

def getCareerPath(currentjobtitle, aspiredjobtitle):
    cpkg = CareerPathKnowledgeGraph()
    ckm = cpkg.getCareerKnowledgeMap()
    cph = cpkg.getCareerPathHeuristic()
    return searchCareerPath(ckm, cph, currentjobtitle, aspiredjobtitle)

#****************************************
# Methods for elicit competence : START
#****************************************
def elicit_competence_with_endgoal(currPos, endGoal):
    # Get career path
    cost, careerPath = getCareerPath(currPos, endGoal)
    # Get next pos from career path
    nextpos = careerPath[1]
    # Get list of competencies to ask user
    return getListofCompetencetoAskUserWithCRoadMap(currPos, nextpos)

def elicit_competence_without_endgoal(currPos):
    return getListofCompetencetoAskUserWithoutCRoadMap(currPos)
#****************************************
# Methods for elicit competence : END
#****************************************
#****************************************
# Methods for jobs recomendation : START
#****************************************
def jobsrecommendation_with_endgoal(currPos, endGoal, userCompetence):
    if not userCompetence:
        return list()
    competenceList = elicit_competence_with_endgoal(currPos, endGoal)
    competenceList.append(userCompetence)
    return getJobRecommendation(competenceList)

def jobsrecommendation_without_endgoal(currPos, userCompetence):
    if not userCompetence:
        return list()
    competenceList = elicit_competence_without_endgoal(currPos)
    competenceList.append(userCompetence)
    return getJobRecommendation(competenceList)
#****************************************
# Methods for jobs recommendation : END
#****************************************
#*****************************************
# Methods for course recomendation : START
#*****************************************
def courserecommendation_with_endgoal(currPos, endGoal, userCompetence):
    origialCompetenceList = elicit_competence_with_endgoal(currPos, endGoal)
    if set(userCompetence) == set(origialCompetenceList):
        return list()
    remainList = [skills for skills in userCompetence if skills not in origialCompetenceList]
    return getCourseRecommendation(remainList)

def courserecommendation_without_endgoal(currPos, userCompetence):
    origialCompetenceList = elicit_competence_without_endgoal(currPos)
    if set(userCompetence) == set(origialCompetenceList):
        return list()
    remainList = [skills for skills in userCompetence if skills not in origialCompetenceList]
    return getCourseRecommendation(remainList)

def getCourseRecommendation(skillgap):
    engine = CourseRecommender()
    engine.reset()
    engine.declare(SkillGapsFact(skills=skillgap))
    engine.run()
    return recommendedcourses
#*****************************************
# Methods for course recomendation : END
#*****************************************
def getListofCompetencetoAskUserWithoutCRoadMap(currPos): # Input is a string
    currSkillList = getCareerSkillList(currPos)
    nextSkillList = getCombinedSkillReqFromNextPos(currPos)
    return [skills for skills in nextSkillList if skills not in currSkillList] # This is a list of skills to ask user

def getListofCompetencetoAskUserWithCRoadMap(currPos, nextPos): # Both input are strings
    currSkillList = getCareerSkillList(currPos)
    nextposSkillList = getCareerSkillList(nextPos)
    return [skills for skills in nextposSkillList if skills not in currSkillList] # This is a list of skills to ask user

def getCareerSkillList(pos): # Input is a string
    careerpos = CareerPosition.objects.get(name=pos)
    careerSkills = CareerSkills.objects.get(careerpos=careerpos)
    skillList = list()
    for skill in careerSkills.skillRequired.all():
        skillList.append(skill)
    return skillList # This is a list of all the skills required for this position

def getCombinedSkillReqFromNextPos(currPos): #Input is a string
    # Get combined list of next pos
    nextposlist = getCombinedListofNextPos(currPos)
    nextposskilllist = list()
    for pos in nextposlist:
        careerSkills = CareerSkills.objects.get(careerpos=pos)
        for cs in careerSkills.skillRequired.all():
            nextposskilllist.append(cs)
    return nextposskilllist # This is a list of skills

def getCombinedListofNextPos(currPos): # Input is string
    # Get career path map
    careerPathMap = getCareerPathMap(currPos)
    nextposlist = list()
    for cp in careerPathMap:
        nextposlist.append(cp.nextpos)
    return nextposlist # This is a list of all next positions available

def getCareerPathMap(currPos): # Input is string
    # Get current pos object
    currCareerPos = CareerPosition.objects.get(name=currPos)
    # Get career path map object filter by career pos object
    careerPath = CareerPathMap.objects.filter(initialpos=currCareerPos)
    return careerPath # This is a queryset of careerpath
