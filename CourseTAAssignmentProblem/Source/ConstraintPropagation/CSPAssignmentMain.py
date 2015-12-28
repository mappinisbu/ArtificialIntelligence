__author__ = 'Shriya Gupta'
__author__ = 'Mahathi Priya'

import sys
import ConstraintPropagation
import ForwardChecking
import BackTracking
import time

CourseArray = {}
TA_array = {}
courseNames = []
TA_Names = []


class Course:

    def __init__(self, courseName):
        self.courseName = courseName
        self.classStartTimes = []
        self.recitationStartTimes = []
        self.classDuration = 0
        self.recitationDuration = 0
        self.numberOfStudents = 0
        self.TAtoAttendClass = 0
        self.skills = []
        self.recitationRequired = 0
        self.isAssignedTA = 0
        self.assignedTAs = []
        self.assignedAllocation = []
        self.possibleTAs = []
        self.totalAssignedTAs = 0
        self.neededTAs = 0

    def setClassTimings(self, classTimings):
        self.classStartTimes = classTimings

    def setRecitationTimings(self, recitationTimings):
        self.recitationStartTimes = recitationTimings

    def setClassDuration(self, classDuration):
        self.classDuration = classDuration

    def setRecitationDuration(self, recitationDuration):
        self.recitationDuration = recitationDuration

    def setNumberOfStudents(self, numberOfStudents):
        self.numberOfStudents = numberOfStudents

    def setTAtoAttendClass(self, TAtoAttendClass):
        self.TAtoAttendClass = TAtoAttendClass

    def setSkills(self, skills):
        self.skills = skills

    def setRecitationRequired(self, recitationRequired):
        self.recitationRequired = recitationRequired

    def ISAssignedTA(self, isAssignedTA):
        self.isAssignedTA = isAssignedTA

    def setAssignedTAs(self, assignedTAs):
        self.assignedTAs = assignedTAs

    def setPossibleTAs(self, possibleTAs):
        self.possibleTAs = possibleTAs


class TA:
    def __init__(self, TAName):
        self.TAName = TAName
        self.TATimings = []
        self.TASkills = []
        self.assignedCourses = []
        self.isAssigned = 0


# The time here is minutes elapsed on a particular day
def getMinutesofTime(time):
    hourTime = 0
    if time.__contains__("AM"):
        time = time.strip('AM')
        time = time.replace(" ","")
        timelist = time.split(":")

        hourTime = int(timelist[0]) * 60
        hourTime = hourTime + int(timelist[1])

    else :
        time = time.strip('PM')
        time = time.replace(" ","")
        timelist = time.split(":")

        if int(timelist[0]) == 12:
            hourTime = 12 * 60
        else:
            hourTime =  (12 + int(timelist[0])) * 60
        hourTime = hourTime + int(timelist[1])

    return hourTime

# The minutes elapsed on a specific day of the week
def getMinutesofWeek(weekday):
    weekday = weekday.replace(" ","")
    weekMinutes = 0

    if weekday.lower() == "mon":
        weekMinutes = 0

    if weekday.lower() == "tue":
        weekMinutes = 1440

    if weekday.lower() == "wed":
        weekMinutes = 1440 * 2

    if weekday.lower() == "th":
        weekMinutes = 1440 * 3

    if weekday.lower() == "fri":
        weekMinutes = 1440 * 4

    if weekday.lower() == "sat":
        weekMinutes = 1440 * 5

    if weekday.lower() == "sun":
        weekMinutes = 1440 * 6

    return weekMinutes

def processCourseSchedule(courseShedule):
    global CourseArray
    global courseNames
    for courseType in courseShedule:
        courseName = courseType[0]
        courseNames.append(courseName)
        c = Course(courseName)
        courseStartTimes = []

        i = 1
        while i < courseType.__len__():
            weekminutes = getMinutesofWeek(courseType[i])
            i = i + 1;
            # now get the timings
            dayminutes = getMinutesofTime(courseType[i])
            totalStartTime = weekminutes + dayminutes
            courseStartTimes.append(totalStartTime)
            i = i + 1;

        c.setClassTimings(courseStartTimes)
        c.setClassDuration(80)
        CourseArray[courseType[0]] = c


def processRecitationSchedule(RecitationSchedule):
    global CourseArray
    for recitationType in RecitationSchedule:
        courseName = recitationType[0]
        #get the course from the CourseArray
        c = CourseArray[courseName]
        c.setRecitationRequired(1)
        c.setRecitationDuration(90)

        i = 1
        recitationStartTimes = []
        while i < recitationType.__len__():
            weekminutes = getMinutesofWeek(recitationType[i])
            i = i + 1;
            # now get the timings
            dayminutes = getMinutesofTime(recitationType[i])
            totalStartTime = weekminutes + dayminutes
            recitationStartTimes.append(totalStartTime)
            i = i + 1;

        c.setRecitationTimings(recitationStartTimes)


def processCourseAllocation(CourseAllocation):
    global CourseArray
    for CourseAllocationType in CourseAllocation:
        courseName = CourseAllocationType[0]
        #get the course from the CourseArray
        c = CourseArray[courseName]
        # set the number of students
        numberOfStudents = CourseAllocationType[1]
        numberOfStudents = numberOfStudents.replace(" ","")
        c.numberOfStudents = int(numberOfStudents)

        #calculate the required number of TA's for the students
        if c.numberOfStudents in range(0,40):
            c.neededTAs = 0.5

        if c.numberOfStudents in range(40,60):
            c.neededTAs = 1.5

        if c.numberOfStudents > 60:
            c.neededTAs = 2

        #set if TA has to attend classes
        isTARequiredforClass = CourseAllocationType[2]
        isTARequiredforClass = isTARequiredforClass.replace(" ","")
        if isTARequiredforClass.lower() == "yes":
            c.TAtoAttendClass = 1


def processCourseSkills(CourseSkills):
    global CourseArray
    for courseSkillType in CourseSkills:
        courseName = courseSkillType[0]
        ##get the course from the CourseArray
        c = CourseArray[courseName]

        i = 1
        courseSkillSet = []
        while i < courseSkillType.__len__():
            skill = courseSkillType[i]
            skill = skill.replace(" ","")
            courseSkillSet.append(skill)
            i = i + 1

        c.skills = courseSkillSet

def processTASchedule(TASchedule):
    global TA_array
    global TA_Names

    for TAScheduleType in TASchedule:
        taName = TAScheduleType[0]
        TA_Names.append(taName)
        t = TA(taName)

        TAClassTimes = []
        i = 1
        while i < TAScheduleType.__len__():
            weekminutes = getMinutesofWeek(TAScheduleType[i])
            i = i + 1;
            # now get the timings
            dayminutes = getMinutesofTime(TAScheduleType[i])
            totalStartTime = weekminutes + dayminutes
            TAClassTimes.append(totalStartTime)
            i = i + 1;

        t.TATimings = TAClassTimes
        TA_array[TAScheduleType[0]] = t


def processTASkills(TASkills):
    global TA_array

    for taSkillType in TASkills:
        taName = taSkillType[0]
        ##get the course from the CourseArray
        t = TA_array[taName]

        i = 1
        taSkillSet = []
        while i < taSkillType.__len__():
            skill = taSkillType[i]
            skill = skill.replace(" ","")
            taSkillSet.append(skill)
            i = i + 1

        t.TASkills = taSkillSet

def getFreeTAsForCourses():
    global CourseArray
    global TA_array
    global courseNames
    global TA_Names

    # for each course check if TA has to attend the classes
    # for each course check if recitation is required
    # make a list of all start times of classes and recitation courses.
    # for each of these start times check if TA is free

    for course in courseNames:
        startTimes = []
        possibleTAList = []
        courseSkills = []

        cObj = CourseArray[course]
        #is TA required to attend?
        if cObj.TAtoAttendClass == 1:
            for start in cObj.classStartTimes:
                startTimes.append(start)

        if cObj.recitationRequired == 1:
            for start in cObj.recitationStartTimes:
                startTimes.append(start)

        for ta in TA_Names:
            tObj = TA_array[ta]
            taStartTime = tObj.TATimings
            validTA = 1

            for classStartTime in startTimes:
                timeDiff = abs(classStartTime - taStartTime[0])
                if timeDiff <= 80:
                    validTA = 0
                    break

            if validTA == 0:
                continue; # try with another TA
            else:
                #add the TA to the possible list of TA
                #check the skills of the TA. If atleast three match add him to the list of TA's
                # if there are no skills required, add the TA directly
                courseSkills = cObj.skills
                if(courseSkills.__len__() == 0):
                    possibleTAList.append(ta)
                else:
                   matchCount = 0
                   taSkills = tObj.TASkills
                   for cskill in courseSkills:
                       for tskill in taSkills:
                           if cskill.lower() == tskill.lower():
                              matchCount = matchCount + 1

                   if matchCount > 0:
                       possibleTAList.append(ta)

        cObj.possibleTAs = possibleTAList


# Main Function of the CSP program
if __name__ == '__main__':
    global CourseArray
    global TA_array
    # Read the input file
    """ # Requirement: All tokens in the tables are separated by commas. All the tables must be provided in a single file, in the
    order given here. Tables are separated by empty line"""
    """
    Format :
    Course, timings
    #newline
    Recitation classes, timings
    #newline
    course, number of students, ta required
    #newline
    course, skills
    #newline
    ta, his class timings
    #newline
    ta, skills
    """

    if len(sys.argv):
        inputDataFile = str(sys.argv[1])
        print("Input File Provided: " + inputDataFile)

        # Read the input file
        dataFile = open(inputDataFile, 'r')
        #read line by line
        content = dataFile.readlines()

        CourseSchedule = []
        RecitationSchedule = []
        CourseAllocation = []
        CourseSkills = []
        TASchedule = []
        TASkills = []

        countNewLines = 0

        for line in content:
            if line == '\n':
                countNewLines = countNewLines + 1
                continue

            if(countNewLines == 0):
                line = line.strip('\n')
                Courseline = line.split(",")
                CourseSchedule.append(Courseline)

            if(countNewLines == 1):
                line = line.strip('\n')
                Courseline = line.split(",")
                RecitationSchedule.append(Courseline)

            if(countNewLines == 2):
                line = line.strip('\n')
                Courseline = line.split(",")
                CourseAllocation.append(Courseline)

            if(countNewLines == 3):
                line = line.strip('\n')
                Courseline = line.split(",")
                CourseSkills.append(Courseline)

            if(countNewLines == 4):
                line = line.strip('\n')
                Courseline = line.split(",")
                TASchedule.append(Courseline)

            if(countNewLines == 5):
                line = line.strip('\n')
                Courseline = line.split(",")
                TASkills.append(Courseline)

        processCourseSchedule(CourseSchedule)
        processRecitationSchedule(RecitationSchedule)
        processCourseAllocation(CourseAllocation)
        processCourseSkills(CourseSkills)
        processTASchedule(TASchedule)
        processTASkills(TASkills)

        """
        print("----------sample course Data Structure---------")
        print(CourseArray['CSE334'].classStartTimes)
        print(CourseArray['CSE334'].recitationStartTimes)
        print(CourseArray['CSE334'].classDuration)
        print(CourseArray['CSE334'].recitationDuration)
        print(CourseArray['CSE334'].numberOfStudents)
        print(CourseArray['CSE334'].TAtoAttendClass)
        print(CourseArray['CSE334'].skills)
        print(CourseArray['CSE334'].recitationRequired)
        print(CourseArray['CSE334'].isAssignedTA)
        print(CourseArray['CSE334'].assignedTAs)
        print(CourseArray['CSE334'].possibleTAs)

        print("---------Sample TA DataStructure---------")

        print(TA_array['TA33'].TAName)
        print(TA_array['TA33'].TATimings)
        print(TA_array['TA33'].TASkills)
        print(TA_array['TA33'].assignedCourses)
        print(TA_array['TA33'].assignedAllocation)
        print(TA_array['TA33'].isAssigned)"""

        # Now we have the global TA and Course datastructures and possible assignments
        # Run all algos over them

        # enforce constriant propagation through node consistency through reduced domain
        getFreeTAsForCourses()
        start_time = time.time()
        #BackTracking.backTrack(CourseArray,TA_array,courseNames,TA_Names)

        #ForwardChecking.forwardCheck(CourseArray,TA_array,courseNames,TA_Names)

        ConstraintPropagation.forwardCheckWithCP(CourseArray,TA_array,courseNames,TA_Names)
        #print("--- %s seconds ---" % (time.time() - start_time))


    else:
        print(" Input file missing. Usage:  CSPAssignmentMain.py <datafile>")

