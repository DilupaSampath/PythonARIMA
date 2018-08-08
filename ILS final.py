from pandas import read_csv
import random
import copy
import math
from numpy import around


class NursesPerWard(object):
    def __init__(self,ward,nursesPerWard):
        self.ward=ward
        self.nursesPerWard=nursesPerWard

def initialSolution(nurses,wards):
    nurseArr = nurses.values
    wardArr = wards.values
    #print(wardArr[0][0])
    nurseCount = len(nurseArr)
    wardCount = len(wardArr[0])
    wardList = list(wards)
    wardsWithNurses = list()
    nurseList = nurseArr.tolist()   
    totPatientCount = 0
    for i in wardArr[0]:
        totPatientCount = totPatientCount + i
    patientPerNurse = math.ceil(totPatientCount/nurseCount)     
    for i in range(wardCount):
        if(i==(wardCount-1)):
            wardnursesPerWard.append(NursesPerWard(wardList[i],nurseCount))                       
        else:
            nurPerWard = math.floor(wardArr[0][i]/patientPerNurse)                       
            wardnursesPerWard.append(NursesPerWard(wardList[i],nurPerWard))
            nurseCount = nurseCount - nurPerWard            
    def assignNursesToWards(listDetails):
        for a in range(0, len(wardnursesPerWard)): 
            ranArrLength=int(wardnursesPerWard[a].nursesPerWard)     
           # wardAllocation = list() no need
            randomNurArr1 = list()
            randoms = range(0,len(nurseList))
            randomNurses = random.sample(randoms,ranArrLength)            
            for x in range (0,ranArrLength):       
                randomIndex = randomNurses[x]
                if(randomIndex >= len(nurseList)):
                    randomIndex = len(nurseList) - 1
                randomNurArr1.append(nurseList.pop(randomIndex))                 
            #wardAllocation.append(randomNurArr1) no need
            wardsWithNurses.append(randomNurArr1)           
        return wardsWithNurses
    assignNursesToWards(wardnursesPerWard)             
    return wardsWithNurses


def calculateFitnessScore(solution):
    fs1 = 0
    fs2 = 0
    fitnessScore = 0
    NurseArr = list()
    for ward in range(0,len(solution)):
        
        for a in range(0,len(solution[ward])):
            if (solution[ward][a][1] == 'Allowed'):
                fs1 = fs1 + 0
            elif (solution[ward][a][1] == 'OT' and ward==0):
                fs1 = fs1 + 2
            else:
                fs1 = fs1 + 1
            
        x = len(solution[ward])
        NurseArr.append(x)
    PPN = wardArr / NurseArr
    patientPerNurse = around(PPN)
    for val in range(0,len(patientPerNurse[0])):
        if (patientPerNurse[0][val] == 8):
            fs2 = fs2+0
        elif (patientPerNurse[0][val] == 7):
            fs2 = fs2 +2
        elif (patientPerNurse[0][val] == 6):
            fs2 = fs2 +3
        elif (patientPerNurse[0][val] == 5):
            fs2 = fs2 +4
        elif (patientPerNurse[0][val] == 4):
            fs2 = fs2 +5
        elif (patientPerNurse[0][val] == 3):
            fs2 = fs2 +6
        elif (patientPerNurse[0][val] == 2):
            fs2 = fs2 +10
        elif (patientPerNurse[0][val] == 1):
            fs2 = fs2 +15
        else:
            fs2 = fs2 +20
    fitnessScore = fs1+fs2
        
    return fitnessScore

def changeSolution(initialSolutionCpy):
    global removeFromMain # is their to identify "WARD" the nurse which is going to be change from the initial solution 
    global removeFrom # the ward that the removing nurse belongs to  
    global mainSwapCount
    global swapCount
    global appendTo # the ward that the removing is going to newly add
    global initialSolution 
    global movingNurse # nurse that is to be moved
    global resetInitialCount
    global status
    global wardCount
    returnSolution = list()
    if resetInitialCount == (wardCount-1):
        initialSolutionCpy = copy.deepcopy(initialSolution)
        resetInitialCount = 0
    if(removeFromMain == wardCount-1 and mainSwapCount == len(initialSolution[removeFromMain])):
        returnSolution = "No more matches left"
        status = False
    else:
        movingNurse = initialSolution[removeFromMain][mainSwapCount]
        if(appendTo == removeFromMain):
            appendTo = appendTo +1
        else:
            if(appendTo==len(initialSolutionCpy)):
                appendTo = 0
            #print(initialSolutionCpy)
            initialSolutionCpy[removeFrom].remove(movingNurse)
            initialSolutionCpy[appendTo].append(movingNurse)
            returnSolution = copy.deepcopy(initialSolutionCpy)
            removeFrom = appendTo
            appendTo = appendTo + 1
            swapCount = swapCount+1
            resetInitialCount = resetInitialCount+1
            if(appendTo == wardCount):
                appendTo = 0
            if(swapCount==(wardCount-1)):
                mainSwapCount = mainSwapCount+1
                removeFrom = removeFromMain
                if(removeFrom == appendTo):
                    appendTo = appendTo+1
                swapCount = 0
                if(mainSwapCount == len(initialSolution[removeFromMain])):
                    if(removeFromMain == len(initialSolutionCpy)-1):
                        initialSolutionCpy = "No more matches left"
                        status = False
                    else:
                        mainSwapCount=0
                        removeFromMain = removeFromMain+1
                        removeFrom = removeFromMain
                        if(removeFrom == appendTo):
                            appendTo = 0
    return returnSolution

#read files
nurses1 = read_csv("nurses.csv",header=0)
wards2  = read_csv("wards.csv",header=0)
wardnursesPerWard=[]
nurseArr = nurses1.values
wardArr = wards2.values
nurseCount = len(nurseArr)
wardCount = len(wardArr[0]) 
bestSolution = list() 
solutionList = list() # to chck whether we are calculating the fitness score to the same solution 
bestSolutionList = list()

initialSolution = initialSolution(nurses1,wards2) 
# =============================================================================
# [
#     [
#         ['nurse6', 'Allowed'],
#         ['nurse13', 'Allowed']
#     ],
#     [
#         ['nurse19', 'OT'],
#         ['nurse7', 'Allowed'],
#         ['nurse15', 'OT'],
#         ['nurse18', 'OT'],
#         ['nurse16', 'OT'],
#         ['nurse8', 'Allowed'],
#         ['nurse5', 'Allowed'],
#         ['nurse20', 'OT'],
#         ['nurse14', 'OT'],
#         ['nurse11', 'Allowed'],
#         ['nurse4', 'Allowed']
#     ],
#     [
#         ['nurse12', 'OT'],
#         ['nurse17', 'OT'],
#         ['nurse1', 'OT'],
#         ['nurse3', 'Allowed'],
#         ['nurse2', 'Allowed'],
#         ['nurse9', 'Allowed'],
#         ['nurse10', 'OT']
#     ]
# ]
# =============================================================================
solutionList.append(initialSolution)
#set initial solution as the best solution at the begining
bestSolution = copy.deepcopy(initialSolution)
bestFitnessScore = calculateFitnessScore(initialSolution)

#get a copy of initialsolution. The copy is going to be changed sequentially
initialSolutionCpy1 = copy.deepcopy(initialSolution)

#Set parameters which are going to be used when changing the solution
movingNurse = initialSolutionCpy1[0][0]
removeFromMain = 0
removeFrom = 0
mainSwapCount = 0
swapCount = 0
appendTo = 1
resetInitialCount = 0 # same as swapcount
status = True

while (status == True):
    backUpList = copy.deepcopy(initialSolutionCpy1)
    initialSolutionCpy1 = changeSolution(initialSolutionCpy1)
    #print(initialSolutionCpy1)
    #checks whether it is empty 
    if not initialSolutionCpy1:
        initialSolutionCpy1 = copy.deepcopy(backUpList)
    if initialSolutionCpy1 not in solutionList:
        tempFitnessScore = calculateFitnessScore(initialSolutionCpy1)
        print(tempFitnessScore)
        if(tempFitnessScore < bestFitnessScore):
            bestFitnessScore = tempFitnessScore
            bestSolution = copy.deepcopy(initialSolutionCpy1)
            #Sprint("best solution = %s"%bestSolution)
        elif (tempFitnessScore == bestFitnessScore):
            bestSolutionList.append(initialSolutionCpy1)
            #print(bestSolutionList)
        else:
            continue
        solutionList.append(initialSolutionCpy1)
    else:
        continue
    if status == False:
        print(initialSolutionCpy1)

if len(bestSolutionList)>1:
    print("There are more than 1 best solutions")
    bestSolution = random.choice(bestSolutionList)

print("initial solution")
print(initialSolution)
print("============================================================================")    
print("best fitness score = %s"%bestFitnessScore)
print("best solution")
print(bestSolution)
print(status)