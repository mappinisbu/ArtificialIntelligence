__author__ = 'Shriya Gupta'
__author__ = 'mahathi'

import copy
import CSPAssignmentMain
import time

global course_arr
global ta_arr
global courses
global assistants

assignedTAs = []

def runbackTrack():
    # check if assignment is complete
    global assignedTAs
    isComplete = 1

    for cName in courses:
        if course_arr[cName].isAssignedTA == 0:
            notAssignedCourse = course_arr[cName]
            isComplete = 0
            break

    if isComplete:
        return 1

    # i have a not yet assigned course in
    possibletas = notAssignedCourse.possibleTAs
    possibleta = ""


    for ta in possibletas:
        if ta not in assignedTAs:
            possibleta = ta
            notAssignedCourse.assignedTAs.append(possibleta)
            notAssignedCourse.isAssignedTA = 1
            notAssignedCourse.neededTAs = notAssignedCourse.neededTAs - 0.5
            taObj = ta_arr[ta]
            taObj.assignedCourses.append(notAssignedCourse.courseName)
            assignedTAs.append(ta)

            if runbackTrack():
               return 1

            notAssignedCourse.isAssignedTA = 0
            notAssignedCourse.neededTAs = notAssignedCourse.neededTAs + 0.5
            notAssignedCourse.assignedTAs = []
            taObj = ta_arr[ta]
            taObj.assignedCourses = []
            assignedTAs.remove(ta)

    if possibleta == "":
        return 0

def backTrack(Course_arr, TA_arr, Courses, Assistants):
    global course_arr
    global ta_arr
    global courses
    global assistants

    course_arr = copy.copy(Course_arr)
    course_arr1 = copy.copy(Course_arr)
    ta_arr = copy.copy(TA_arr)
    courses = copy.copy(Courses)
    assistants = copy.copy(Assistants)

    runbackTrack()

    # Now I have all courses assigned with half TA's

    # for each course, now check if the TA is not assigned fully, among the possible TA's of that course who is free until all courses are checked
    # Revive the possible ta's section
    for cName in courses:
        course_arr[cName].possibleTAs = course_arr1[cName].possibleTAs

    for cName in courses:
        if course_arr[cName].neededTAs  == 0:
            continue
        for ta in course_arr[cName].possibleTAs:
            if course_arr[cName].neededTAs  == 0:
                break;
            taObj = ta_arr[ta]
            if taObj.assignedCourses.__len__() == 1:
                # i can assign this as half TA
                course_arr[cName].assignedTAs.append(ta)
                course_arr[cName].neededTAs = course_arr[cName].neededTAs - 0.5
                taObj.assignedCourses.append(cName)


    #for cName in courses:
    #        print("CourseName :" + str(cName) + ": TA's  : "+ str(course_arr[cName].assignedTAs) + ",  still needed :" + str(course_arr[cName].neededTAs))

    #for assistant in assistants:
    #   print(assistant + "'s assigned courses" + str(ta_arr[assistant].assignedCourses))

    print("-------------------BackTracking-----------------------")
    for assistant in assistants:
        printStr = ""
        prevAssignedCourse = ""

        if ta_arr[assistant].assignedCourses.__len__() == 0:
            continue;
        for assignedCourse in ta_arr[assistant].assignedCourses:
            if prevAssignedCourse != assignedCourse:
                printStr = printStr + "," + str(assignedCourse) + ", 0.5"
            else:
                printStr =  "," + str(assignedCourse) + ", 1"
            prevAssignedCourse = assignedCourse

        print(assistant + printStr)

    print("-------------------BackTracking---------------------")

    for cName in courses:
        needed = ""
        taString = ""

        if course_arr[cName].neededTAs > 0:
            needed = ", needed : " + str(course_arr[cName].neededTAs)

        for ta in course_arr[cName].assignedTAs:
            prevTa = ""
            if prevTa != ta:
                taString = taString + "," + str(ta) + ", 0.5"
            else:
                taString =  "," + str(ta) + ", 1"
            prevTa = ta

        print(str(cName) + taString + needed)







