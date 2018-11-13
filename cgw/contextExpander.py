# -*- coding: utf-8 -*-
import sys

if (len(sys.argv) < 2 ):
	print("Error - you need to supply a file to parse!")
	print("So I'm going to crash the program by dividing by zero, like a gentleman :)")
	print(5/0)

print('\nFile to Parse:'+ sys.argv[1]+'\n')
fileToParse = open(sys.argv[1],'r')
theFile = fileToParse.read()
#print('Fun fact!  Your file looks like this:\n',theFile,'\n')

#Here's the general idea - we go through the file line by line
#until we get to a {
#At which point we look for the <s on the upcoming lines, telling us what to loop through
#It is an important rule that nothing, not even comments, come between { and the <s
#The | tell us which to ignore, and must come directly after the <s if at all
#We continue line by line, expanding each line out according to our commands.
#Until we reach }
#Then its back to normal.

allLines = theFile.split('\n')
outputString = ""
bracketMode = False
finishedReadingAngles = False
finishedReadingPipes = False
templateDict = {}
ignoreTuples = []
killList = []

lineCounterOld = 0.0
lineCounterNew = 0.0

def checkUnorderedListEquality(s, t):
    return sorted(s) == sorted(t)

def doReplacing(line,listOfTemplators):
	global outputString
	global templateDict
	global ignoreTuples
	global lineCounterNew
	if listOfTemplators == []:
		splitline = line.split("∂");
		actualLine = line.split("∂")[0]
		if len(splitline) > 1:
			lineEnders = line.split("∂")[1:]
			#First check for any conditionals
			condSplit = actualLine.split("$")
			#Every odd index (if starting at 0) is a conditional - ex: a$cond1$b -> c$cond2$
			for cond in range(len(condSplit)):
				if cond%2 == 0: continue
				#a conditional looks like this: a,b,c=_a,_b,_c?x:y
				#Let's grab the components
				splitAtQmark = condSplit[cond].split("?")
				splitAtColon = splitAtQmark[1].split(":")
				splitAtEquals = splitAtQmark[0].split("=")
				toBeIfTrue = splitAtColon[0]
				toBeIfFalse = splitAtColon[1]
				templateCondition = splitAtEquals[0]
				valueOfCondition = splitAtEquals[1]
				templateConditions = templateCondition.split(',')
				valuesOfCondition  = valueOfCondition.split(',')
				tuplesToCheck = []
				for indx in range(len(templateConditions)):
					tuplesToCheck.append(templateConditions[indx] + ":" + valuesOfCondition[indx])
				#we want to know if the tuple is a subset of the lineEnders list
				if set(tuplesToCheck).issubset(set(lineEnders)):
					condSplit[cond] = toBeIfTrue
				else:
					condSplit[cond] = toBeIfFalse
				actualLine = "".join(condSplit)
		
			#Now check if on the ignore list
			#if any([checkUnorderedListEquality(lineEnders,x) for x in ignoreTuples]):
			if any([set(x).issubset(lineEnders) for x in ignoreTuples]):
				#It's on the ignore list!
				return
		splitlisttemp = actualLine.split()
		if not any([x in splitlisttemp for x in killList]):
			if len(actualLine.strip()) > 0 and actualLine.strip()[0] != '#':
				lineCounterNew = lineCounterNew + 1
			outputString = outputString + "\n" + actualLine
		return
	else:
		curTemplateRaw = listOfTemplators[0]
		curTemplate = curTemplateRaw.split("{")[1].split("}")[0]
		listOfTemplators = listOfTemplators[1:]
		for replacement in templateDict[curTemplate]:
			realReplacement = replacement
			if realReplacement == "ε":
				realReplacement = ""
			doReplacing(line.replace(curTemplateRaw,realReplacement)+"∂"+curTemplate + ":" + replacement,listOfTemplators)


for line in allLines:
	trimmed = line.strip()
	if trimmed == "{":
		if bracketMode:
			print("Double brackets error!!!")
			print(5/0)
		bracketMode = True
		continue
	elif trimmed == "}":
		finishedReadingAngles = False
		finishedReadingPipes = False
		templateDict = {}
		ignoreTuples = []
		if not bracketMode:
			print("Missing opening bracket")
			print(5/0)
		bracketMode = False
		continue
	elif not bracketMode:
		if len(trimmed) > 0 and trimmed[0] != '#' and trimmed[0] != '<':
			lineCounterOld = lineCounterOld + 1
		if (len(trimmed) > 0 and trimmed[0] != '<') or len(trimmed) == 0:
			outputString = outputString + "\n" + line
		elif len(trimmed) > 0:
			#add to kill list
			toKill = trimmed.split('<')[1].split('>')[0].split()[1:]
			killList = killList + toKill
	else:
		if len(trimmed) == 0:
			outputString = outputString + "\n"
			continue
		firstChar = trimmed[0]
		if firstChar == '<':
			if finishedReadingAngles:
				print("Angle bracket too late")
				print(5/0)
			#Readin here
			contents = trimmed.split('<')[1].split('>')[0].split() #split on whitespace
			templateDict[contents[0]] = contents[1:]
		else:
			finishedReadingAngles = True
			if firstChar == '|':
				if finishedReadingPipes:
					print("Pipe too late")
					print(5/0)
				#Readin here
				contents = trimmed.split('|')[1].split()[1:]
				ignoreTuples.append(contents)
			else:
				finishedReadingPipes = True
				#Now we are on the normal stuff
				#Copy each line unless it contains one of the templates
				#In which case perform the template
				if firstChar == '#':
					outputString = outputString + "\n" + line
				else:
					lineCounterOld = lineCounterOld + 1
					listOfTemplators = ["{" + x + "}" for x in templateDict.keys() if "{" + x + "}" in line]
					doReplacing(line,listOfTemplators)


#print(outputString)
outputString = "# The start symbol is TOP.\n# These two rules are required; choose their weights carefully!\n99  TOP  S1\n1   TOP  S2\n" + outputString
outputString = outputString + "\n# in case you use S1.gr by itself\n1   S2   Misc\n"
#fout = open("innerWorkings/S1.gr", "w")
#print(outputString)
#fout.write(outputString)
fout = open("contextExpanderOutput.txt", "w")
fout.write(outputString)
print("Input file had " + str(lineCounterOld) + " lines of production rules.")
print("This does not include comments, template headers, brackets, and whitespace")
print("Output file has " + str(lineCounterNew) + " lines of production rules.")
print("Thus the output file is " + str(lineCounterNew/lineCounterOld) + " times as large.")
print("The above figures are all pre-CNF")
