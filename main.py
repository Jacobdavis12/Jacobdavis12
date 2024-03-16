# -*- coding: utf-8 -*-
"""
Created on Wed May 11 23:43:51 2022

@author: jacob
"""


# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
import numpy as np
from PIL import Image


app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        return do_POST()
    else:
        return do_GET()

html = ['<html><head><title>Sudoku solver</title><style>',
            '</style><script type="text/javascript">function openTab(tab) { document.getElementById("tab1").className = "buttons tab"; document.getElementById("tab2").className = "buttons tab"; document.getElementById("tab3").className = "buttons tab"; document.getElementById("content1").style.display = "none"; document.getElementById("content2").style.display = "none"; document.getElementById("content3").style.display = "none"; document.getElementById("tab" + String(tab)).className += " tabOpen"; document.getElementById("content" + String(tab)).style.display = "block"; }; function updatePrefs() { for (var i = 0; i < 3; i++) { if (document.getElementsByClassName("taskInput")[i].checked) { for (var j = 0; j < 3; j++) { document.getElementsByClassName("taskHiddenInput")[j].setAttribute("value", document.getElementsByClassName("taskInput")[i].getAttribute("value")); }; }; }; }; function sumbitSudoku() { updatePrefs(); sudoku.submit(); }; function submitVersion() { updatePrefs(); for (var i = 0; i < 3; i++) { if (document.getElementsByClassName("versionInput")[i].checked) { for (var j = 0; j < 3; j++) { document.getElementsByClassName("versionHiddenInput")[j].setAttribute("value", document.getElementsByClassName("versionInput")[i].getAttribute("value")); }; }; }; version.submit(); }; function submitUpload() { updatePrefs(); upload.submit(); };</script> </head><body><h1 id="header">Sudoku solver</h1><div id="content"><form id="sudoku" method="post"> <input name="type" class="hiddenInputs" value="sudoku"></input> <input name="version" class="hiddenInputs versionHiddenInput" value="',
            '"></input> <input name="task" class="hiddenInputs taskHiddenInput"></input>',
            '</form><div id="controls"> <label for="image" class="control buttons"> Upload Sudoku image<form id = "upload" method="post" enctype="multipart/form-data"> <input name="type" class="hiddenInputs" value="image"></input> <input name="version" class="hiddenInputs versionHiddenInput" value="',
            '"></input> <input name="task" class="hiddenInputs taskHiddenInput"></input> <input id="image" type="file" name="filename" onchange="submitUpload()"></form> </label> <label id="prefernceControl" class="control" for="photo"><div id="tabs"><div id="tab0"> Preferences</div><div id="tab1" class="buttons tab tabOpen" onclick="openTab(1)"> Menu</div><div id="tab2" class="buttons tab" onclick="openTab(2)"> Version</div><div id="tab3" class="buttons tab" onclick="openTab(3)">Task</div></div><div id="content1" class="content">',
            '</br><a href="/static/Documentation.pdf">Documentation</a></div><div id="content2" class="content"><form id="version" method="post"> <label for="version">Version: </label></br> <input class="versionInput" type="radio" id="99standard" name="version" value="99standard"',
            '> <label for="99standard">Standard 9x9</label></br> <input class="versionInput" type="radio" id="sudokuX" name="version" value="sudokuX"',
            '> <label for="sudokuX">sudokuX 9x9</label></br> <input class="versionInput" type="radio" id="44standard" name="version" value="44standard"',
            '> <label for="44standard">Standard 4x4</label></br> <input name="type" class="hiddenInputs" value="version"></input> <input name="version" class="hiddenInputs versionHiddenInput" value="',
            '"></input> <input name="task" class="hiddenInputs taskHiddenInput"></input> <button type="button" onclick="submitVersion()">Submit</button></form></div><div id="content3" class="content"> <label for="task">Task: </label></br> <input class="taskInput" type="radio" id="solve" name="task" value="solve"',
            '> <label for="solve">Solve sudoku</label></br> <input class="taskInput" type="radio" id="hint" name="task" value="hint"',
            '> <label for="hint">Provide hint</label></br> <input class="taskInput" type="radio" id="check" name="task" value="check"',
            '> <label for="check">Check sudoku</label></br></div> </label> <label class="control buttons" onclick="sumbitSudoku()"> Solve Sudoku </label></div></div></body></html>',]

style = '.buttons{cursor:pointer}#header{font-size:10vh;height:10vh;margin:0}#content{display:flex;flex-wrap:wrap}#sudoku{height:80vh;width:80vh;display:grid;grid-template-columns:squarePlaceHolderVhTimes;grid-gap:1vh;background-color:#000;border:solid #ccc 1vh;float:left}.square{position:relative;height:100%;width:100%;display:grid;grid-template-columns:cellPlaceHolderVhTimes;grid-gap:1vh;background-color:silver}.cell{font-size:cellPlaceHolderVh;height:cellPlaceHolderVh;text-align:center;background-color:#fff;border:0}#image,.hiddenInputs{display:none}.control{background-color:#004080;border-radius:5px;border:1px solid #004080;color:#fff}#controls{flex-grow:100;display:grid;grid-template-rows:26vh 26vh 26vh;grid-gap:1vh;white-space:nowrap;font-size:6vh;padding:1vh 0 0 1vh}#controls>.control{height:26vh;width:100%}.tab{width:25%;background-color:ccc}#tab0{width:25%;background-color:#004080}#tabs{width:100%;display:flex;background-color:ccc}.tabOpen{background-color:#fff;color:#000}.content{background-color:#fff;color:#000;display:none;font-size:3vh}#content1{display:block}.diagonal{background-color: beige;}.incorrectCell{background-color: red;}.incorrectSet{background-color: lightpink;}.hintCell{background-color: green;}.hintSet{background-color: lightgreen;}@media screen and (orientation:portrait){#header{font-size:10vw;height:10vw}#sudoku{height:80vw;width:80vw;grid-template-columns:squarePlaceHolderVwTimes;grid-gap:1vw;border-width:1vw}.square{grid-template-columns:cellPlaceHolderVwTimes;grid-gap:1vw}.cell{font-size:cellPlaceHolderVw;height:cellPlaceHolderVw}#controls{padding-left:0;font-size:6vw;height:6vw;grid-template-rows:26vw 26vw 26vw;grid-gap:1vw;padding:1vw 0 0 1vw}#controls>.control{height:26vw}.content{font-size:3vw}}'

def makeSudoku(version, params, extraClasses, opacity):
    sudokuHtml = ''
    if version == '99standard':
        sudokuHtml = makeSudokuHtml(9, version, params, extraClasses, opacity)

    elif version == 'sudokuX':
        for i in ['00', '04', '08', '40', '44', '48', '80', '84', '88', '22', '24', '26', '42', '44', '46', '62', '64', '66']:
            if i in extraClasses:
                extraClasses[i] += ' diagonal'
            else:
                extraClasses[i] = 'diagonal'
            sudokuHtml = makeSudokuHtml(9, version, params, extraClasses, opacity)

    elif version == '44standard':
         sudokuHtml = makeSudokuHtml(4, version, params, extraClasses, opacity)

    else:
       input('error makeSudoku')

    return sudokuHtml

def makeSudokuHtml(size, version, params, extraClasses, opacity):
    sudokuHtml = ''
    for s in range(size):
        sudokuHtml += '<div id="s' + str(s) + '" class="square">\n'
        for c in range(size):
            if str(s) + str(c) in params:
                sudokuHtml += '<input type="text" size="1" maxlength="1" name="' + str(s) + str(c) + '" value="' + params[str(s) + str(c)] + '" class="cell'
            else:
                sudokuHtml += '<input type="text" size="1" maxlength="1" name="' + str(s) + str(c) + '" value="" class="cell'

            if str(s) + str(c) in extraClasses:
                sudokuHtml += ' ' + extraClasses[str(s) + str(c)]

            sudokuHtml += '" style="'
            if str(s) + str(c) in opacity:
                sudokuHtml += 'color: rgba(0, 0, 0, ' + str(opacity[str(s) + str(c)]) + ');'

            sudokuHtml += '">\n'

        sudokuHtml += '</div>\n'

    return sudokuHtml

def applyStylePlaceHolders(squareAmount, cellAmount):
        squareSize = (81 - squareAmount)/squareAmount
        cellSize = (squareSize + 1 - cellAmount)/cellAmount

        squarePlaceHolderVhTimes = (str(squareSize) + 'vh ')*squareAmount
        squarePlaceHolderVwTimes = (str(squareSize) + 'vw ')*squareAmount
        cellPlaceHolderVh = (str(cellSize) + 'vh ')
        cellPlaceHolderVw = (str(cellSize) + 'vw ')
        cellPlaceHolderVhTimes = cellPlaceHolderVh*cellAmount
        cellPlaceHolderVwTimes = cellPlaceHolderVw*cellAmount

        return style.replace('squarePlaceHolderVhTimes', squarePlaceHolderVhTimes).replace('squarePlaceHolderVwTimes', squarePlaceHolderVwTimes).replace('cellPlaceHolderVhTimes', cellPlaceHolderVhTimes).replace('cellPlaceHolderVwTimes', cellPlaceHolderVwTimes).replace('cellPlaceHolderVh', cellPlaceHolderVh).replace('cellPlaceHolderVw', cellPlaceHolderVw)

def makeStyle(version):
    if version == '99standard':
        versionStyle = applyStylePlaceHolders(3, 3)
    elif version == 'sudokuX':
        versionStyle = applyStylePlaceHolders(3, 3)
    elif version == '44standard':
        versionStyle = applyStylePlaceHolders(2, 2)
    else:
       input('error makeStyle')

    return versionStyle

def do_GET(message = ['Enter your sudoku by uploading an image or type directly into the sudoku.', 'Press solve sudoku when ready to.'], version = '99standard', task = 'solve', params = {}, extraClasses = {}, opacity = {}):
    index = html[0]
    index += makeStyle(version)
    index += html[1]
    index += version
    index += html[2]
    index += makeSudoku(version, params, extraClasses, opacity)
    index += html[3]
    index += version
    index += html[4]
    index += '</br>'.join(message)
    index += html[5]

    if version == '99standard':
        index += 'checked="checked"'
    index += html[6]
    if version == 'xSudoku':
        index += 'checked="checked"'
    index += html[7]
    if version == '44standard':
        index += 'checked="checked"'

    index += html[8]
    index += version
    index += html[9]

    if task == 'solve':
        index += 'checked="checked"'
    index += html[10]
    if task == 'hint':
        index += 'checked="checked"'
    index += html[11]
    if task == 'check':
        index += 'checked="checked"'

    index += html[12]

    return index

def do_POST():
    extraClasses = {}
    if verbose:
        print(request.form)

    if request.form['type'] == 'image':
        img = Image.open(request.files['filename'].stream)
        if verbose:
            img.save('file.jpg')
        imageInput = sudokuImage(img)
        imageInput.recognise()
        return do_GET(['Sudoku recognised successfully'], request.form['version'], request.form['task'], imageInput.getValues(), {}, imageInput.getConfidences())
    elif request.form['type'] == 'sudoku':
        if request.form['version'] == '99standard':
            sudokuInput = sudoku(request.form, 3, 3, 3, 3)
        elif request.form['version'] == 'sudokuX':
            sudokuInput = sudokuX(request.form)
        elif request.form['version'] == '44standard':
            sudokuInput = sudoku(request.form, 2, 2, 2, 2)


        if request.form['task'] == 'solve':
            sudokuInput.solve()
            if sudokuInput.getNoOfSolutions() > 300:
                return do_GET(['Sudoku has over 300 different solutions!'], request.form['version'], request.form['task'], sudokuInput.getValues())
            else:
                return do_GET(['Sudoku has ' + str(sudokuInput.getNoOfSolutions()) + ' solution(s)'], request.form['version'], request.form['task'], sudokuInput.getValues())

        elif request.form['task'] == 'hint':
            hint = sudokuInput.getHint()
            if verbose:
                print(hint)
            if hint != "unsolvable" and hint != "complete":
                extraClasses = {}
                for pointer in hint[1]:
                    x, y = sudokuInput.squareToRowIndividual(pointer[0], pointer[1])
                    extraClasses[str(x) + str(y)] = 'hintSet'

                x, y = sudokuInput.squareToRowIndividual(hint[0][0], hint[0][1])
                extraClasses[str(x) + str(y)] = 'hintCell'
                if sudokuInput.getNoOfSolutions() > 300:
                    return do_GET(['Sudoku has over 300 different solutions!'], request.form['version'], request.form['task'], request.form, extraClasses)
                else:
                    return do_GET(['Sudoku has ' + str(sudokuInput.getNoOfSolutions()) + 'solution(s)'], request.form['version'], request.form['task'], request.form, extraClasses)
            elif hint == "unsolvable":
                return do_GET(['Sudoku has 0 solutions'], request.form['version'], request.form['task'], sudokuInput.getValues())
            elif hint == "complete":
                return do_GET(['Sudoku is already complete'], request.form['version'], request.form['task'], sudokuInput.getValues())

        elif request.form['task'] == 'check':
            result = sudokuInput.checkSudoku()
            if result == True:
                return do_GET(['Sudoku is currently correct'], request.form['version'], request.form['task'], request.form)
            else:
                extraClasses = {}
                for pointer in result[1]:
                    x, y = sudokuInput.squareToRowIndividual(pointer[0], pointer[1])
                    extraClasses[str(x) + str(y)] = 'incorrectSet'

                x, y = sudokuInput.squareToRowIndividual(result[0][0], result[0][1])
                extraClasses[str(x) + str(y)] = 'incorrectCell'
                return do_GET(['Sudoku is currently incorrect'], request.form['version'], request.form['task'], request.form, extraClasses)

    elif request.form['type'] == 'version':
        return do_GET(['Enter your sudoku by uploading an image or type directly into the sudoku.', 'Press solve sudoku when ready to.'], request.form['version'], request.form['task'], {}, {})

class sudoku():
    firstChange = []
    noOfSolutions = 1

    def __init__(self, rawData, SquareRowCount, SquareColCount, CellRowCount, CellColCount):
        self.squareRowCount = SquareRowCount
        self.squareColCount = SquareColCount
        self.cellRowCount = CellRowCount
        self.cellColCount = CellColCount

        self.grid = np.asarray(self.squareToRow([[rawData[str(col)+str(row)] for row in range(self.squareRowCount*self.squareColCount)] for col in range(self.squareRowCount*self.squareColCount)]))

        self.possible = ''
        for row in range(self.squareRowCount*self.squareColCount):
            for col in range(self.squareRowCount*self.squareColCount):
                if len(self.grid[row][col]) == 1 and self.grid[row][col] not in self.possible:
                    self.possible += self.grid[row][col]

        i = 0
        chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z']
        while len(self.possible) < self.cellRowCount*self.cellColCount:
            if chars[i] not in self.possible:
                self.possible += chars[i]
            i+=1

        self.possibilities = np.full(self.grid.shape, self.possible)
        for row in range(self.squareRowCount*self.squareColCount):
            for col in range(self.squareRowCount*self.squareColCount):
                if self.grid[row][col] != '':
                    self.possibilities[row][col] = str(self.grid[row][col])

    def getValues(self):
        values = {}
        squareGrid = self.squareToRow(self.grid)
        for square in range(self.squareRowCount*self.squareColCount):
            for cell in range(self.cellRowCount*self.cellColCount):
                values[str(square)+str(cell)] = squareGrid[square][cell]
        return values

    def getNoOfSolutions(self):
        return self.noOfSolutions

    def solve(self):
        if verbose:
            print('Solving')

        if self.check(self.possibilities):
            if verbose:
                self.display()
            self.applyRestrictions(self.possibilities)
            #self.display()

            if self.isSolved():
                if verbose:
                    print('Solved')
                self.grid = self.possibilities
            else:
                if verbose:
                    print('Backtracking')
                solutions = self.recursiveSolve(self.possibilities)
                self.noOfSolutions = len(solutions)

                if len(solutions) == 0:#If no solution dont update grid
                    self.noOfSolutions = 0
                else:
                    self.possibilities = solutions[0]
                    if self.firstChange == []:
                        for row in range(self.squareRowCount*self.cellRowCount):
                            for col in range(self.squareColCount*self.cellColCount):
                                if self.possibilities[row][col] != self.grid[row][col]:
                                    self.firstChange = [[row, col], self.possibilities[row][col]]

                    self.grid = self.possibilities
        else:#If no solution dont update grid
            self.noOfSolutions = 0

    def getHint(self):
        if self.isSolved() and self.check(self.grid) == True:
            return "complete"
        else:
            self.solve()
            if self.noOfSolutions == 0:
                return "unsolvable"
            else:
                return self.firstChange

    def checkSudoku(self):
        return self.check(self.possibilities)

    def check(self, grid):
        for restriction in self.getRestrictionPointers():
            for pointers in restriction:
                inRestriction = ''
                for pointer in pointers:
                    if len(grid[pointer[0]][pointer[1]]) == 1:
                        if grid[pointer[0]][pointer[1]] in inRestriction:
                            return [pointer, pointers]
                        inRestriction += grid[pointer[0]][pointer[1]]
                    if len(grid[pointer[0]][pointer[1]]) == 0:
                        return False

        return True

    def applyRestrictions(self, possibilities):
        previousPossibilities = []

        while previousPossibilities != str(possibilities):
            previousPossibilities = str(possibilities)
            for restriction in self.getRestrictionPointers():
                for pointers in restriction:
                    possibilities = self.remove(pointers, possibilities)
                    possibilities = self.insert(pointers, possibilities)

        return possibilities

    def getRestrictionPointers(self):
        yield self.rowRestriction()
        yield self.columnRestriction()
        yield self.squareRestriction()

    def recursiveSolve(self, possibilities):
        if self.check(possibilities) == True:
            row = 0
            col = 0
            while not len(possibilities[row][col]) > 1:

                row += 1
                if row == self.squareRowCount*self.cellRowCount:
                    col += 1
                    row = 0

                if col == self.squareColCount*self.cellColCount:#solution found
                    return [possibilities]

            solutions = []
            for possible in possibilities[row][col]:
                newPossibilities = [[str(possibilities[row][col]) for col in range(self.squareRowCount*self.cellRowCount)] for row in range(self.squareColCount*self.cellColCount)]
                newPossibilities[row][col] = possible
                solutions.extend(self.recursiveSolve(self.applyRestrictions(newPossibilities)))
                if len(solutions) > 300:
                    return solutions

            return solutions

        return []

    def isSolved(self):
        for row in range(self.squareRowCount*self.cellRowCount):
            for col in range(self.squareColCount*self.cellColCount):
                if len(self.possibilities[row][col]) != 1:
                    return False

        return True

    def remove(self, pointers, possibilities):
        for pointer in pointers:
            if len(possibilities[pointer[0]][pointer[1]]) == 1:
                for pointerRemove in pointers:
                    if pointerRemove != pointer:
                        if possibilities[pointer[0]][pointer[1]] in possibilities[pointerRemove[0]][pointerRemove[1]]:
                            if len(possibilities[pointerRemove[0]][pointerRemove[1]]) == 2:
                                if self.firstChange == []:
                                    self.firstChange = [pointerRemove, pointers]
                            possibilities[pointerRemove[0]][pointerRemove[1]] = possibilities[pointerRemove[0]][pointerRemove[1]].replace(possibilities[pointer[0]][pointer[1]], '')

        return possibilities

    def insert(self, pointers, possibilities):
        for number in range(len(self.possible)):
            sole = False
            for pointer in pointers:
                if str(number) in possibilities[pointer[0]][pointer[1]]:
                    if sole == False:
                        sole = pointer
                    else:
                        sole = False
                        break

            if sole != False and len(possibilities[sole[0]][sole[1]]) != 1:
                if self.firstChange == []:
                    self.firstChange = [sole, pointers]
                possibilities[sole[0]][sole[1]] = str(number)

        return possibilities

    def rowRestriction(self):
        for row in range(self.squareRowCount*self.cellRowCount):
            yield [[row, col] for col in range(self.squareColCount*self.cellColCount)]

    def columnRestriction(self):
        for col in range(self.squareColCount*self.cellColCount):
            yield [[row, col] for row in range(self.squareRowCount*self.cellRowCount)]

    def squareRestriction(self):
        for row in range(0,self.squareRowCount*self.cellRowCount,self.cellRowCount):
            for col in range(0,self.squareColCount*self.cellColCount,self.cellColCount):
                yield [[row+row2, col+col2] for col2 in range(0,self.cellColCount,1) for row2 in range(0,self.cellRowCount,1)]

    def display(self):
        self.grid[self.grid == ''] = ' '
        for row in self.grid:
            print([[row[col+col2] for col2 in range(0,self.cellColCount,1)] for col in range(0,self.squareColCount*self.cellColCount,self.cellColCount)])
        print()
        self.grid[self.grid == ' '] = ''

    def squareToRow(self, grid):
        return [[grid[row+row2][col+col2] for row2 in range(0,self.cellRowCount,1) for col2 in range(0,self.cellColCount,1)] for row in range(0,self.squareRowCount*self.cellRowCount,self.cellRowCount) for col in range(0,self.squareColCount*self.cellColCount,self.cellColCount)]

    def squareToRowIndividual(self, x, y):
        x2 = (x//self.squareRowCount)*self.squareColCount + y//self.cellRowCount
        y2 = (x%self.squareColCount)*self.squareRowCount + y%self.squareColCount
        return x2, y2

class sudokuX(sudoku):
    def __init__(self, rawData):
        super(sudokuX, self).__init__(rawData, 3, 3, 3, 3)

    def getRestrictionPointers(self):
        yield from super(sudokuX, self).getRestrictionPointers()
        yield self.diagonalRestriction()

    def diagonalRestriction(self):
        yield [[dia, dia] for dia in range(0, 9)]
        yield [[8-dia, dia] for dia in range(0, 9)]

def generateGaussianKernel(sigma, size):
    xDistance = np.array((2*size+1)*[[i for i in range(-size, size+1)]])
    distance = -0.5 * (xDistance**2 + xDistance.T**2)
    kernel = np.exp(distance/sigma**2)
    return kernel/kernel.sum()

class sudokuImage():
    def __init__(self, imageData, Directory = 'images/'):
        #Inherit Module by delegated wrapper
        self._img = imageData.convert('L')

        if self.height > 1000 or self.width > 1000:
            if self.height > self.width:
                self._img  = self._img.resize((1000, int(self.height*1000/self.width)))
            else:
                self._img  = self._img.resize((int(self.width*1000/self.height), 1000))
        self.directory = Directory

        #Initialise properties
        self.pixles = np.array([[self.getpixel((w, h)) for w in range(self.width)] for h in range(self.height)])
        self.values = np.zeros((9,9))
        self.confidences = np.zeros((9,9))

    #Inherit Module by delegated wrapper
    def __getattr__(self,key):
        return getattr(self._img,key)

    def transform(self, size, method, data, pixles):
        img = Image.fromarray(np.uint8(pixles)).transform(size, method, data)
        return np.array([[img.getpixel((w, h)) for w in range(img.width)] for h in range(img.height)])

    def getValues(self):
        outputValues = {}
        squareValues = self.squareToRow(self.values)

        for square in range(9):
            for cell in range(9):
                if squareValues[square][cell] != 0:
                    outputValues[str(square)+str(cell)] = str(squareValues[square][cell])[0]

        return outputValues

    def getConfidences(self):
        outputValues = {}
        squareValues = self.squareToRow(self.values)

        for square in range(9):
            for cell in range(9):
                outputValues[str(square)+str(cell)] = self.confidences[square][cell]

        return outputValues

    def updatePixles(self):
        self.pixles = np.array([[self.getpixel((w, h)) for w in range(self.width)] for h in range(self.height)])

    def savePixles(self):
        self._img = Image.fromarray(np.uint8(self.pixles))

    def squareToRow(self, grid):
        return [[grid[row+row2][col+col2] for row2 in range(0,3,1) for col2 in range(0,3,1)] for row in range(0,9,3) for col in range(0,9,3)]

    def recognise(self):
        if verbose:
            self.doSave('greyscale.jpg')

        #Detect edges
        threshold = self.adaptiveThreshold(self.pixles)
        if verbose:
            self.doSave('Threshold.jpg', threshold)

        #Isolate sudoku
        corners = self.findCorners(threshold)

        #Format into 252x252 square
        warped = self.transform((252,252), Image.QUAD, [i for j in corners for i in j[::-1]], threshold)

        if verbose:
            self.doSave('warped.jpg', warped)

        #separate into grid
        grid = self.getCells(corners, warped)

        #clean grid
        for row in range(9):
            for col in range(9):
                grid[row][col] = self.removeAllButlargest(grid[row][col])
                self.values[row][col], self.confidences[row][col] = nt.recognise(grid[row][col]/255)

    def removeAllButlargest(self, pixles):
        components = self.connectedComponents(pixles)

        #If on edges remove
        componentI = 0
        while componentI < len(components):
            remove = 0
            for pix in components[componentI]:
                if pix[0] == 0 or pix[0] == pixles.shape[0]-1 or pix[1] == 0 or pix[1] == pixles.shape[1]-1:
                    remove = 1
                    break
                if pix[0] == 1 or pix[0] == pixles.shape[0]-2 or pix[1] == 1 or pix[1] == pixles.shape[1]-2:
                    remove+=0.0625

                if pix[0] == 2 or pix[0] == pixles.shape[0]-3 or pix[1] == 2 or pix[1] == pixles.shape[1]-3:
                    remove+=0.03125

                if remove>=1:
                    break

            if remove>=1:
                del components[componentI]
            else:
                componentI += 1

        components = sorted(components, key = len)

        componentPixles = np.zeros(pixles.shape)

        if len(components) != 0:
            for pix in components[-1]:
                componentPixles[pix[0]][pix[1]] = 255

        return componentPixles


    def convolve(self, kernel, pixles):
        kernel = np.flipud(np.fliplr(kernel))
        newPixles = np.zeros(pixles.shape)
        kernelHeight = kernel.shape[0] // 2
        kernelWidth = kernel.shape[1] // 2
        pixlesHeight = pixles.shape[0]
        pixlesWidth = pixles.shape[1]

        for row in range(0, pixlesHeight):
            for col in range(0, pixlesWidth):
                lowRow = row-kernelWidth
                upRow = row+kernelWidth+1
                lowCol = col-kernelHeight
                upCol = col+kernelHeight+1
                div = kernelWidth*kernelHeight

                if lowRow < 0:
                    div += lowRow
                    lowRow = 0
                if lowCol < 0:
                    div += lowCol
                    lowCol = 0
                if upRow >= pixlesHeight-1:
                    div -= upRow-pixlesHeight-1
                    upRow = pixlesHeight-1
                if upCol >= pixlesWidth-1:
                    div -= upCol-pixlesWidth-1
                    upCol = pixlesWidth-1

                #Map kernel to sub-matrix then sum to give central pixle
                newPixles[row][col] = (kernel[lowRow-row+kernelWidth: upRow-row+kernelWidth, lowCol-col+kernelHeight:upCol-col+kernelHeight]*pixles[lowRow:upRow, lowCol:upCol]).sum()/div*kernelWidth*kernelHeight

        return newPixles

    def adaptiveThreshold(self, pixles):
        size = 15
        kernel = -generateGaussianKernel(5, size)
        kernel[size][size] = kernel[size][size]+1

        localMean = self.convolve(kernel, pixles)
        if verbose:
            self.doSave('lm.jpg', 255*(localMean-localMean.min())/(localMean-localMean.min()).max())

        localMean[localMean>-3] = 0
        localMean[localMean!=0] = 255

        return localMean

    def countOnEdge(self, component, corners):
        complete = np.full(self.pixles.shape, 255)
        count = 0

        for a, b in [[0,1],[1,2],[2,3],[3,0]]:#left, bottom, right top
            edgeImage = np.zeros(self.pixles.shape)
            dx = (corners[b][0] - corners[a][0])
            dy = (corners[b][1] - corners[a][1])
            lengthXY = (dx**2+dy**2)**(1/2)
            if lengthXY == 0:
                count += 1
            else:
                for pixle in component:
                    if abs((pixle[0] - corners[a][0])*dy - (pixle[1] - corners[a][1])*dx)/lengthXY <= 3:#On same line
                        count+=1
                        edgeImage[pixle[0]][pixle[1]] = 255

                    if complete[pixle[0]][pixle[1]] > abs((pixle[0] - corners[a][0])*dy - (pixle[1] - corners[a][1])*dx)/lengthXY:
                        complete[pixle[0]][pixle[1]] = abs((pixle[0] - corners[a][0])*dy - (pixle[1] - corners[a][1])*dx)/lengthXY

        if verbose:
            self.doSave('edge' + str(a) + str(b) + '.jpg', edgeImage)
            self.doSave('complete.jpg', complete)

        return count

    def findCorners(self, pixles):
        components = self.connectedComponents(pixles)
        components = sorted(components, key = len)

        #if verbose:
        #    for i in range(len(components)):
        #        self.saveArray('components/' + str(i) + '.jpg', components[i], pixles)

        possibleSudokus = components[-4:]
        possibleCorners = [[min(sudoku, key = lambda x:x[0]+x[1]), max(sudoku, key = lambda x:x[0]-x[1]), max(sudoku, key = lambda x:x[0]+x[1]), min(sudoku, key = lambda x:x[0]-x[1])] for sudoku in possibleSudokus]#lt lb rb rt

        #Find most Sudoku-like
        biggest = [0]
        for i in range(0, 4):
            if verbose:
                self.saveArray('currentComponent.jpg', possibleSudokus[i], pixles)
            size = self.countOnEdge(possibleSudokus[i], possibleCorners[i])*(i+2)/5

            if size >= biggest[0]:
                biggest = [size, i]

        if verbose:
            for i in range(1, 5):
                self.saveArray('component' + str(i) + '.jpg', components[-i], pixles)

        corners = possibleCorners[biggest[1]]
        if verbose:
            self.saveArray('corners.jpg', corners, pixles)

        if verbose:
            self.doSave('pix.jpg')

        return corners

    def removeComponent(self, component, pixles):
        for i in component:
            pixles[i[0]][i[1]] = 0

        return pixles

    def connectedComponents(self, pixles):
        self.pixlesTemp = np.copy(pixles)
        components = []
        for row in range(pixles.shape[0]):
            for col in range(pixles.shape[1]):
                if self.pixlesTemp[row][col] == 255:
                    component, overflows = self.floodFill(row, col)

                    while len(overflows) > 0:
                        moreOverflows = []
                        if verbose:
                            print(len(overflows))
                        for row, col in overflows:
                            for r in range(-1,2):
                                for c in range(-1,2):
                                    if r != 0 or c != 0 :
                                        componentIn, overflowIn = self.floodFill(row+r, col+c)
                                        component += componentIn
                                        moreOverflows += overflowIn

                        overflows = [i for i in moreOverflows]

                        if verbose:
                            print('uo', len(moreOverflows))

                    components.append(component)

        return components

    def floodFill(self, row, col, size = 0):
        if row >= 0 and row < self.pixlesTemp.shape[0] and col >= 0 and col < self.pixlesTemp.shape[1] and self.pixlesTemp[row][col] == 255:
            if size > 900:#overflow
                return [], [[row,col]]
            else:
                self.pixlesTemp[row][col] = 0
                component = [[row,col]]
                overflow = []
                for r in range(-1,2):
                    for c in range(-1,2):
                        if r != 0 or c != 0:
                            componentIn, overflowIn = self.floodFill(row+r, col+c, size+1)
                            component += componentIn
                            overflow += overflowIn

                return component, overflow
        else:
            return [], []

    def getCells(self, corners, pixles):
        grid = []
        cellWidth = 28
        cellHeight = 28

        yPosition = 0
        for y in range(9):
            xPosition = 0
            grid.append([])
            for x in range(9):
                grid[-1].append(pixles[yPosition:yPosition+28, xPosition:xPosition+28])#warning
                xPosition += 28
            yPosition += 28

        return grid

    #Test Saves
    def doSave(self, fileName, pixles=''):
        if verbose:
            print(fileName)
        if pixles == '':
            imageFromPixles = Image.fromarray(np.uint8(self.pixles))
        else:
            imageFromPixles = Image.fromarray(np.uint8(pixles))#.convert('RGB')
        imageFromPixles.save(self.directory + fileName)

    def saveArray(self, fileName, array, pixles):
        if verbose:
            print(fileName)
        validPixles = np.zeros(pixles.shape)
        for i in array:
            validPixles[i[0]][i[1]] = 255

        self.doSave(fileName, validPixles)

class network:
    def __init__(self, fileName = False):
        self.loadNet()
        self.dimensions = [784] + [len(i) for i in self.weights]

    def loadNet(self, filename = 'network.npz'):
        data = np.load(filename, allow_pickle=True)
        self.biases = data['bias']
        self.weights = data['weight']

    def run(self, activation):
        activations = [activation]
        for weight, bias in zip(self.weights, self.biases):
            activation = self.sigmoid(np.dot(weight, activation)+bias)
            activations.append(activation)
        return activations

    def sigmoid(self, matrix):
        return 1/(1+np.exp(-matrix))

    def recognise(self, image):
        activation = self.run(image.flatten())[-1]
        #display(image.flatten())
        #print(activation)
        #input(np.argmax(activation))
        return np.argmax(activation), np.max(activation)

def display(pixles):
    imageFromPixles = Image.fromarray(np.uint8([pixles[i:i+28]*255 for i in range(0,784,28)]))
    imageFromPixles.show()


verbose = False
nt = network()
