from django.db.models import Count
from Level_Up_App.models import CareerSkills, CareerPosition, Skill, Job, GenericInfo
from Level_Up_App.genericjobinfo import *
from Level_Up_App.careerknowledgegraph import *
from Level_Up_App.CareerPathASTARSearch import *


def getJobCompetency(jobtitle):
    jobcompetency = []
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
