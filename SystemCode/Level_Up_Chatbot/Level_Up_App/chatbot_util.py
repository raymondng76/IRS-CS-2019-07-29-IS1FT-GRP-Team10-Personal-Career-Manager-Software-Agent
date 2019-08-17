from Level_Up_App.models import CareerSkills, CareerPosition, Skill

def getJobCompetency(jobtitle):
    jobcompetency = []
    careerpos = CareerPosition.objects.get(name=jobtitle)
    filterCareerPos = CareerSkills.objects.get(careerpos=careerpos)
    for skill in filterCareerPos.skillRequired.all():
        jobcompetency.append(str(skill))
    return jobcompetency
