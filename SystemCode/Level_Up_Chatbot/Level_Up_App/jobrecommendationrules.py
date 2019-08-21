from pyknow import *
from Level_Up_App.models import Job, Skill, CareerPosition, CareerSkills


# def getJobSkillRequired(jobtitle):
#     careerpos = CareerPosition.objects.get(name=jobtitle)
#     careerskills = CareerSkills.objects.get(name=careerpos)
#     skillreq = list()
#     for skill in careerskill.skillRequired.all():
#         skillreq.append(str(skill))
#     return skillreq

def getMatchJob(skills):
    joblist = list()
    jobs = Job.objects.all()
    for job in jobs:
        skillreq = job.skillRequired.all()
        for skill in skillreq:
            if matchSkills(skill, skills):
                joblist.append(job)
    return joblist

def matchSkills(list1, list2):
    result = False
    for x in list1:
        for y in list2:
            if x == y:
                result = True
                return result
    return result

class SkillSetFact(Fact):
    """Fact input from derived career map"""
    pass

recommendedjobs = list()

class JobRecommender(KnowledgeEngine):
    @Rule(AS.joblisting << SkillSetFact(lambda skills: L(getMatchJob(skills))))
    def recommend(joblisting):
        """Recommend jobs"""
        global recommendedjobs
        for job in joblisting:
            recommendedjobs.append(job)
