import random as r
import math


def generateEquation(difficulty=1):

    global operator

    value1 = r.randrange(int(math.pow(difficulty, 2)), 10 * difficulty + int(math.pow(difficulty, 2)))
    value2 = r.randrange(int(math.pow(difficulty, 2)), 10 * difficulty + int(math.pow(difficulty, 2)))

    if difficulty < 2:
        operator = "+"
    elif difficulty <= 4:
        operator = r.choice(["+", "-"])
    elif difficulty > 4:
        operator = r.choice(["+", "-", ])

    eqnString = "{} {} {}".format(value1, operator, value2)
    finalDict = {eqnString: int(eval(eqnString))}
    return finalDict


def generateEquationList(size, difficulty=1):

    eqnList = []

    if size > 0 and difficulty >= 1:
        for i in range(size):
            eqnList.append(generateEquation(difficulty))
        return eqnList
    else:
        raise ValueError


def formatEquationList(eqnlist):

    formattedEqnList = "List of {} equations:\n\n".format(len(eqnlist))

    for equation in eqnlist:
        formattedEqnList += str(equation.keys())[12:-3] + " = " + str(equation.values())[13:-2] + "\n"
    return formattedEqnList


def quizFromEqnList(eqnlist):

    amntCorrect = 0
    qCount = 1

    for eqn in eqnlist:
        ans = input("Question {}/{}: ".format(qCount, len(eqnlist)) + str(eqn.keys())[12:-3] + " = ")
        if ans == str(eqn.values())[13:-2]:
            print("\tCorrect!")
            amntCorrect += 1
        else:
            print("\tIncorrect (Correct answer: {})".format(str(eqn.values())[13:-2]))
        qCount += 1

    print("\nTotal Score: {}/{} ({}%)".format(amntCorrect, len(eqnlist), int(100 * (amntCorrect / len(eqnlist)))))

#print(generateEquationList(3, 4))   # <----- The list of question/answer tuples, for connecting with GUI
quizFromEqnList(generateEquationList(3, 4))    # <----- Text only output test
