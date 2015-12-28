__author__ = 'Shriya Gupta'
__author__ = 'mahathi'

import copy
import CSPAssignmentMain

global course_arr
global ta_arr
global courses
global assistants

def runfc():
    # check if assignment is complete

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
    if possibletas.__len__() == 0:
        return 0
    for ta in possibletas: # possible TA's is a node consistency algorithm
        notAssignedCourse.assignedTAs.append(ta)
        notAssignedCourse.isAssignedTA = 1
        notAssignedCourse.neededTAs = notAssignedCourse.neededTAs - 0.5
        taObj = ta_arr[ta]
        taObj.assignedCourses.append(notAssignedCourse.courseName)

        #remove this TA in other courses
        for cName in courses:
            if course_arr[cName].isAssignedTA == 0:
                if ta in course_arr[cName].possibleTAs:
                    course_arr[cName].possibleTAs.remove(ta)

        # check if removal of this TA does not empty the domain for others
        for cName in courses:
            if course_arr[cName].possibleTAs == 0:
                return 0

        if runfc():
            return 1

        for cName in courses:
            if course_arr[cName].isAssignedTA == 0:
                course_arr[cName].possibleTAs.append(ta)
        notAssignedCourse.isAssignedTA = 0
        notAssignedCourse.neededTAs = notAssignedCourse.neededTAs + 0.5
        notAssignedCourse.assignedTAs = []
        taObj = ta_arr[ta]
        taObj.assignedCourses = []


def forwardCheck(Course_arr, TA_arr, Courses, Assistants):
    global course_arr
    global ta_arr
    global courses
    global assistants

    course_arr = copy.copy(Course_arr)
    course_arr1 = copy.copy(Course_arr)
    ta_arr = copy.copy(TA_arr)
    courses = copy.copy(Courses)
    assistants = copy.copy(Assistants)

    runfc()

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

    print("-------------------FC-----------------------")
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

    print("-------------------FC---------------------")

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





