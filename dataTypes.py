# This file contains data type classes
class Integer():
    def __init__(self, val):
        self.val = val

    def incr(self):
        self.val += 1
        return self.val

    def print(self):
        print(self.val)

    def perform(self, funcName, params):
        if funcName == "print":
            self.print()
        elif funcName == "incr":
            return self.incr()
        elif funcName == "get":
            return self.val


class Floating():
    def __init__(self, val):
        self.val = val

    def incr(self):
        return self.val + 1

    def print(self, newline=False):
        if newline:
            print(self.val)
        else:
            print(self.val, end="")

    def perform(self, funcName, redef=False, params=[]):
        if funcName == "print":
            self.print()
        elif funcName == "incr":
            if redef:
                self.val = self.incr()
            else:
                return self.incr()
        elif funcName == "get":
            return self.val

class String():
    def __init__(self, val):
        self.val = val

    def upper(self):
        return self.val.upper()

    def print(self):
        print(self.val)

    def perform(self, funcName, redef=False, params = []):
        if funcName == "print":
            self.print()
        elif funcName == "upper":
            if redef:
                self.val = self.upper()
            else:
                return self.upper()
        elif funcName == "get":
            return self.val

class Boolean:
    def __init__(self, val):
        self.val = val

    def print(self):
        print(self.val)

    def perform(self, funcName, params = []):
        if funcName == "print":
            self.print()
