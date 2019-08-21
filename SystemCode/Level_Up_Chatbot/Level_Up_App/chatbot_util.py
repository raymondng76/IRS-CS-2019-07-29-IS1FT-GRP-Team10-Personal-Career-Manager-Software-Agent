from django.db.models import Count
from Level_Up_App.models import CareerSkills, CareerPosition, Skill, Job, GenericInfo, CareerPathMap
from Level_Up_App.courserecommendationrules import CourseRecommender, SkillGapsFact, recommendedcourses
from Level_Up_App.jobrecommendationrules import JobRecommender, SkillSetFact, recommendedjobs
from Level_Up_App.genericjobinfo import *
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
    origialCompetenceList = elicit_competence_with_endgoal(currPos, endGoal)
    origialCompetenceList.append(userCompetence)
    return getJobRecommendation(origialCompetenceList)

def jobsrecommendation_without_endgoal(currPos, userCompetence):
    if not userCompetence:
        return list()
    origialCompetenceList = elicit_competence_without_endgoal(currPos)
    origialCompetenceList.append(userCompetence)
    return getJobRecommendation(origialCompetenceList)

def getJobRecommendation(skillset):
    engine = JobRecommender()
    engine.reset()
    engine.declare(SkillSetFact(skills=skillset))
    engine.run()
    return recommendedjobs
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

def getJobDescriptionTemp(jobtitle):
    title = jobtitle.lower()
    if title == 'intern':
        return getInternDescription()
    if title == 'engineer':
        return getEngineerDescription()
    if title == 'senior engineer':
        return getSeniorEngineerDescription()
    if title == 'software engineer':
        return getSoftwareEngineerDescription()
    if title == 'software developer':
        return getSoftwareDeveloperDescription()
    if title == 'analyst':
        return getAnalystDescription()
    if title == 'sales engineer':
        return getSalesEngineerDescription()
    if title == 'business analyst':
        return getBusinessAnalystDescription()
    if title == 'principle engineer':
        return getPrincipalEngineerDescription()
    if title == 'senior software engineer':
        return getSeniorSoftwareEngineerDescription()
    if title == 'senior software developer':
        return getSeniorSoftwareDeveloperDescription()
    if title == 'solution architect':
        return getSolutionArchitectDescription()
    if title == 'consultant':
        return getConsultantDescription()
    if title == 'senior analyst':
        return getSeniorAnalystDescription()
    if title == 'senior sales engineer':
        return getSeniorSalesEngineerDescription()
    if title == 'senior business analyst':
        return getSeniorBusinessAnalystDescription()
    if title == 'principle software engineer':
        return getPrincipalSoftwareEngineerDescription()
    if title == 'senior solution architect':
        return getSeniorSolutionArchitectDescription()
    if title == 'senior consultant':
        return getSeniorConsultantDescription()
    if title == 'technical lead':
        return getTechnicalLeadDescription()
    if title == 'project manager':
        return getProjectManagerDescription()
    if title == 'software manager':
        return getSoftwareManagerDescription()
    if title == 'sales manager':
        return getSalesManagerDescription()
    if title == 'senior project manager':
        return getSeniorProjectManagerDescription()
    if title == 'technical manager':
        return getTechnicalManagerDescription()
    if title == 'business manager':
        return getBusinessManagerDescription()
    if title == 'senior software manager':
        return getSeniorSoftwareManagerDescription()
    if title == 'senior sales manager':
        return getSeniorSalesManagerDescription()
    if title == 'senior technical manager':
        return getSeniorTechnicalManagerDescription()
    if title == 'programme manager':
        return getProgrammeManagerDescription()
    if title == 'sales director':
        return getSalesDirectorDescription()
    if title == 'professor':
        return getProfessorDescription()
    if title == 'director':
        return getDirectorDescription()
    if title == 'software director':
        return getSoftwareDirectorDescription()
    if title == 'head':
        return getHeadDescription()
    if title == 'senior sales director':
        return getSeniorSalesDirectorDescription()
    if title == 'senior director':
        return getSeniorDirectorDescription()
    if title == 'senior software director':
        return getSeniorSoftwareDirectorDescription()
    if title == 'senior head':
        return getSeniorHeadDescription()
    if title == 'chief technology officer' or title == 'cto':
        return getCTODescription()
    if title == 'vice president' or title == 'vp':
        return getVPDescription()
    if title == 'chief information officer' or title == 'cio':
        return getCIODescription()
    if title == 'president':
        return getPresidentDescription()
    if title == 'chief operating officer' or title == 'coo':
        return getCOODescription()
    if title == 'chief executive officer' or title == 'ceo':
        return getCEODescription()
