import numpy as np

class Simplex:
    def __init__(self, limitationCoeff=np.empty([0, 0]), limits=np.empty([0, 0]), funcCoeff=np.empty([0, 0]), minmax='MAX'):
        self.limitationCoeff = limitationCoeff
        self.limits = limits
        self.funcCoeff = funcCoeff
        self.result = [float(0)] * len(funcCoeff)
        self.minmax = minmax
        self.counterFlag = True
        self.zOPT = None
        self.transform = False

    def setLimitationCoeff(self, limitationCoeff):
        self.limitationCoeff = limitationCoeff

    def setLimits(self, limits):
        self.limits = limits

    def setFuncCoeff(self, funcCoeff):
        self.funcCoeff = funcCoeff
        self.transform = False

    def setFunc(self, minmax):
        if (minmax == 'MIN' or minmax == 'MAX'):
            self.minmax = minmax
        else:
            print('error')
        self.transform = False

    def setcounterFlag(self, counterFlag):
        self.counterFlag = counterFlag

    def show(self):
        print('x1, x2: ')
        print(self.result)
        print('z opt: ')
        print(self.zOPT)

    def printTable(self, tmpTable):
        space = ' '
        for j in range(0, len(funcCoeff)):
            print('x' + str(j + 1) + space * 5, end='\t')
        for j in range(0, (len(tmpTable[0]) - len(funcCoeff) - 2)):
            print('s' + str(j + 1) + space * 5, end='\t')

        print()
        for j in range(0, len(tmpTable)):
            for i in range(0, len(tmpTable[0])):
                if (not np.isnan(tmpTable[j, i])):
                    if (i == 0):
                        print('|', end='\t')
                    else:
                        print(round(tmpTable[j, i], 2), space * 5 + '|', end='\t')
                else:
                    print(end='\t')
            print()

    def getTmpTable(self):
        if (self.minmax == 'MIN' and self.transform == False):
            self.funcCoeff[0:len(funcCoeff)] = -1 * self.funcCoeff[0:len(funcCoeff)]
            self.transform = True

        t1 = np.array([None, 0])
        numVar = len(self.funcCoeff)
        numSlack = len(self.limitationCoeff)

        t1 = np.hstack(([None], [0], self.funcCoeff, [0] * numSlack))
        basis = np.array([0] * numSlack)

        for i in range(0, len(basis)):
            basis[i] = numVar + i

        limitationCoeff = self.limitationCoeff

        if (not ((numSlack + numVar) == len(self.limitationCoeff[0]))):
            B = np.identity(numSlack)
            limitationCoeff = np.hstack((self.limitationCoeff, B))

        t2 = np.hstack((np.transpose([basis]), np.transpose([self.limits]), limitationCoeff))

        tmpTable = np.vstack((t1, t2))

        tmpTable = np.array(tmpTable, dtype='float')

        return tmpTable

    def optimize(self):
        if (self.minmax == 'MIN' and self.transform == False):
            for i in range(len(self.c)):
                self.c[i] = -1 * self.c[i]
                transform = True

        tmpTable = self.getTmpTable()

        if (self.counterFlag == True):
            self.printTable(tmpTable)

        optimal = False
        counter = 1

        while (True):
            if (self.counterFlag == True):
                print('current iteration :', counter)
                self.printTable(tmpTable)

            if (self.minmax == 'MAX'):
                for profit in tmpTable[0, 2:]:
                    if profit > 0:
                        optimal = False
                        break
                    optimal = True
            else:
                for cost in tmpTable[0, 2:]:
                    if cost < 0:
                        optimal = False
                        break
                    optimal = True
            if optimal == True:
                break

            if (self.minmax == 'MAX'):
                mainColumn = tmpTable[0, 2:].tolist().index(np.amax(tmpTable[0, 2:])) + 2
            else:
                mainColumn = tmpTable[0, 2:].tolist().index(np.amin(tmpTable[0, 2:])) + 2

            minimum = 99999
            mainRow = -1

            for i in range(1, len(tmpTable)):
                if (tmpTable[i, mainColumn] > 0):
                    val = tmpTable[i, 1] / tmpTable[i, mainColumn]
                    if val < minimum:
                        minimum = val
                        mainRow = i

            mainElement = tmpTable[mainRow, mainColumn]

            print('main column:', mainColumn)
            print('main row:', mainRow)
            print('main element: ', mainElement)

            tmpTable[mainRow, 1:] = tmpTable[mainRow, 1:] / mainElement

            for i in range(0, len(tmpTable)):
                if i != mainRow:
                    mult = tmpTable[i, mainColumn] / tmpTable[mainRow, mainColumn]
                    tmpTable[i, 1:] = tmpTable[i, 1:] - mult * tmpTable[mainRow, 1:]

            tmpTable[mainRow, 0] = mainColumn - 2

            counter += 1

        if (self.counterFlag == True):
            print('final result:', counter, 'iterations')
            self.printTable(tmpTable)

        self.result = np.array([0] * len(funcCoeff), dtype=float)
        for key in range(1, (len(tmpTable))):
            if (tmpTable[key, 0] < len(funcCoeff)):
                self.result[int(tmpTable[key, 0])] = tmpTable[key, 1]

        self.zOPT = -1 * tmpTable[0, 1]

simplex = Simplex()

"""

limitationCoeff = np.array([[-5, 9],
              [9, 4]])
limits = np.array([36, 117])
funcCoeff = np.array([8, 1])

"""

limitationCoeff = np.array([[-3, 1],
             [2, 1],
              [2, -6]])
limits = np.array([3, 8, 4])
funcCoeff = np.array([5, 6])



def run():
    simplex.setLimitationCoeff(limitationCoeff)
    simplex.setLimits(limits)
    simplex.setFuncCoeff(funcCoeff)
    simplex.setFunc('MAX')
    simplex.optimize()
    simplex.show()
