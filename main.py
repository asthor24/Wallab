import settings
from basic import Basic

f = open("script.wal", 'r')
code = f.read()
f.close()

settings.init()

# Splits the lines on a new line
lines = Basic.toLines(code)
# Loops through all the lines
for line in lines:
    if '=' in line:
        Basic.define(line)

    elif '/' in line:
        Basic.runFunction(line)

print("\n\n")

# Basic.printAll()
