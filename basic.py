import sys
import settings
from dataTypes import Integer
from dataTypes import Floating
from dataTypes import String
from dataTypes import Boolean

class Wallab:
    @staticmethod
    def arithmetic(line):
        vars = []
        name = ''
        for x in range(len(line)):
            letter = line[x]
            if letter == '+' or letter == '-' or letter == '*' or letter == '/' or letter == '%':
                vars.append(name)
                name = ''
                vars.append(letter)
            elif x == len(line) - 1:
                name += letter
                vars.append(name)
            else:
                name += letter
        for x in range(0, len(vars), 2):
            varType = Basic.findType(vars[x])
            if varType == 'i':
                vars[x] = str(settings.ints[vars[x]].val)

        return eval(''.join(vars))

    @staticmethod
    def logic(line):
        vars = []
        name = ''
        for letter in line:
            if letter != '<' and letter != '>' and letter != '=':
                name += letter
            else:
                if name != '':
                    vars.append(name)
                    name = ''
        if name != '':
            vars.append(name)

        for name in vars:
            varType = Basic.findType(name)
            if varType == 'i':
                line = line.replace(name, str(settings.ints[name].val))
            elif varType == 'f':
                line = line.replace(name, str(settings.floats[name].val))
            elif varType == 's':
                line = line.replace(name, str(settings.strings[name].val))
            elif varType == 'b':
                line = line.replace(name, str(settings.bools[name].val))
        return eval(line)

    @staticmethod
    def Input():
        s = input()
        return s

    @staticmethod
    def perform(name, params):
        if name == "Input":
            return Wallab.Input()
        elif name == "Arit":
            return Wallab.arithmetic(params[0])
        elif name == "Logic":
            return Wallab.logic(params[0])

class Basic:
    # method for printing all data
    @staticmethod
    def printAll():
        print("ints:", settings.ints)
        print("floats:", settings.floats)
        print("strings:", settings.strings)
        print("bools:", settings.bools)

    @staticmethod
    def findNameParams(func):
        params = []
        name = ''
        nameOut = ''
        add = False
        for letter in func:
            if letter == '(':
                add = True
            elif letter == ',':
                params.append(name)
                name = ''
            elif letter == ')':
                params.append(name)
            elif add:
                name += letter
            else:
                nameOut += letter
        return (nameOut, params)

    # method for finding type of variable from name
    @staticmethod
    def findType(name):
        if name in settings.ints:
            return 'i'
        elif name in settings.floats:
            return 'f'
        elif name in settings.strings:
            return 's'
        elif name in settings.bools:
            return 'b'

    # method for running a function given the string type name
    @staticmethod
    def runFunction(line):
        iswallab = False
        varFuncsTup = tuple(line.split('/'))
        varType = Basic.findType(varFuncsTup[0])
        if varType == 'i':
            varObj = settings.ints[varFuncsTup[0]]

        elif varType == 'f':
            varObj = settings.floats[varFuncsTup[0]]

        elif varType == 's':
            varObj = settings.strings[varFuncsTup[0]]

        elif varType == 'b':
            varObj = settings.bools[varFuncsTup[0]]

        elif varFuncsTup[0] == 'w':
            iswallab = True
            for x in range(len(varFuncsTup)-1):
                params = Basic.findNameParams(varFuncsTup[x + 1])
                return Wallab.perform(params[0], params[1])

        if not iswallab:
            for x in range(len(varFuncsTup)-1):
                params = Basic.findNameParams(varFuncsTup[len(varFuncsTup)-1])
                if varType == 'i':
                    varObj = Integer(varObj.perform(params[0], params[1]))
                elif varType == 'f':
                    varObj = Floating(varObj.perform(params[0], params[1]))
                elif varType == 's':
                    varObj = String(varObj.perform(params[0], params[1]))
                elif varType == 'b':
                    varObj = Boolean(varObj.perform(params[0], params[1]))

            return varObj


    # method for defining a variable and adding to appropriate dictionary
    @staticmethod
    def define(line):
        addVar = False
        addDef = False
        varName = ''
        value = ''
        for ind in range(len(line)):
            letter = line[ind]
            if letter == "|":
                addVar = True
            elif letter == '=':
                prev = line[ind-1]
                next = line[ind+1]
                if next != '=' and prev != '=' and next != '>' and prev != '>' and next != '<' and prev != '<':
                    addVar = False
                    addDef = True
                else:
                    value += letter
            elif addVar:
                varName += letter
            elif addDef:
                value += letter

        type = Basic.findType(value)
        if value[0] == "'" and value[len(value)-1] == "'" or value[0] == '"' and value[len(value)-1] == '"':
            settings.strings[varName] = String(value[1:len(value)-1])
            return

        elif "/" in value:
            value = Basic.runFunction(value)

        elif type:
            if type == 'i':
                value = settings.ints[value].val
            elif type == 'f':
                value = settings.floats[value].val
            elif type == 's':
                value = settings.strings[value].val
            elif type == 'b':
                value = settings.bools[value].val

        if line[0] == 'i':
            settings.ints[varName] = Integer(int(value))
        elif line[0] == 'f':
            settings.floats[varName] = Floating(float(value))
        elif line[0] == 's':
            settings.strings[varName] = String(str(value))
        elif line[0] == 'b':
            if value == 'False' or not value:
                settings.bools[varName] = Boolean(False)
            elif value == 'True' or value:
                settings.bools[varName] = Boolean(True)
            else:
                print("illegal name of boolean")
                sys.exit(0)


    # method for converting string to list of lines
    @staticmethod
    def toLines(code):
        lines = code.split('\n')
        newlines = list()
        for line in lines:
            if line != '':
                if '#' not in line:
                    line = line.replace("\t", "")
                    line = line.replace(" ", "")
                    newlines.append(line)

        forlines = list()
        lines = newlines
        newlines = list()
        begins = list()
        # ends = list()
        newIndex = 0
        add = True
        for ind in range(len(lines)):
            line = lines[ind]
            if line[0:8] == "<repeat(":
                forlines.append(list())
                num = ''
                for letter in range(8, len(line)-2):
                    num += line[letter]
                num = int(num)
                begins.append([newIndex, num])
                add = False
            elif line == "</repeat>":
                newIndex += len(forlines[len(forlines)-1])
                add = True
            elif add:
                newIndex += 1
                newlines.append(line)
            elif not add:
                forlines[len(forlines)-1].append(line)

        return lines









