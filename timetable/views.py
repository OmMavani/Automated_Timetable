from django.shortcuts import render

# Create your views here.

from .models import * 
from teacher.models import *

def displayTeacher(request) : 
    teachers = Teacher.objects.all()
    if request.method == 'POST' : 
        name = request.POST['name']
        teacher = Teacher.objects.filter(name=name).first()
        slotList = Timetable.objects.filter(teacherid=teacher.teacherid)
        context = {'slotList' : slotList, 'name' : teacher.name, 'shortName' : teacher.teacherid, 'range':range(1,9)}
        return render(request, 'teacherTimetable.html', context)
    context = {'teachers' : teachers}
    return render(request, 'displayTeacher.html', context)

def displaySemester(request) : 
    teachers = Teacher.objects.all()
    if request.method == 'POST' : 
        semester = request.POST['semester']
        div = request.POST['div']
        slotList = Timetable.objects.filter(semester=semester, div=div)
        context = {'slotList' : slotList, 'name' : semester, 'shortName' : div, 'range':range(1,9)}
        return render(request, 'teacherTimetable.html', context)
    context = {'semester' : [1, 3, 5], 'div' : ['A', 'B', 'C', 'D']}
    return render(request, 'displaySemester.html', context)

def display(request) : 
    return render(request, 'display.html')


class faculty :
    lectures = []
    labs = []
    def __init__(self, name, priority, choices) :
        self.name = name
        self.priority = priority
        self.choices = choices
        self.labs = []
        self.lectures = []
        self.lecHours = 0
        self.labHours = 0

class subject :
    def __init__(self, name, classesCount, lectureCount, labCount, batchesCount) :
        self.name = name
        self.classesCount = classesCount
        self.lectureCount = lectureCount
        self.labCount = labCount
        self.classes = []
        self.labs = {}
        self.lectures = {}
        self.batchesCount = batchesCount
        if self.labCount == 0 :
            self.batchesCount = 0

    def assignClasses(self) :
        for i in range(0, self.classesCount) :
            className = self.name + chr(ord('@') + i + 1)
            self.classes.append(className)
            self.lectures[className] = ""
            for batch in range(0, self.batchesCount) :
                batchName = className + str(batch + 1)
                self.labs[batchName] = ""

    def getRemLectures(self) :
        count = 0
        for i in self.lectures :
            if self.lectures[i] == "" :
                count = count + 1
        return count

    def getRemLabs(self) :
        count = 0
        for i in self.labs :
            if self.labs[i] == "" :
                count = count + 1
        return count

class Session :
    def __init__(self, subjectName, type, duration, facultyName, division, batchNo, sessionInfo) :
        self.subjectName = subjectName;
        self.type = type;
        self.duration = duration;
        self.facultyName = facultyName;
        self.division = division;
        self.batchNo = batchNo;
        self.sessionInfo = sessionInfo;

class DNA :
    def __init__(self, sessionList) :
        self.sessionList = sessionList
        self.genes = {}
        self.fitness = 0
        self.days = 5
        self.hours = self.days * 8

        for i in range(self.hours) :
            self.genes[i] = []

        for session in sessionList :
            if session.type == 'lab' :
                choice = random.randint(0, (self.hours - 1)//2)
                choice += choice
                self.genes[choice].append(session)
                choice += 1
                self.genes[choice].append(session)
                continue
            choice = random.randint(0, self.hours - 1)
            self.genes[choice].append(session)


    def getRandom(self) :
        hr = random.randint(0, self.hours - 1)
        while len(self.genes[hr]) == 0 :
          hr = random.randint(0, self.hours - 1)
        hc = random.randint(0, len(self.genes[hr]) - 1)
        return [hr, hc]

    def calcFitness(self) :
        # no same sub lec and lab /
        # no same prof for diff session at same time /
        # it is good if you have lab in morning
        # it is also good if you have all lab of same div at same time
        # it is good if we end day at 4 -> total hours 6

        # init -> 1000 points
        # -20 for negative
        # +10 for positive

        score = 1000

        subjectCnt = {}

        for sessions in self.genes :
            subjectData = {}
            profData = {}
            divLabs = {}
            divLecs = {}

            for session in self.genes[sessions] :
                if session.subjectName not in subjectData :
                    subjectData[session.subjectName + session.division] = {}
                subjectData[session.subjectName + session.division][session.type] = 1

                if session.facultyName not in profData :
                    profData[session.facultyName] = 0;
                profData[session.facultyName] = profData[session.facultyName] + 1;

                if session.type == 'lab' :
                    mrgName = session.subjectName + session.division
                    if mrgName not in divLabs :
                        divLabs[mrgName] = 0
                    divLabs[mrgName] = divLabs[mrgName] + 1

                if session.type == 'lec' :
                    mrgName = session.division
                    if mrgName not in divLecs :
                        divLecs[mrgName] = 0
                    divLecs[mrgName] += 1

                fullName = session.subjectName + session.division
                if session.batchNo != -1 :
                    fullName += str(session.batchNo)
                if fullName not in subjectCnt :
                    subjectCnt[fullName] = 0
                subjectCnt[fullName] += 1
                # print(fullName)

            for obj in subjectData :
                count = 0
                for i in subjectData[obj] :
                    count = count + subjectData[obj][i]
                score -= (count - 1) * 10
            for obj in profData :
                count = profData[obj] - 1
                score -= count * 10
            for obj in divLabs :
                count = divLabs[obj] - 1
                # score += count * 10
            for obj in divLecs :
                count = divLecs[obj] - 1
                score -= count * 10

        absDiff = 0
        for i in subjectList :
            for j in i.lectures :
              need = i.lectureCount
              if j in subjectCnt :
                absDiff += abs(need - subjectCnt[j])
            for j in i.labs :
              need = 2
              if j in subjectCnt :
                absDiff += abs(need - subjectCnt[j])
        score -= absDiff * 10
        # print(absDiff)
        self.fitness = score


    def crossover(self, partner) :
        child = DNA(self.sessionList)
        midPoint = random.randint(0, self.days//2)
        for i in range(self.hours) :
            if i > midPoint*2 : child.genes[i] = self.genes[i]
            else : child.genes[i] = partner.genes[i]
        return child


    def mutate(self, mutationRate) :
        fate = random.random()
        if fate < mutationRate :
            # choice = random.randint(0, self.hours - 1)
            # height = len(self.genes[choice])
            # selected = []
            # rndSession = random.randint(0, len(sessionList) - 1)
            # while sessionList[rndSession].type == 'lab' :
            #     rndSession = random.randint(0, len(sessionList) - 1)
            # selected.append(sessionList[rndSession])
            # self.genes[choice] = selected

            hr1 = random.randint(0, self.hours - 1)
            # hr2 = random.randint(0, self.hours - 1)

            # while len(self.genes[hr1]) == 0 :
            #     hr1 = random.randint(0, self.hours - 1)
            # while len(self.genes[hr2]) == 0 :
            #     hr2 = random.randint(0, self.hours - 1)

            # hr1c = random.randint(0, len(self.genes[hr1]) - 1)
            # hr2c = random.randint(0, len(self.genes[hr2]) - 1)

            # e1 = self.genes[hr1][hr1c]
            # e2 = self.genes[hr2][hr2c]

            # e1, e2 = e2, e1.

            cnt = random.randint(0, self.hours - 1)
            for i in range(cnt) :
              c1 = self.getRandom()
              c2 = self.getRandom()

              e1 = self.genes[c1[0]][c1[1]]
              e2 = self.genes[c2[0]][c2[1]]

              e1, e2 = e2, e1

    def printGenes(self) :
            for i in self.genes :
                print(i)
                for session in self.genes[i] :
                    print(session.subjectName, session.division, session.type, session.batchNo, session.facultyName)

class Population :
    def __init__(self, sessionList, mutationRate, popmax) :
        self.sessionList = sessionList
        self.mutationRate = mutationRate
        self.popmax = popmax
        self.isFinished = False
        self.populationList = []
        self.matingPool = []

        for i in range(self.popmax) :
            self.populationList.append(DNA(sessionList))

    def calcFitness(self) :
        for element in self.populationList :
            element.calcFitness()

    def naturalSelection(self) :
        sumFitness = 0
        for element in self.populationList :
            sumFitness += element.fitness
        for element in self.populationList :
            fitRatio = element.fitness/sumFitness
            presence = fitRatio * 10000
            for i in range(int(presence)) :
                self.matingPool.append(element)

    def generate(self) :
        newPopulationList = []
        for element in self.populationList :
            a = random.randint(0, len(self.matingPool) - 1)
            b = random.randint(0, len(self.matingPool) - 1)
            partnerA = self.matingPool[a]
            partnerB = self.matingPool[b]
            child = partnerA.crossover(partnerB)
            child.mutate(self.mutationRate)
            newPopulationList.append(child)
        self.populationList = newPopulationList



def generate(request) : 
    facultyList = []
    subjectList = []
    subjectMap = {}

    facultyCount = 64
    subjectCount = 8

    for i in range(0, subjectCount) :
        name = "subName" + str(i)
        classesCount = 4
        lectureCount = 2 + (int(random.random()*10) % 3 == 0)
        labCount = (int(random.random()*10) % 4 != 0)
        batchesCount = 4
        obj = subject(name, classesCount, lectureCount, labCount, batchesCount)
        obj.assignClasses()
        subjectMap[name] = i;
        subjectList.append(obj)

    for i in range(0, facultyCount) :
        priority = getPriority()
        name = "name" + str(i)
        choices = random.choices(subjectList, k=10)
        facultyList.append(faculty(name, priority, choices))

    facultyList.sort(key=lambda x : -x.priority)
    for i in facultyList :
        print(i.name, i.priority)
        for j in i.choices :
            print(j.name, j.lectureCount, end=' ')

        print('\n')

    
    givenL = 0
    for i in facultyList :
        # print(i.name)
        for choice in i.choices :
            subObj = subjectList[subjectMap[choice.name]]
            remLec = subObj.getRemLectures()
            remLab = subObj.getRemLabs()
            # print(remLec, len(i.lectures), i.name)
            if remLec and subObj.lectureCount <= 5 - i.lecHours :
                for j in subObj.classes :
                    if subObj.lectures[j] == "" :
                        subObj.lectures[j] = i.name
                        i.lectures.append(j)
                        i.lecHours = i.lecHours + subObj.lectureCount
                        break
            cnt = len(subObj.classes)
            if remLab :
                for j in range(0, subObj.batchesCount) :
                    for c in subObj.classes :
                        if cnt > 0 :
                            batchName = c + str(j + 1)
                            if subObj.labs[batchName] != "" or i.labHours == 12 :
                                continue
                            subObj.labs[batchName] = i.name
                            i.labHours = i.labHours + 2
                            givenL = givenL + 2
                            i.labs.append(batchName)
                            cnt = cnt - 1

            subjectList[subjectMap[choice.name]] = subObj


    # for i in facultyList :
    #     print(i.lectures)
    # print("given labs : ", givenL)
    cnt = 0
    t = 0
    c = 0
    for i in subjectList :
        for j in i.lectures :
            if i.lectures[j] == '':
                c = c + 1
        t = t + len(i.labs)*2
        for j in i.labs :
            if i.labs[j] == "":
                cnt = cnt + 1
    print("total labs : ", t)
    print("yet to be given : ", cnt)

    given = 0
    for i in facultyList :
        given = given + len(i.labs)*2
        print("given : ", given)
        print("lec yet to be given : ", c)

        for i in subjectList :
            for j in i.lectures :
                if i.lectures[j] == '' :
                    for f in facultyList :
                        remLecHours = 5 - f.lecHours
                        if i.lectureCount <= remLecHours :
                            print(remLecHours, i.lectureCount)
                            f.lecHours = f.lecHours + i.letureCount
                            f.lectures.append(i.name)
                            i.lectures[j] = f.name

    totalLabs = 0
    for i in subjectList :
        totalLabs = totalLabs + len(i.labs)*2
        for j in i.labs :
            if i.labs[j] == '' :
                for f in facultyList :
                    if f.labHours < 12:
                        f.labHours = f.labHours + 2
                        f.labs.append(i.name)
                        i.labs[j] = f.name
    # print("totalLabs : ", totalLabs)

    # given = 0
    # for i in facultyList :x
    #     # print(i.name, i.labs)
    #     given = given + len(i.labs)*2
    # print("given : ", given)

    cnt = 0
    c = 0
    for i in subjectList :
        print(i.lectures)
        for j in i.lectures :
            if i.lectures[j] == '':
                c = c + 1
        for j in i.labs :
            if i.labs[j] == '':
                cnt = cnt + 1

    for i in subjectList :
        print(i.name, i.lectures, i.labs)

    for i in facultyList :
        print(i.lectures)
    for i in facultyList :
        print(i.labs)

    print("lab yet to be given : ", cnt)
    print("lec yet to be given : ", c)


    # for f in facultyList :
    #     print(f.lecHours)
    sessionList = []
    for sub in subjectList :
        for i in range(sub.classesCount) :
            subName = sub.name +  getChar(i)
            facultyName = sub.lectures[subName]
            sessionInfo = subName + " " + facultyName
            for j in range(sub.lectureCount) :
                sessionList.append(Session(sub.name, 'lec', 1, facultyName, getChar(i), -1, sessionInfo))
            for j in range(sub.batchesCount) :
                batchName = subName + str(j + 1)
                facultyName = sub.labs[batchName]
                sessionInfo = batchName + " " + facultyName
                # sessionList.append(Session(sub.name, 'lab', 2, facultyName, getChar(i), j+1, sessionInfo))


    for session in sessionList :
        print(session.subjectName, session.division, session.type, session.batchNo, session.facultyName)
    
    N = 5000
    mutationRate = 0.4
    popmax = 3000

    mx = DNA(sessionList)
    maxFit = 0
    minFit = 1000
    step = 0

    p = Population(sessionList, mutationRate, popmax)
    for i in range(N) :
        p.calcFitness()
        greaterThan800 = 0
        for ii in p.populationList :
            if ii.fitness > maxFit :
                maxFit = ii.fitness
                mx = ii
            if ii.fitness > 800 :
                greaterThan800 += 1
            if ii.fitness < minFit :
                minFit = ii.fitness
        step += 1
        print(step,maxFit, minFit, greaterThan800, len(p.populationList))
        p.naturalSelection()
        p.generate()
    
    print(mx.fitness)
    for i in mx.genes :
        print(i)
        sessionList = mx.genes[i]
        for session in sessionList :
            print(session.subjectName, session.division, session.type, session.batchNo, session.facultyName)

    # for session in sessionList : 
    #     obj = Timetable(session)
    #     obj.save()

    return render(request, 'display.html')